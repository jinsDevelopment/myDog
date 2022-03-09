let enabledSettings = [];

function join() {
    let dog_result = enabledSettings.toString();

    // checking email, nickname, password, password-confirm
    let email = $("#useremail").val();
    let id = $("#userid").val();
    let nickname = $("#usernick").val();
    let password = $("#userpw").val();
    let password_confirm = $("#pwconfirm").val();
    regExpId = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$/;
    // checking if validation is successful:

    if ($("#useremail").hasClass("regex-confirm-email")) {
        // $(".email-confirm").show();
        // $(".email-text-msg").hide();
        $("#userid").removeAttr("disabled");
        if ($("#userid").hasClass("regex-confirm-id") == true) {
            if ($("#usernick").hasClass("regex-confirm-nick")) {
                if ($("#userpw").hasClass("regex-confirm-pw")) {
                    if ($("#pwconfirm").hasClass("pw-confirm")) {
                        $.ajax({
                            type: "POST",
                            url: "/api/join",
                            data: {
                                email: $("#useremail").val(),
                                id: $("#userid").val(),
                                nickname: $("#usernick").val(),
                                pw: $("#userpw").val(),
                                dogCode: dog_result,
                            },
                            success: function (response) {
                                if (response["result"] == "success") {
                                    alert("회원가입이 완료되었습니다.");
                                    window.location.href = "/login";
                                } else {
                                    alert(response["msg"]);
                                }
                            },
                        });
                    }
                }
            }
            // alert("correct id");
        }
    }
    // checking if validation is unsuccessful
    if (email.includes("@") == false || email.includes(".") == false) {
        $(".email-confirm").hide();
        $(".email-text-msg").show();
    }
    if (regExpId.test(id) == false) {
        alert("아이디 방식이 잘못되었습니다");
    }
    if ($("#userid").hasClass("id-confirm") == false) {
        alert("아이디 중복확인이 필요합니다");
    }
    if ($("#userpw").hasClass("regex-confirm-pw") == false) {
        alert("비밀번호 방식이 잘못되었습니다");
    }
    if ($("#pwconfirm").hasClass("pw-confirm") == false) {
        alert("비밀번호가 틀립니다");
    }
}

// 이메일 정규표현식
function check_email() {
    let email = $("#useremail").val();
    if (email.includes("@") && email.includes(".")) {
        $(".email-confirm").show();
        $(".email-text-msg").hide();
        $("#useremail").addClass("regex-confirm-email");
        $("#userid").removeAttr("disabled");
    }
    if (email.includes("@") == false || email.includes(".") == false) {
        $(".email-confirm").hide();
        $(".email-text-msg").show();
        $("#useremail").removeClass("regex-confirm-email");
        $("#userid").attr("disabled", true);
    }
}

// 아이디 정규표현식
function check_id() {
    let id = $("#userid").val();
    regExpId = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$/;
    if (regExpId.test(id) == true) {
        $(".id-text-msg").hide();
        $("#userid").addClass("regex-confirm-id");
    }
    if (regExpId.test(id) == false) {
        $(".id-text-msg").show();
        $("#userid").removeClass("regex-confirm-id");
        $("#userid").removeClass("id-confirm");
    }
    if (
        $("#userid").hasClass("regex-confirm-id") == false &&
        regExpId.test(id) == false
    ) {
        $(".id-confirm-icon").hide();
        $("#usernick").attr("disabled", true);
        $("#userpw").attr("disabled", true);
        $("#pwconfirm").attr("disabled", true);
    }
}

// 닉네임 정규표현식
function check_nick() {
    if ($("#usernick").val() == "") {
        $(".nick-text-msg").show();
    } else {
        $("#usernick").addClass("regex-confirm-nick");
        $(".nick-text-msg").hide();
    }
}

// 비밀번호 정규표현식
function check_pw() {
    let password = $("#userpw").val();
    regExpPw = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    if (regExpPw.test(password) == false) {
        $(".pw-text-msg").show();
        $("#userpw").removeClass("regex-confirm-pw");
    } else {
        $(".pw-text-msg").hide();
        $("#userpw").addClass("regex-confirm-pw");
    }
}

// 비밀번호 중복확인
function confirm_pw() {
    if ($("#userpw").val() == $("#pwconfirm").val()) {
        $(".pw-confirm-text-msg").hide();
    } else {
        $(".pw-confirm-text-msg").show();
        $("#pwconfirm").addClass("pw-confirm");
    }
}

// 중복확인

function checkdup() {
    if ($("#userid").hasClass("regex-confirm-id") == true) {
        $.ajax({
            type: "POST",
            url: "/api/check_dup",
            data: {
                id: $("#userid").val(),
            },
            success: function (response) {
                if (response["exists"]) {
                    alert("존재하는 아이디입니다");
                    $("#usernick").attr("disabled", true);
                    $("#userpw").attr("disabled", true);
                    $("#pwconfirm").attr("disabled", true);
                    $(".id-confirm-icon").hide();
                    $("#userid").removeClass("id-confirm");
                    $("#userid").addClass("id-confirm");
                } else {
                    alert("존재하지 않는 아이디입니다");
                    $("#usernick").removeAttr("disabled");
                    $("#userpw").removeAttr("disabled");
                    $("#pwconfirm").removeAttr("disabled");
                    $(".id-confirm-icon").show();
                    $("#userid").addClass("id-confirm");
                }
            },
        });
    }
}

// dropdown

$(document).ready(function () {
    checkbox_append();
});

function checkbox_append() {
    $("#checkboxgroup").empty();
    $.ajax({
        type: "GET",
        url: "/dog/list",
        data: {},
        success: function (response) {
            let row = response["msg"];
            console.log(row);
            for (let i = 0; i < row.length; i++) {
                let id = row[i]["id"];
                let name = row[i]["name"];
                let temp_html = `<label for="task1" class="task">
                                    <input
                                        type="checkbox"
                                        name="${name}"
                                        id="${name}"
                                        value=${id}
                                    />
                                    ${name}
                                </label>`;
                $("#checkboxgroup").append(temp_html);
                onlyOneCheckBox();
            }
            var checkboxes = document.querySelectorAll("input[type=checkbox]");
            // let enabledSettings = [];

            checkboxes.forEach(function (checkbox) {
                checkbox.addEventListener("change", function () {
                    $(".show-list").empty();
                    enabledSettings = Array.from(checkboxes) // Convert checkboxes to an array to use filter and map.
                        .filter((i) => i.checked) // Use Array.filter to remove unchecked checkboxes.
                        .map((i) => i.value); // Use Array.map to extract only the checkbox values from the array of objects.

                    console.log(enabledSettings);
                    for (let i = 0; i < enabledSettings.length; i++) {
                        console.log(enabledSettings[i]);
                        let result = enabledSettings[i];
                        let select_name = $("input[value=" + result + "]").attr(
                            "id"
                        );
                        let temp_html = `<button onclick="takeOut(${result})" class="${result}"style="width:100px; height:40px; margin: 10px;">${select_name}</button>`;
                        if (select_name.length > 7) {
                            temp_html = `<button onclick="takeOut(${result})" class="${result}"style="width:140px; height:40px; margin: 10px; padding:0;">${select_name}</button>`;
                        }
                        $(".show-list").append(temp_html);
                    }
                });
            });
        },
    });
}

function takeOut(result) {
    console.log(result);
    if (result <= 9) {
        result = "0" + result;
        console.log(result);
    }
    $("input[value=" + result + "]").prop("checked", false);
    $("button[class=" + result + "]").remove();
    let checkboxes = document.querySelectorAll("input[type=checkbox]");
    enabledSettings = Array.from(checkboxes) // Convert checkboxes to an array to use filter and map.
        .filter((i) => i.checked) // Use Array.filter to remove unchecked checkboxes.
        .map((i) => i.value); // Use Array.map to extract only the checkbox values from the array of objects.

    console.log(enabledSettings);
}

// onlyOneCheckBox();
function onlyOneCheckBox() {
    var checkboxgroup = document
        .getElementById("checkboxgroup")
        .getElementsByTagName("input");
    var limit = 3;
    for (var i = 0; i < checkboxgroup.length; i++) {
        checkboxgroup[i].onclick = function () {
            var checkedcount = 0;
            for (var i = 0; i < checkboxgroup.length; i++) {
                checkedcount += checkboxgroup[i].checked ? 1 : 0;
            }
            if (checkedcount > limit) {
                console.log(
                    "You can select maximum of " + limit + " checkbox."
                );
                alert("최대  " + limit + "개 까지 고를실 수 있어요!");
                this.checked = false;
            }
        };
    }
}

document.querySelector(".select-field").addEventListener("click", () => {
    document.querySelector(".list").classList.toggle("show");
    document.querySelector(".down-arrow").classList.toggle("rotate180");
});

// checkbox "없음"을 고르면 다른 선택 불가능
