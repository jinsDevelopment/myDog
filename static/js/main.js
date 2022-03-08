function logout() {
  $.removeCookie('mytoken');
  alert('로그아웃!');
  window.location.href = '/login';
}

function boardList() {
  window.location.href = '/boardList';
}

function goLogin() {
  window.location.href = '/login';
}
function goJoin() {
  window.location.href = '/join';
}

function write_page() {
  window.location.href = '/write';
}
