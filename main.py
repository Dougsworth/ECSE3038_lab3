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

userData = {}


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

#Profile  Routes 
@app.route('/profile')
def profile_get():
    global userData
    success = {
        "success" :True,
        "data" : userData
    }
    return jsonify(success)

@app.route('/profile', methods = ['POST'])
def profile_post():
    #obtain time stamp
    tVar = datetime.datetime.now(tz=pytz.timezone('America/Jamaica'))
    tVartoString = tVar.isoformat()
    #obtain json object from the request object
    userD = request.json
    #do the validation 
    if len(userD) > 0:
        #update global dictionary to show that a user has logged in
        global userData
        userData = userD
        #append time stamp to local dictionary and prepare for return
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
    global userData 

    tVar = datetime.datetime.now(tz=pytz.timezone('America/Jamaica'))
    tVartoString = tVar.isoformat()
    
    userD = request.json   
    
    if len(userData) > 0:
       
        userData = userD
        
        userD["last_updated"] = tVartoString
        success = {
        "successs":True,
        "data": userD
        }            
        return jsonify(success)
    else:
        return redirect(url_for("profile_get"))


if __name__ == "__main__":
    app.run(debug = True)
