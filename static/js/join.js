let enabledSettings = [];

function join() {
    let dog_result = enabledSettings.toString();
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
function checkdup() {
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
            } else {
                alert("존재하지 않는 아이디입니다");
                $("#usernick").removeAttr("disabled");
                $("#userpw").removeAttr("disabled");
                $("#pwconfirm").removeAttr("disabled");
                $(".fa-check").show();
            }
        },
    });
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
