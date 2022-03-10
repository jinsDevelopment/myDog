# IntroDog

반려견 정보 및 나의 반려견 소개

## MONGO DB 설계

- user

  - id(유저아이디) - PK
  - password(비밀번호)
  - nickname(닉네임)
  - email(이메일)
  - dogId(강아지코드)
  - profileImg(프로필사진)

- dog

  - id(강아지코드) - PK
  - name(강아지명)
  - desc(강아지설명)

- dogimg

  - dogId(강아지코드)
  - seqNo(일련번호)
  - imgUrl(이미지경로)

- board

  - id(게시글의 아이디) - PK
  - userId(유저의 아이디)
  - title(게시글제목)
  - contents(게시글내용)
  - imgUrl(게시글이미지)
  - createTime(게시글작성시간)
  - updateTime(게시글수정시간)

- reply
  - boardId(게시글의 아이디)
  - userId(유저의 아이디)
  - seqNo(일련번호)
  - contents(댓글내용)
  - createTime(댓글작성시간)

## API 설계

| 기능                 | Method | URL                   | Request                                                                                    | Response                                                                                                                            |
| -------------------- | ------ | --------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| 메인화면 페이지 로드 | GET    | /                     |                                                                         | render_template('index.html')                                                                                       |
| 로그인 페이지 로드   | GET    | /login                | msg                                                                                        | render_template('login.html', msg=errorMsg)                                                                                              |
| 회원가입 페이지 로드 | GET    | /join                 |                                                                                            | render_template('join.html')                                                                                                        |
| 글쓰기 페이지 로드   | GET    | /board/write          |                                                                                            | Token 인증시 - render_template('board_write.html'), Token 미인증시 - {msg="로그인 정보가 존재하지 않습니다."}                       |
| 회원가입시 선택할 강아지 목록 조회 | GET| /dog/list  | |jsonify({'msg': dog})|
| ID 중복검사          | POST   | /api/check_dup    | {'id': id}                                                                            | 중복 아닐시 - {'msg': "사용 가능한 ID 입니다"} 중복 시 - {'msg': "사용이 불가능한 ID 입니다."}                               |
| 회원가입             | POST   | /api/join        | {'file': file, 'email': email, 'id' :id, 'nickname':nickname, 'pw':password, 'dogCode',dog_result}                                                            | 회원가입 성공시 - {'msg': '회원가입이 완료되었습니다.'}  , 실패시 - 상황에 맞는 MSG 출력                                                                                             |
| 로그인               | POST   | /api/login       | {'id': id_give, 'pw': pw_give}                                                            | 로그인 성공 - {'result': 'success', 'token': token, "nickname":nickname } 로그인 실패 - {'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'} |
| 메인화면 강아지 이미지, 목록 조회 | GET    | /getDogList |                                                            | 조회 성공시 - {'dogList': dog_list, 'dogimgList': dogimg_list}   |
| 메인화면에서 강아지 검색어 조회          | POST    | /api/search         |         {'give_keyword': keyword}                                                                                   | 조회 성공시 - {'search_dog': search_dog, 'dogimgList': dogimg_list, 'receive_keywords': receive_keywords}                        |
| 게시글 작성          | GET    | /board/write         |                                                                                            | Token 인증시 - render_template('board_write.html', user_id = user_id, nickname = nickname, profileImg=user_info["profileImg"]), Token 인증 실패시 - make_response(redirect(url_for("login", errorCode=errorCode)))                        |
| 게시글 조회          | GET    | /board/select         |                                                                                            | Token 인증시 - render_template('board_list.html',result=boardList, user_id = user_id, nickname = nickname, profileImg=user_info["profileImg"] ), Token 인증 실패시 - make_response(redirect(url_for("login", errorCode=errorCode)))                        |
| 게시글 상세 조회     | GET    | /board/detail?id={id} |                {'id':board_id}                                                                            | Token 인증시 - render_template('board_detail.html', board=board, reply=reply_list, user_id=user_id, nickname = nickname, profileImg=user_info["profileImg"]), Token 인증 실패시 - make_response(redirect(url_for("login", errorCode=errorCode)))                      |
| 게시글 수정 화면 렌더링          | GET    | /board/modify?id={id}     | {'id':board_id} | render_template('board_update.html', board = board, user_id = user_id, nickname = nickname)                                                                                                          |
| 게시글 저장          | POST   | /board/create     | {'id':id, 'userId': user_id, 'contents': contents, 'title': title, 'imgUrl': imgUrl,'createTime': now.strftime("%Y-%m-%d %H:%M:%S"),'updateTime': now.strftime("%Y-%m-%d %H:%M:%S")}                | {msg="저장되었습니다."}                                                                                                             |
| 게시글 수정          | PUT   | /board/update     | {'id':boardId, 'contents': contents, 'title': title, 'imgUrl': imgUrl,'updateTime': now.strftime("%Y-%m-%d %H:%M:%S")}                | {msg="수정되었습니다."}                                                                                                             |
| 게시글 삭제          | DELETE | /board/delete     | {'id':id}                                                                            | {msg="삭제되었습니다."}                                                                                                             |
| 댓글 저장            | POST   | /board/reply/create     | {'boardId':board_Id ,'userId': user_id, 'contents': contents}                              | {msg="저장되었습니다."}                                                                                                             |
| 댓글 삭제            | DELETE | /board/reply/delete     | {'boardId':board_id,'seqNo' : seqNo}                                                                       | {msg="삭제되었습니다."}                                                                                                             |
