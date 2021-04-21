from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import pymongo
import config
app = Flask(__name__)

app.config["MONGODB_DB"] = "myFirstDatabase"
app.config['MONGO_URI'] = 'mongodb+srv://admin:admin@cluster0.og2k6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

# app.config['MONGO_URI'] = 'mongodb+srv://'+config.USERNAME+':'+config.PASSWORD+'@cluster0.og2k6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

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


if __name__ == '__main__':
    app.run(debug=True)
