'use strict';
/***********************************
 * Thumbnail
 ***********************************/
// 메인 페이지가 로드되면 thumbnail을 보여줍니다.
window.addEventListener('load', () => {
  $.ajax({
    type: 'GET',
    url: '/getDogList',
    data: {},
    success: (response) => {
      let rows = response['dogList'];
      let rowsImg = response['dogimgList'];

      for (let i = 0; i < rows.length; i++) {
        // dogList의 code(id값)을 정의합니다.
        let code = rows[i]['id'];
        for (let j = 0; j < rowsImg.length; j++) {
          // dogimgList의 imgCode(dogId 값)을 정의합니다.
          let imgCode = rowsImg[j]['dogId'];
          // dog의 id값과 dogimg의 dogid값이 같으면 같은 종 입니다.
          if (code == imgCode) {
            let name = rows[i]['name'];
            let img = rowsImg[j]['imgUrl'];
            let desc = rows[i]['desc'];
            // thumbnail-box에 들어갈 temp_html을 정해줍니다.
            // modal창에 보여주기 위해 data-bs-* 속성이 필요합니다.
            let temp_html = `<button
                        type="button"
                        class="thumbnail"
                        data-bs-toggle="modal"
                        data-bs-target="#exampleModal"
                        data-bs-whatever="${name}"
                        data-bs-img="${img}"
                        data-bs-desc="${desc}"
                      >
                        <div class="col my-2">
                          <div class="card shadow-sm">
                            <img
                              src="${img}"
                              width="100%"
                              height="100%"
                              class="card-img-top"
                              title="${name}"
                              alt="${name}"
                            />
                            <div class="card-body">
                              <p class="thunmbnail__title">${name}</p>
                            </div>
                          </div>
                        </div>
                      </button>`;
            $('#thumbnail-box').append(temp_html);
            break;
          }
        }
      }
    },
  });
});

/***********************************
 * Modal
 ***********************************/
// 받아온 정보를 모달창에 넣어줍니다.
window.addEventListener('load', () => {
  const exampleModal = document.getElementById('exampleModal');
  exampleModal.addEventListener('show.bs.modal', function (event) {
    // 모달창을 열게한 버튼을 정의해줍니다.
    const button = event.relatedTarget;
    // data-*에서 속성을 추출해옵니다.
    const recipient = button.getAttribute('data-bs-whatever');
    const img = button.getAttribute('data-bs-img');
    const desc = button.getAttribute('data-bs-desc');

    // 모달창의 내용을 업데이트 해줍니다.
    const modalTitle = exampleModal.querySelector('.modal-title');
    const modalImg = document.getElementById('modal-img');
    const modalBody = document.querySelector('.modal-desc');

    modalTitle.textContent = recipient + ' 🐶';
    modalImg.src = img;
    modalBody.textContent = desc;
  });
});
