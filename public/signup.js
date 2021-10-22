

function signUp() {
    var pw1 = document.getElementById("psw").value;
    var pw2 = document.getElementById("psw_repeat").value;
    if (pw1 != pw2) {
        alert("Passwords did not match");
    } else if (pw1.length < 6 || pw2.length < 6) {
        alert("Passwords too short");
    }
    else {
        // $.ajax({
        //     url: "sign",
        //     method: "POST",
        //     data: {email: document.getElementById('email').value, psw: document.getElementById('psw').value,
        //     psw_repeat: document.getElementById('psw_repeat').value},
        //     success: function(response) {

        //     }
        // });
        $.post('sign', {
            email: document.getElementById('email').value, psw: document.getElementById('psw').value,
            psw_repeat: document.getElementById('psw_repeat').value
        },
            function (returnedData) {
                alert("yay");
            });
    }
}