from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import pymongo
import config
app = Flask(__name__)

app.config["MONGODB_DB"] = "myFirstDatabase"
app.config['MONGO_URI'] = 'mongodb+srv://admin:admin@cluster0.og2k6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/getEliteUsers', methods=['GET'])
def get_elite_users():
  data = mongo.db.myData.aggregate([{"$limit": 20}, {"$match": {"elite": {"$ne": '"'}}}])
  output = []
  for obj in data:
    # print("this is the output", obj['name'])
    output.append({'name': obj['name'], 'review_count': obj['review_count'], 'yelping_since': obj['yelping_since']})
    # print(output)
  return jsonify({'result': output})

@app.route('/deleteUsers/<int:number>', methods = ["DELETE"])
def delete_users(number):
    ndoc = mongo.db.myData.find({}, ('_id',), limit=number)
    selector = {'_id': {'$in': [doc['_id'] for doc in ndoc]}}
    result = mongo.db.myData.delete_many(selector)
    print("The ackowledgement value is {0} and the deleted count {1}".format(result.acknowledged,  result.deleted_count))
    return jsonify({'result': result.acknowledged})


@app.route('/editReviewCount/<string:name>/<int:adder>', methods = ['PUT'])
def editReviewCount(name, adder):
  data = mongo.db.myData.find({"name":name})
  for obj in data:
    review_val = obj['review_count']
    mongo.db.myData.update_one({"_id": obj["_id"]}, {"$set":{'review_count': review_val + adder}}, True)
    # print("row is: ", obj)

  return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
