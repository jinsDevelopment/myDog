'use strict';
// 재혁님 작업
function logout() {
  $.removeCookie('mytoken',{ path: '/' });
  alert('정상적으로 로그아웃되었습니다.');
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
//

/*************************
 * topBtn function
 **************************/
const dm = document.documentElement;
const topBtn = document.querySelector('.top__btn');

const documentHeight = dm.scrollHeight;

window.addEventListener('scroll', function () {
  let scrollToTop = dm.scrollTop;

  if (documentHeight != 0) {
    const actionHeight = documentHeight / 4;

    if (scrollToTop > actionHeight) {
      topBtn.classList.remove('blind');
    } else {
      topBtn.classList.add('blind');
    }
  }
});

topBtn.addEventListener('click', function () {
  window.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
});
