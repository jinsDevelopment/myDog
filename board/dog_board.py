from pymongo import MongoClient
import certifi
import app



mongo_connect = 'mongodb+srv://test:sparta@cluster0.u9lvb.mongodb.net/Cluster0?retryWrites=true&w=majority'
client = MongoClient(mongo_connect, tlsCAFile=certifi.where())
db = client.dbIntroDog

from flask import Blueprint, Flask, render_template, request, jsonify
from datetime import datetime

# 블루프린트 객체 생성
board = Blueprint("board", __name__, url_prefix="/board", template_folder="templates")


# 게시글 작성
@board.route('/write', methods=["GET"])
def board_write():

    # Token 미인증시 - 상황에 맞는 errorCode 출력
    if app.auth_token('board_write.html').get_json() is None:
        return app.auth_token('board_write.html')

    else:
        # Token 인증시 - render_template('board_write.html'),
        user_id = app.auth_token('board_write.html').get_json()['userId']
        return render_template('board_write.html', user_id = user_id)


# 게시글 목록
@board.route('/select', methods=["GET"])
def board_list():
    boardList = list(db.board.find({}, {'_id': False}))
    for i in range(0, len(boardList), 1):
        if boardList[i]['imgUrl'] == '':
            boardList[i]['imgUrl'] = 'empty.jpg'
    return render_template('board_list.html', result=boardList)


# 게시글 저장
@board.route('/create', methods=["POST"])
def board_save():
    title = request.form['title']
    contents = request.form['contents']
    user_id = request.form['userid']

    # 현재시간 구해오기
    now = datetime.now()
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
@board.route('/modify', methods=["GET"])
def board_modify():

    # Token 미인증시 - 상황에 맞는 errorCode 출력
    if app.auth_token('board_update.html').get_json() is None:
        return app.auth_token('board_update.html')

    else:
        # Token 인증시 - render_template('board_update.html'),
        user_id = app.auth_token('board_update.html').get_json()['userId']
        board = db.board.find_one({'id': int(request.args.get('id'))}, {'_id': False})
        return render_template('board_update.html', board = board, user_id = user_id)



# 게시글 수정
@board.route('/update', methods=["PUT"])
def board_update():
    title = request.form['title']
    contents = request.form['contents']
    orgFile = request.form['orgFile']
    boardId = request.form['boardId']

    board = db.board.find_one({'id': int(boardId)}, {'_id': False})

    # 현재시간 구해오기
    now = datetime.now()
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
@board.route('/detail', methods=["GET"])
def board_detail():

    # Token 미인증시 - 상황에 맞는 errorCode 출력
    if app.auth_token('board_detail.html').get_json() is None:
        return app.auth_token('board_detail.html')

    else:
        # Token 인증시 - render_template('board_detail.html')
        user_id = app.auth_token('board_detail.html').get_json()['userId']
        board = db.board.find_one({'id': int(request.args.get('id'))}, {'_id': False})
        reply_list = list(db.reply.find({'boardId': int(request.args.get('id'))}, {'_id': False}))
        if board['imgUrl'] == '':
            board['imgUrl'] = 'empty.jpg'

        return render_template('board_detail.html', board=board, reply=reply_list, user_id=user_id)


# 게시글 삭제
@board.route('/delete', methods=["DELETE"])
def board_delete():
    db.board.delete_one({'id': int(request.form['id'])})
    db.reply.delete_many({'boardId': int(request.form['id'])})
    # Token인증시 - render_template('board_detail.html'),
    # Token미인증시 - {msg = "로그인 정보가 존재하지 않습니다."}
    return jsonify({"msg": "삭제되었습니다."})


# 댓글 저장
@board.route('/reply/create', methods=["POST"])
def reply_create():
    boardId = request.form['board_id']
    contents = request.form['contents']
    userId = request.form['user_id']

    now = datetime.now()

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
@board.route('/reply/delete', methods=["DELETE"])
def reply_delete():
    db.reply.delete_one({'boardId': int(request.form['board_id']), 'seqNo': int(request.form['seqNo'])})
    # Token인증시 - render_template('board_detail.html'),
    # Token미인증시 - {msg = "로그인 정보가 존재하지 않습니다."}
    return jsonify({"msg": "삭제되었습니다."})
