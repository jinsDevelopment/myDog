'use strict';
const searchInput = document.querySelector('#input_kw');
const searchBtn = document.querySelector('.btn-search');
const searchForm = document.querySelector('.search__bar');

// form의 submit을 막아 줍니다.
searchForm.addEventListener('submit', (e) => {
  e.preventDefault();
});

// searchBtn에 클릭이벤트를 등록합니다.
searchBtn.addEventListener('click', search);

// searchInput에서 enter(keycode:13)를 눌러도 검색이 되게 합니다.
searchInput.addEventListener('keydown', (e) => {
  if (e.keyCode == 13) {
    search();
  }
});

function search() {
  let keyword = $('#input_kw').val();
  // search 함수 유효성 검사
  if (keyword == '') {
    alert('검색어를 입력하세요.');
    return;
  } else if (keyword.length < 2) {
    alert('두 글자 이상 입력 해주세요.');
    return;
  } else if (/[^가-힣0-9a-zA-Z ]/.test(keyword) == true) {
    alert('검색은 특수문자를 포함할 수 없습니다.');
    return;
  } else {
    $.ajax({
      type: 'POST',
      url: '/api/search',
      data: {
        give_keyword: keyword,
      },
      success: (response) => {
        let rows = response['search_dog'];
        let rowsImg = response['dogimgList'];

        // 검색창을 비워줍니다
        let searched_wt = response['search_dog'];
        searchInput.value = null;
        // 썸네일 창을 비워줍니다
        $('#thumbnail-box').empty();

        if (searched_wt == '') {
          alert('검색 결과가 없습니다.');
          window.location.reload();
        } else {
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
                                  <p class="thunmbnail__title card-text">${name}</p>
                                </div>
                              </div>
                            </div>
                          </button>`;
                $('#thumbnail-box').append(temp_html);
                break;
              }
            }
          }
        }
      },
    });
  }
}
