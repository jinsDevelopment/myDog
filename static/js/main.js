'use strict';
// 재혁님 작업
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
//

/***********************************
 * Modal
 ***********************************/
// Put information received from db in modal window
const exampleModal = document.getElementById('exampleModal');
exampleModal.addEventListener('show.bs.modal', function (event) {
  // Button that triggered the modal
  const button = event.relatedTarget;
  // Extract info from data-bs-* attributes
  const recipient = button.getAttribute('data-bs-whatever');
  const thumbImg = button.getAttribute('data-img');

  // Update the modal's content.
  const modalTitle = exampleModal.querySelector('.modal-title');
  const modalImg = document.getElementById('modal-img');

  modalTitle.textContent = recipient;
  modalImg.src = thumbImg;
});
