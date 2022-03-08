% API 구현

| 기능                 | Method | URL            | Request             | Response                                                                                                      |
| -------------------- | ------ | -------------- | ------------------- | ------------------------------------------------------------------------------------------------------------- |
| 메인화면 페이지 로드 | GET    | /              | {'keyWord':keyWord} | render_template('index.html',keyWord=keyWord)                                                                 |
| 로그인 페이지 로드   | GET    | /login         | msg                 | render_template('login.html', msg=msg)                                                                        |
| 회원가입 페이지 로드 | GET    | /join          | 290                 | render_template('join.html')                                                                                  |
| 글쓰기 페이지 로드   | GET    | /write         | 290                 | Token 인증시 - render_template('board_write.html'), Token 미인증시 - {msg="로그인 정보가 존재하지 않습니다."} |
| ID 중복검사          | POST   | /api/check_dup | {'id': check_id}    | 중복 아닐시 - {'msg': "사용 가능한 아이디 입니다."} 중복 시 - {'msg': "이미 존재하는 아이디 입니다."}286      |
