# IntroDog
## MONGO DB 설계
  - USER
    - id(아이디)
    - password(비밀번호)
    - nickname(닉네임)
    - email(이메일)
    - dogCode(강아지코드)
    
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
    - boardTitle(게시글제목)
    - boardContents(게시글내용)
    - boardImg(게시글이미지)


## API 설계
|기능|Method|URL|Request|Response|
|------|---|---|---|---|
|테스트1|테스트2|테스트3|테스트3|테스트3|
|테스트1|테스트2|테스트3|테스트3|테스트3|
|테스트1|테스트2|테스트3|테스트3|테스트3|
