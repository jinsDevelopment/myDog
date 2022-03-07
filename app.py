from pymongo import MongoClient
#import certifi
#mongo_connect = 'mongodb+srv://test:sparta@cluster0.u9lvb.mongodb.net/Cluster0?retryWrites=true&w=majority'
#client = MongoClient(mongo_connect,tlsCAFile=certifi.where())
#db = client.dbsparta

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/community')
def community():
    return render_template('community.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)