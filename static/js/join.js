function join() {
    $.ajax({
        type: "POST",
        url: "/api/join",
        data: {
            email: $("#useremail").val(),
            id: $("#userid").val(),
            nickname: $("#usernick").val(),
            pw: $("#userpw").val(),
            dogCode: $("#dogtype").val(),
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
