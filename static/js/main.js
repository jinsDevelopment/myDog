'use strict';

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
