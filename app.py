from pymongo import MongoClient
import certifi
mongo_connect = 'mongodb+srv://test:sparta@cluster0.u9lvb.mongodb.net/Cluster0?retryWrites=true&w=majority'
client = MongoClient(mongo_connect,tlsCAFile=certifi.where())
db = client.dbIntroDog

from flask import Flask, render_template, request, jsonify
from python.board import board

app = Flask(__name__)

app.register_blueprint(board)

@app.route('/')
def home():

    return render_template('index.html')

# 반려견 종류 정보 가져오기
@app.route("/getDogList", methods=["GET"])
def getDogList():
    li = ""
    print(request.args.get('id'))
    if id is None:
        li = list(db.dog.find({}, {'_id': False}))
    else:
        li = list(db.dog.find({'id': request.args.get('id')}, {'_id': False}))
    print(li)
    return jsonify({'dogList': li})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)