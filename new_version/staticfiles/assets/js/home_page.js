let full_name_completed = false;
let phone_number_completed = false;
let age_completed = false;
let User_Location_completed = false;



function FullName() {
    let user_input = document.getElementsByName('full_name')[0];
    let user_full_name = user_input.value.trim();
    let letters = /^[a-zA-Zc' ']+$/;
    let is_numuric = false;
    for (let i = 0; i < user_full_name.length; i++) {
        if (!(user_full_name[i].match(letters))) {
            user_input.style.borderColor = 'red';
            is_numuric = true;
            full_name_completed = false;
            break;
        }
    }
    if (user_full_name.split(' ').length != 2 || is_numuric) {
        user_input.style.borderColor = 'red';
        full_name_completed = false;
    }
    else {
        user_input.style.borderColor = 'green';
        full_name_completed = true;
    }
}

function PhoneNumber() {
    let user_input = document.getElementsByName('phone')[0];
    let user_phone_number = user_input.value.trim();
    let num = /^[0-9]+$/;
    console.log('ok')
    for (let i = 0; i < user_phone_number.length; i++) {
        if (!(user_phone_number[i].match(num)) || user_phone_number.length != 9) {
            user_input.style.borderColor = 'red';
            phone_number_completed = false;
            break;
        }
        else {
            user_input.style.borderColor = 'green';
            phone_number_completed = true;
        }
    }

    let data = JSON.stringify(
        {
            phone_number: user_phone_number,
        }
    )

    let url = 'check_phone_number/?data=' + data

    fetch(url).then(response => response.json()).then(data => {
        let message = document.getElementsByName('is_checked')[0];
        if (data["status"] == 200) {
            message.innerHTML = ''
            phone_number_completed = true;
        }
        if (data["status"] == 404) {
            message.innerHTML = "Bu raqam ro'yhatdan o'tgan!";
            message.style.color = 'red';
            phone_number_completed = false;
        }
    }).catch(error => (console.log(error)));
}

function Age() {
    let user_input = document.getElementsByName('age')[0];
    let user_age = user_input.value.trim();
    let num = /^[0-9]+$/;

    for (let i = 0; i < user_age.length; i++) {
        if (!(user_age[i].match(num)) || 9 > Number(user_age) || Number(user_age) > 31) {
            user_input.style.borderColor = 'red';
            age_completed = false;
            break;
        }
        else {
            user_input.style.borderColor = 'green';
            age_completed = true;
            break;
        }
    }
}

function User_Location() {
    let user_input = document.getElementsByName('location')[0];
    let user_location = user_input.value.trim();

    if (user_location.length < 5) {
        user_input.style.borderColor = 'red';
        User_Location_completed = false;
    }
    else {
        user_input.style.borderColor = 'green';
        User_Location_completed = true;

    }
}

setInterval(function () {
    let send_button = document.getElementsByName('form_send')[0]
    if (full_name_completed && phone_number_completed && age_completed && User_Location_completed) {
        send_button.removeAttribute('disabled');
    }
    else {
        send_button.setAttribute('disabled', true);
    }
}, 1000);