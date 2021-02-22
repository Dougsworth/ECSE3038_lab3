from flask import Flask, request, jsonify, json
from flask_pymongo import PyMongo
from marshmallow import Schema, fields, ValidationError
from bson.json_util import dumps
from json import loads


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://dougyd:Pd-tkSKDbMg3fNs@cluster0.5rdhy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)

class FruitSchema(Schema):
  name = fields.String(required=True)
  sugar_content = fields.Float(required=True)
  color = fields.String(required=True)
  seed_num = fields.Integer(required=True)

@app.route("/fruit")
def get_fruits():
  fruits = mongo.db.fruits.find()
  return jsonify(loads(dumps(fruits)))


@app.route("/fruit", methods=["POST"])
def add_fruit():
  try:
    newFruit = FruitSchema().load(request.json)
    fruit_id = mongo.db.fruits.insert_one(newFruit).inserted_id
    fruit = mongo.db.fruits.find_one(fruit_id)
    return loads(dumps(fruit))
  except ValidationError as ve:
    return ve.messages, 400

@app.route("/fruit/<ObjectId:id>", methods=["PATCH"])
def update_fruit(id):
  mongo.db.fruits.update_one({"_id": id},{ "$set": request.json})

  fruit = mongo.db.fruits.find_one(id)

  return loads(dumps(fruit))

@app.route("/fruit/<ObjectId:id>", methods=["DELETE"])
def delete_fruit(id):
  result = mongo.db.fruits.delete_one({"_id": id})

  if result.deleted_count == 1:
    return {
      "success": True
    }
  else:

    return {
      "success": False
    }, 400


if __name__ == "__main__":
  app.run(debug=True)