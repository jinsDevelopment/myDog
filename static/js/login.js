function login() {
    $.ajax({
        type: "POST",
        url: "/api/login",
        data: { id_give: $("#userid").val(), pw_give: $("#userpw").val() },
        success: function (response) {
            if (response["result"] == "success") {
                // 로그인이 정상적으로 되면, 토큰을 받아옵니다.
                // 이 토큰을 mytoken이라는 키 값으로 쿠키에 저장합니다.
                $.cookie("mytoken", response["token"]);

                alert("로그인 완료!");
                window.location.href = "/";
            } else {
                // 로그인이 안되면 에러메시지를 띄웁니다.
                alert(response["msg"]);
            }
        },
    });
}

function join() {
    window.location.href = "/join";
}
