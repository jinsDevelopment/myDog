from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, session, redirect, url_for, make_response
import jwt
import datetime
import hashlib
import certifi
import json
mongo_connect = 'mongodb+srv://test:sparta@cluster0.u9lvb.mongodb.net/Cluster0?retryWrites=true&w=majority'
client = MongoClient(mongo_connect, tlsCAFile=certifi.where())
db = client.dbIntroDog

app = Flask(__name__)


SECRET_KEY = 'SPARTA'


def auth_token(page):
    token_receive = request.cookies.get('mytoken')
    if page == 'index.html':
        if token_receive is None:
            return render_template('index.html')
        else:
            try:
                payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
                user_info = db.user.find_one({"id": payload['id']})
                return render_template(f'{page}', userId=user_info["id"], profileImg=user_info["profileImg"], nickname=user_info["nickname"])
            except jwt.ExpiredSignatureError:
                return render_template(f'{page}')
            except jwt.exceptions.DecodeError:
                return render_template(f'{page}')

    else:
        if token_receive is None:
            return make_response(redirect(url_for("login", errorCode="0")))
        else:
            try:
                payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
                user_info = db.user.find_one({"id": payload['id']})

                user_data = {
                    'userId': user_info['id'],
                    'nickname': user_info['nickname']
                }
                response = app.response_class(
                    response=json.dumps(user_data),
                    mimetype='application/json'
                )
                return response
            except jwt.ExpiredSignatureError:
                return make_response(redirect(url_for("login", errorCode="1")))

            except jwt.exceptions.DecodeError:
                return make_response(redirect(url_for("login", errorCode="2")))

#################################
##  HTML을 주는 부분             ##
#################################

@app.route('/')
def home():
    
    return auth_token('index.html')

@app.route('/login')
def login():
    code = request.args.get("errorCode")

    errorMsg = ""
    if code == "0":
        errorMsg = "로그인을 해주세요"
    elif code == "1":
        errorMsg = "로그인 시간이 만료되었습니다."
    elif code == "2":
        errorMsg = "로그인 정보가 존재하지 않습니다."

    return render_template('login.html', msg=errorMsg)


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

    # 현재시간 구해오기
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    imgUrl = ""

    if len(request.files) != 0:
        # 새로운 이름을 만들어주기
        filename = f'file-{date_time}'

        # 확장자를 빼내기
        file = request.files['file']
        extension = file.filename.split(",")[-1]

        # 새로운 이름으로 저장하기
        save_to = f'static/images/{filename}.{extension}'
        file.save(save_to)

        imgUrl = f'{filename}.{extension}'
    else:
        imgUrl = "blank_profile.png"

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        "email": email_receive,
        "id": id_receive,
        "password": pw_hash,
        "nickname": nickname_receive,
        "dogId": dogCode_receive,
        'profileImg': imgUrl,

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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        user_info = db.user.find_one({"id": payload['id']})
        nickname=user_info["nickname"]
        return jsonify({'result': 'success', 'token': token, "nickname":nickname})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

#############################
# 반려견 종류 정보 가져오기
@app.route("/getDogList", methods=["GET"])
def getDogList():
    dog_list = list(db.dog.find({'id': {'$ne': '00'}}, {'_id': False}))
    dogimg_list = list(db.dogimg.find({}, {'_id': False}))

    return jsonify({'dogList': dog_list, 'dogimgList': dogimg_list})


############################
# 메인에서 검색하기
@app.route('/api/search', methods=['POST'])
def search():
    receive_keywords = request.form["give_keyword"]
    print(receive_keywords)
    search_dog = list(db.dog.find({'name': {'$regex': '.*' + receive_keywords + '.*'}}, {'_id': False}))
    dogimg_list = list(db.dogimg.find({}, {'_id': False}))

    return jsonify({'search_dog': search_dog, 'dogimgList': dogimg_list, 'receive_keywords': receive_keywords})



############################
# board.py 소스


# 게시글 작성
@app.route('/board/write', methods=["GET"])
def board_write():

    # Token 미인증시 - 상황에 맞는 errorCode 출력
    if auth_token('board_write.html').get_json() is None:
        return auth_token('board_write.html')

    else:
        # Token 인증시 - render_template('board_write.html'),
        user_id = auth_token('board_write.html').get_json()['userId']
        nickname = auth_token('board_list.html').get_json()['nickname']
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('board_write.html', user_id = user_id, nickname = nickname, profileImg=user_info["profileImg"])


# 게시글 목록
@app.route('/board/select', methods=["GET"])
def board_list():
    
    # Token 미인증시 - 상황에 맞는 errorCode 출력
    if auth_token('board_list.html').get_json() is None:
        return auth_token('board_list.html')

    else:
        # Token 인증시 - render_template('board_list.html'),
        user_id = auth_token('board_list.html').get_json()['userId']
        nickname = auth_token('board_list.html').get_json()['nickname']
        boardList = list(db.board.find({}, {'_id': False}))
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})

        for i in range(0, len(boardList), 1):
            if boardList[i]['imgUrl'] == '':
                boardList[i]['imgUrl'] = 'empty.jpg'
            if len(boardList[i]['title']) >= 12:
                boardList[i]['title'] = boardList[i]['title'][0:12]+"..."
            if len(boardList[i]['contents']) >= 20:
                boardList[i]['contents'] = boardList[i]['contents'][0:36]+"..."

        return render_template('board_list.html',result=boardList, user_id = user_id, nickname = nickname, profileImg=user_info["profileImg"] )


# 게시글 저장
@app.route('/board/create', methods=["POST"])
def board_save():
    title = request.form['title']
    contents = request.form['contents']
    user_id = request.form['userid']

    # 현재시간 구해오기
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    imgUrl = ""

    if len(request.files) != 0:
        # 새로운 이름을 만들어주기
        filename = f'file-{date_time}'

        # 확장자를 빼내기
        file = request.files['file']
        extension = file.filename.split(",")[-1]

        # 새로운 이름으로 저장하기
        save_to = f'static/images/{filename}.{extension}'
        file.save(save_to)

        imgUrl = f'{filename}.{extension}'

    # 여러개 찾기 - 예시 ( _id 값은 제외하고 출력)
    board_list = list(db.board.find({}, {'_id': False}))
    lists = []
    count = 0
    for li in board_list:
        lists.append(li['id'])

    if len(lists) == 0:
        count = 1
    else:
        count = int(max(lists)) + 1

    # 변경된 파일 이름을 db에도 저장하기
    doc = {
        'id': count,
        'title': title,
        'contents': contents,
        'userId': user_id,
        'imgUrl': imgUrl,
        'createTime': now.strftime("%Y-%m-%d %H:%M:%S"),
        'updateTime': now.strftime("%Y-%m-%d %H:%M:%S"),
    }

    db.board.insert_one(doc)

    # board
    # - id(게시글의 아이디) - PK
    # - userId(유저의 아이디)
    # - title(게시글제목)
    # - contents(게시글내용)
    # - imgUrl(게시글이미지)
    # - createTime(게시글작성시간)
    # - updateTime(게시글수정시간)

    return jsonify({"msg": "저장되었습니다."})


# 게시글 수정 화면 렌더링
@app.route('/board/modify', methods=["GET"])
def board_modify():

    # Token 미인증시 - 상황에 맞는 errorCode 출력
    if auth_token('board_update.html').get_json() is None:
        return auth_token('board_update.html')

    else:
        # Token 인증시 - render_template('board_update.html'),
        user_id = auth_token('board_update.html').get_json()['userId']
        nickname = auth_token('board_list.html').get_json()['nickname']
        board = db.board.find_one({'id': int(request.args.get('id'))}, {'_id': False})
        return render_template('board_update.html', board = board, user_id = user_id, nickname = nickname)



# 게시글 수정
@app.route('/board/update', methods=["PUT"])
def board_update():
    title = request.form['title']
    contents = request.form['contents']
    orgFile = request.form['orgFile']
    boardId = request.form['boardId']

    board = db.board.find_one({'id': int(boardId)}, {'_id': False})

    # 현재시간 구해오기
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H-%M-%S")

    imgUrl = ""
    imgChange = False
    if board['imgUrl'] != orgFile:

        if len(request.files) != 0:
            # 새로운 이름을 만들어주기
            filename = f'file-{date_time}'

            # 확장자를 빼내기
            file = request.files['file']
            extension = file.filename.split(",")[-1]

            # 새로운 이름으로 저장하기
            save_to = f'static/images/{filename}.{extension}'
            file.save(save_to)

            imgUrl = f'{filename}.{extension}'
            imgChange = True

    # 변경된 사항 db 저장
    doc = {
        'title': title,
        'contents': contents,
        'imgUrl': imgUrl if imgChange else board['imgUrl'],
        'updateTime': now.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # 업데이트
    db.board.update_one({'id': int(boardId)}, {'$set': doc})

    # board
    # - id(게시글의 아이디) - PK
    # - userId(유저의 아이디)
    # - title(게시글제목)
    # - contents(게시글내용)
    # - imgUrl(게시글이미지)
    # - createTime(게시글작성시간)
    # - updateTime(게시글수정시간)

    # Token인증시 - render_template('board_write.html'),
    # Token미인증시 - {msg = "로그인 정보가 존재하지 않습니다."}
    return jsonify({"msg": "수정되었습니다."})


# 게시글 상세
@app.route('/board/detail', methods=["GET"])
def board_detail():

    # Token 미인증시 - 상황에 맞는 errorCode 출력
    if auth_token('board_detail.html').get_json() is None:
        return auth_token('board_detail.html')

    else:
        # Token 인증시 - render_template('board_detail.html')
        user_id = auth_token('board_detail.html').get_json()['userId']
        nickname = auth_token('board_detail.html').get_json()['nickname']
        board = db.board.find_one({'id': int(request.args.get('id'))}, {'_id': False})
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        reply_list = list(db.reply.find({'boardId': int(request.args.get('id'))}, {'_id': False}))
        if board['imgUrl'] == '':
            board['imgUrl'] = 'empty.jpg'

        return render_template('board_detail.html', board=board, reply=reply_list, user_id=user_id, nickname = nickname, profileImg=user_info["profileImg"])


# 게시글 삭제
@app.route('/board/delete', methods=["DELETE"])
def board_delete():
    db.board.delete_one({'id': int(request.form['id'])})
    db.reply.delete_many({'boardId': int(request.form['id'])})
    # Token인증시 - render_template('board_detail.html'),
    # Token미인증시 - {msg = "로그인 정보가 존재하지 않습니다."}
    return jsonify({"msg": "삭제되었습니다."})


# 댓글 저장
@app.route('/board/reply/create', methods=["POST"])
def reply_create():
    boardId = request.form['board_id']
    contents = request.form['contents']
    userId = request.form['user_id']

    now = datetime.datetime.now()

    reply_list = list(db.reply.find({'boardId': int(boardId)}, {'_id': False}))
    lists = []
    seqNo = 0
    for li in reply_list:
        lists.append(li['seqNo'])

    if len(lists) == 0:
        seqNo = 1
    else:
        seqNo = int(max(lists)) + 1

    doc = {
        'boardId': int(boardId),
        'contents': contents,
        'userId': userId,
        'createTime': now.strftime("%Y-%m-%d %H:%M:%S"),
        'seqNo': seqNo
    }
    print(doc)
    db.reply.insert_one(doc)

    # Token인증시 - render_template('board_detail.html'),
    # Token미인증시 - {msg = "로그인 정보가 존재하지 않습니다."}

    # reply
    # - boardId(게시글의 아이디)
    # - userId(유저의 아이디)
    # - seqNo(일련번호)
    # - contents(댓글내용)
    # - createTime(댓글작성시간)

    return jsonify({"msg": "저장되었습니다."})


# 댓글 삭제
@app.route('/board/reply/delete', methods=["DELETE"])
def reply_delete():
    db.reply.delete_one({'boardId': int(request.form['board_id']), 'seqNo': int(request.form['seqNo'])})
    # Token인증시 - render_template('board_detail.html'),
    # Token미인증시 - {msg = "로그인 정보가 존재하지 않습니다."}
    return jsonify({"msg": "삭제되었습니다."})

##############################################
# 실행 파일
##############################################

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
