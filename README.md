# IntroDog

반려견 정보 및 나의 반려견 소개

## MONGO DB 설계

- USER
  - id(아이디)
  - password(비밀번호)
  - nickname(닉네임)
  - email(이메일)
  - dogCode(강아지코드)
  - profileUrl(프로필사진)
- DOGLIST

  - dogCode(강아지코드)
  - dogName(강아지명)
  - dogDesc(강아지설명)

- DOGIMG

  - dogCode(강아지코드)
  - seqNo(일련번호)
  - imgUrl(이미지경로)

- BOARD

  - id(user의 아이디)
  - boardNum(게시글번호)
  - title(게시글제목)
  - contents(게시글내용)
  - imgUrl(게시글이미지)
  - createTime(게시글작성시간)
  - updateTime(게시글수정시간)

- REPLY
  - boardNum(게시글번호)
  - seqNo(일련번호)
  - writer(댓글작성자)
  - contents(댓글내용)
  - createTime(댓글작성시간)

## API 설계

| 기능                 | Method | URL              | Request                                                                                         | Response                                                                                                                            |
| -------------------- | ------ | ---------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| 메인화면 페이지 로드 | GET    | /                | {'keyWord':keyWord}                                                                             | render_template('index.html',keyWord=keyWord)                                                                                       |
| 로그인 페이지 로드   | GET    | /login           | msg                                                                                             | render_template('login.html', msg=msg)                                                                                              |
| 회원가입 페이지 로드 | GET    | /join            |                                                                                                 | render_template('join.html')                                                                                                        |
| 글쓰기 페이지 로드   | GET    | /write           |                                                                                                 | Token 인증시 - render_template('board_write.html'), Token 미인증시 - {msg="로그인 정보가 존재하지 않습니다."}                       |
| ID 중복검사          | POST   | /api/check_dup   | {'id': check_id}                                                                                | 중복 아닐시 - {'msg': "사용 가능한 아이디 입니다."} 중복 시 - {'msg': "이미 존재하는 아이디 입니다."}                               |
| 회원가입             | POST   | /api/join        | {'id': id, 'pw': password}                                                                      | {'msg': '회원가입이 완료되었습니다.'}                                                                                               |
| 로그인               | POST   | /api/login       | {'id': id, 'pw': password}                                                                      | 로그인 성공 - {'result': 'success', 'token': token} 로그인 실패 - {'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'} |
| 게시글 조회          | get    | /boardList       |                                                                                                 | Token 인증시 - render_template('board_list.html'), Token 미인증시 - {msg="로그인 정보가 존재하지 않습니다."}                        |
| 게시글 수정          | POST   | /api/writeUpdate | {'boardNum':boardNum ,'writer': writer, 'contents': contents, 'title': title, 'imgUrl': imgUrl} | {msg="수정되었습니다."}                                                                                                             |
| 게시글 저장          | POST   | /api/writeCreate | {'writer': writer, 'contents': contents, 'title': title, 'imgUrl': imgUrl}                      | {msg="저장되었습니다."}                                                                                                             |
| 게시글 삭제          | POST   | /api/writeDelete | {'boardNum':boardNum}                                                                           | {msg="삭제되었습니다."}                                                                                                             |
| 댓글 저장            | POST   | /api/replyCreate | {'boardNum':boardNum ,'writer': writer, 'contents': contents                                    | {msg="저장되었습니다."}                                                                                                             |
| 댓글 삭제            | POST   | /api/replyDelete | {'boardNum':boardNum ,'seqNo' : seqNo                                                           | {msg="삭제되었습니다."}                                                                                                             |
