from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from python.board import board
import jwt
import datetime
import hashlib
import certifi
mongo_connect = 'mongodb+srv://test:sparta@cluster0.u9lvb.mongodb.net/Cluster0?retryWrites=true&w=majority'
client = MongoClient(mongo_connect,tlsCAFile=certifi.where())
db = client.dbIntroDog

app = Flask(__name__)
app.register_blueprint(board)

SECRET_KEY = 'SPARTA'




#################################
##  HTML을 주는 부분             ##
#################################



@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    if token_receive is None:
        return render_template('index.html')
    else:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.user.find_one({"id": payload['id']})
            return render_template('index.html', nickname=user_info["nickname"])
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/community')
def community():
    return render_template('community.html')


####### 데이터베이스에서 dog id랑 name 값 받아서 체크박스에 append시키기 ########
@app.route("/dog/list", methods=["GET"])
def bucket_get():
    dog = list(db.dog.find({}, {'_id': False}))
    return jsonify({'msg': dog})


#################################
##  로그인을 위한 API            ##
#################################

# [회원가입 API]

@app.route('/api/join', methods=['POST'])
def api_join():
    email_receive = request.form['email']
    id_receive = request.form['id']
    pw_receive = request.form['pw']
    nickname_receive = request.form['nickname']
    dogCode_receive = request.form['dogCode'].split(",")

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        "email": email_receive,
        "id": id_receive,
        "password": pw_hash,
        "nickname": nickname_receive,
        "dogId": dogCode_receive,

    }

    db.user.insert_one(doc)

    return jsonify({'result': 'success'})

# 회원가입 아이디 중복확인
@app.route('/api/check_dup', methods=['POST'])
def check_dup():
    id_receive = request.form["id"]

    exists = bool(db.user.find_one({"id": id_receive}))

    return jsonify({'exists': exists})


# [로그인 API]

@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.user.find_one({'id': id_receive, 'password': pw_hash})

    if result is not None:

        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# [유저 정보 확인 API]

@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:

        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nickname']})
    except jwt.ExpiredSignatureError:

        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5005, debug=True)
