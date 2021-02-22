
from json import loads
from bson.json_util import dumps
from flask_pymongo import PyMongo
from flask import Flask, request, jsonify, json
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://dougyd:Pd-tkSKDbMg3fNs@cluster0.5rdhy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)

class TankSchema(Schema):
  location = fields.String(required=True)
  lat = fields.Float(required=True)
  long = fields.Float(required=True)
  percentage_full = fields.Integer(required=True)

@app.route("/data")
def get_data():
  tanks = mongo.db.tanks.find()
  return jsonify(loads(dumps(tanks)))


@app.route("/data", methods=["POST"])
def add_data():
  try:
    newTank = TankSchema().load(request.json)
    Tank_id = mongo.db.tanks.insert_one(newTank).inserted_id
    retTank = mongo.db.tanks.find_one(Tank_id)
    return loads(dumps(retTank))
  except ValidationError as ve:
    return ve.messages, 400

@app.route("/data/<ObjectId:id>", methods=["PATCH"])
def update_data(id):
  mongo.db.tanks.update_one({"_id": id},{ "$set": request.json})

  tank = mongo.db.tanks.find_one(id)

  return loads(dumps(tank))

@app.route("/data/<ObjectId:id>", methods=["DELETE"])
def delete_data(id):
  result = mongo.db.tanks.delete_one({"_id": id})

  if result.deleted_count == 1:
    return {
      "success": True
    }
  else:

    return {
      "success": False
    }, 400

#________________________________________________________________________
#Profile Routes
@app.route('/profile')
def profile_get():
    global person_D
    success = {
        "success" :True,
        "data" : person_D
    }
    return jsonify(success)

@app.route('/profile', methods = ['POST'])
def profile_post():
    tVar = datetime.datetime.now(tz=pytz.timezone('Jamaica'))
    tVartoString = tVar.isoformat()
    userD = request.json
    
    if len(userD) > 0:
       
        global person_D
        person_D = userD
        
        userD["last_updated"] = tVartoString
        success = {
            "successs":True,
            "data": userD
        }
        return jsonify(success)
    else:
        return redirect(url_for("profile_get"))

@app.route('/profile', methods = ["PATCH"])
def profile_patch():
    global person_D 

    tVar = datetime.datetime.now(tz=pytz.timezone('Jamaica'))
    tVartoString = tVar.isoformat()
   
   
    userD = request.json   
   
    if len(person_D) > 0:
        
        person_D = userD
        
        userD["last_updated"] = tVartoString
        success = {
        "successs":True,
        "data": userD
        }            
        return jsonify(success)
    else:
        return redirect(url_for("profile_get"))


if __name__ == "__main__":
  app.run(debug=True)