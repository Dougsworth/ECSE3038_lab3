from flask import Flask, request, jsonify, json, redirect, url_for
from flask_pymongo import PyMongo
from marshmallow import Schema, fields, ValidationError
from bson.json_util import dumps
from json import loads
from flask_cors import CORS 
from pytz import datetime
import pytz

app = Flask(__name__)
CORS(app) 

app.config["MONGO_URI"] = "mongodb+srv://dougyd:Pd-tkSKDbMg3fNs@cluster0.5rdhy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)
ppl_D = {}


class TankSchema(Schema):
    location = fields.String(required = True)
    lat = fields.String(required = True)
    long = fields.String(required = True)
    percentage_full = fields.Integer(required = True)
     
#Data Routes 
@app.route("/data")
def data_get():
    tanks = mongo.db.tanks.find()
    return jsonify(loads(dumps(tanks)))

@app.route("/data", methods = ["POST"])
def add_data():
    try:
        newTank = TankSchema().load(request.json)
        newTank_id = mongo.db.tanks.insert_one(newTank).inserted_id
        tank = mongo.db.tanks.find_one(newTank_id)
        return loads(dumps(tank)) 
    except ValidationError as ve:
        return ve.messages, 400


@app.route('/data/<ObjectId:id>', methods = ["PATCH"])
def update_Data(id):
    mongo.db.tanks.update_one({"_id": id},{"$set": request.json})
    patch_Tank = mongo.db.tanks.find_one(id)
    return loads(dumps(patch_Tank))
        
@app.route('/data/<ObjectId:id>', methods = ["DELETE"])
def data_delete(id):
    result = mongo.db.tanks.delete_one({"_id":id})
    if result.deleted_count == 1:
        success = { "success":True,}
        return jsonify(success) 
    else:
        success = { "success":False}
        return jsonify(success), 400


#__________________________________________________________________________________________________________________
#Profile  Routes 
@app.route('/profile')
def profile_get():
    global ppl_D
    success = {
        "success" :True,
        "data" : ppl_D
    }
    return jsonify(success)

@app.route('/profile', methods = ['POST'])
def profile_post():
    tVar = datetime.datetime.now(tz=pytz.timezone('Jamaica'))
    tVartoString = tVar.isoformat()
    person_Data = request.json
    if len(person_Data) > 0:
        global ppl_D
        ppl_D = person_Data
        person_Data["last_updated"] = tVartoString
        success = {
            "successs":True,
            "data": person_Data
        }
        return jsonify(success)
    else:
        return redirect(url_for("profile_get"))

@app.route('/profile', methods = ["PATCH"])
def profile_patch():
    global ppl_D 

    tVar = datetime.datetime.now(tz=pytz.timezone('Jamaica'))
    tVartoString = tVar.isoformat()
    
    person_Data = request.json   
    
    if len(ppl_D) > 0:
       
        ppl_D = person_Data
        person_Data["last_updated"] = tVartoString
        success = {
        "successs":True,
        "data": person_Data
        }            
        return jsonify(success)
    else:
        return redirect(url_for("profile_get"))

if __name__ == "__main__":
    app.run(debug = True)
