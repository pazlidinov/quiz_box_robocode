var sec = 120;
function pad(val) { return val > 9 ? val : "0" + val; }
setInterval(function () {
    document.getElementById("seconds").innerHTML = pad(--sec % 60);
    document.getElementById("minutes").innerHTML = pad(parseInt(sec / 60, 10));
    

    if (!Number(pad(--sec % 60))) {
        document.getElementById('repeat_send').style.display="inline"
        document.getElementById("watch").style.display="none"        
    }
}, 1000);

let new_phonenumber_completed = false;
function NewNumber() {
    let user_input = document.getElementById('phone');
    let user_phone_number = user_input.value.trim();
    let num = /^[0-9]+$/;
    for (let i = 0; i < user_phone_number.length; i++) {
        if (!(user_phone_number[i].match(num)) || user_phone_number.length != 9) {
            user_input.style.borderColor = 'red';
            new_phonenumber_completed = false;
            break;
        }
        else {
            user_input.style.borderColor = 'green';
            new_phonenumber_completed = true;
        }
    }

    let data = JSON.stringify(
        {
            "phone_number": user_phone_number,
        }
    )


    let url = 'check_phone_number/?data=' + data


    fetch(url).then(response => response.json()).then(data => {

        let message = document.getElementsByClassName('is_checked')[0];
        if (data["status"] == 200) {
            message.innerHTML = ''
            new_phonenumber_completed = true;
        }
        if (data["status"] == 404) {
            message.innerHTML = "Bu raqam ro'yhatdan o'tgan!";
            message.style.color = 'red';
            new_phonenumber_completed = false;
        }
    }).catch(error => (console.error(error)));
}

setInterval(function () {
    let send_button = document.getElementsByClassName('new_phonenumber')[0]
    if (new_phonenumber_completed) {
        send_button.removeAttribute('disabled');
    }
    else {
        send_button.setAttribute('disabled', true);
    }
}, 1000);