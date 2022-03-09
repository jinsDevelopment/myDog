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

# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/community')
def community():
    return render_template('community.html')


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






@app.route('/boardList')
def board_list():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('boardList.html', nickname=user_info["nickname"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/write')
def write():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('write.html', nickname=user_info["nickname"])
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


@app.route('/api/check_dup', methods=['POST'])
def check_dup():
    id_receive = request.form["id"]

    exists = bool(db.user.find_one({"id": id_receive}))

    return jsonify({'exists': exists})


# [로그인 API]

@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id']
    pw_receive = request.form['pw']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'password': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})



import certifi
mongo_connect = 'mongodb+srv://test:sparta@cluster0.u9lvb.mongodb.net/Cluster0?retryWrites=true&w=majority'
clientT = MongoClient(mongo_connect,tlsCAFile=certifi.where())
dbT = clientT.dbIntroDog


#############################
# 반려견 종류 정보 가져오기
@app.route("/getDogList", methods=["GET"])
def getDogList():
    dog_list = list(dbT.dog.find({ 'id': { '$ne': '00'}}, {'_id': False}))
    dogimg_list = list(dbT.dogimg.find({},{'_id': False}))
    
    return jsonify({'dogList': dog_list, 'dogimgList': dogimg_list})

############################
# 메인에서 검색하기
@app.route('/api/search', methods=['POST'])
def search():
  receive_keywords = request.form["give_keyword"]
  print(receive_keywords)
  search_dog = list(dbT.dog.find({'name': {'$regex': '.*' + receive_keywords + '.*'}},{'_id': False}))
  dogimg_list = list(dbT.dogimg.find({},{'_id': False}))
  
  return jsonify({'search_dog': search_dog, 'dogimgList': dogimg_list, 'receive_keywords':receive_keywords})


##############################################
# 실행 파일
##############################################
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
