from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

import config
import json
from bson import ObjectId


app = Flask(__name__)

app.config["MONGODB_DB"] = "myFirstDatabase"
app.config['MONGO_URI'] = 'mongodb+srv://admin:admin@cluster0.og2k6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/getEliteUsers/<string:year>', methods=['GET'])
def get_elite_users(year):
    data = mongo.db.myData.aggregate(
        [{"$match": {"elite": {"$regex": year}}}])

    output = json.dumps(list(data), default=str)
    # print(output)
    # for obj in data:
    #   # print("this is the output", obj['name'])
    #   output.append({'name': obj['name'], 'review_count': obj['review_count'], 'yelping_since': obj['yelping_since']})
    #   # print(output)
    return jsonify({'result': output})

# @app.route('/deleteUsers/<int:number>', methods = ["DELETE"])
# def delete_users(number):
#     ndoc = mongo.db.myData.find({}, ('_id',), limit=number)
#     selector = {'_id': {'$in': [doc['_id'] for doc in ndoc]}}
#     result = mongo.db.myData.delete_many(selector)
#     print("The ackowledgement value is {0} and the deleted count {1}".format(result.acknowledged,  result.deleted_count))
#     return jsonify({'result': result.acknowledged})

# @app.route('/updateRecordForID/<string:id>', methods = ["PUT"])
# def update_record(id):
#   data = mongo.db.myData.find({"_id":id})


@app.route('/getDonald', methods=['GET'])
def getDonald():
    data = mongo.db.myData.find({"name": "Donald"})
    output = json.dumps(list(data), default=str)
    return jsonify({'result': output})


@app.route('/editReviewCount/<int:adder>', methods=['PUT'])
def editReviewCount(adder):
    data = mongo.db.myData.find({"name": "Donald"})
    # mongo.db.myData.update({"_id": obj["_id"]}, {"$set":{'review_count': review_val + adder}}, True)
    for obj in data:
        review_val = obj['review_count']
        mongo.db.myData.update_one({"_id": obj["_id"]}, {
                                   "$set": {'review_count': review_val + adder}}, True)

    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
