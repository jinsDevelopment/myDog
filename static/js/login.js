function login() {
  let idInput = $('#userid').val();
  let psInput = $('#userpw').val();
  if (idInput != '' && psInput != '') {
    $.ajax({
      type: 'POST',
      url: '/api/login',
      data: { id_give: $('#userid').val(), pw_give: $('#userpw').val() },
      success: function (response) {
        if (response['result'] == 'success') {
          // 로그인이 정상적으로 되면, 토큰을 받아옵니다.
          // 이 토큰을 mytoken이라는 키 값으로 쿠키에 저장합니다.
          $.cookie('mytoken', response['token']);

          alert(response['nickname'] + '님 환영합니다');
          window.location.href = '/';
        } else {
          // 로그인이 안되면 에러메시지를 띄웁니다.
          alert(response['msg']);
        }
      },
    });
  }

  if (idInput == '') {
    $('.id-text-msg').show();
  }
  if (psInput == '') {
    $('.password-text-msg').show();
  }
  if (idInput != '' && psInput == '') {
    $('.password-text-msg').show();
    $('.id-text-msg').hide();
  }
  if (idInput == '' && psInput != '') {
    $('.id-text-msg').show();
    $('.password-text-msg').hide();
  }
}

function join() {
  window.location.href = '/join';
}
