

function signUp() {
    var username = document.getElementById("username").value;
    var pw1 = document.getElementById("psw").value;
    var pw2 = document.getElementById("psw_repeat").value;
    if (username.length < 6) {
        alert("username is too short");
    }
    else if (pw1 != pw2) {
        alert("Passwords did not match");
    } else if (pw1.length < 6 || pw2.length < 6) {
        alert("Passwords too short");
    }
    else {
        alert("ddd");
        $.post('signup', {
            email: document.getElementById('email').value, psw: document.getElementById('psw').value,
            psw_repeat: document.getElementById('psw_repeat').value
        },function (returnedData) {
                alert("yay");
            });
    }
}