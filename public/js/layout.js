document.addEventListener("DOMContentLoaded", init)


let modal = document.getElementById('modal');
let login_tag = document.getElementById("login_tag")
let logout_tag = document.getElementById("logout_tag")
let login_form = document.querySelector(".login_form")
let register_form = document.querySelector(".register_form")
let login_btn = document.getElementById("login_btn")
let registe_btn = document.getElementById("registe_btn")
let goToRegister = document.getElementById("goToRegister")
let goToLogin = document.getElementById("goToLogin")
let closeBtn = document.getElementById("closeBtn")
let login_form_message = document.getElementById("login_form_message")
let register_form_message = document.getElementById("register_form_message")

window.addEventListener("click", (e) => {
    if (e.target === modal) {
        resetStatus()
    }
})

function resetStatus() {
    modal.style.display = "none";
    register_form.style.display = "none"
    login_form.style.display = "none"
    login_form_message.textContent = ""
    register_form_message.textContent = ""
}
function init() {
    loginValidation();
}

async function loginValidation() {
    let isLogin = await getUser()
    console.log(isLogin)
    if (isLogin.data === "null") {
        login_tag.style.display = "inline"
        logout_tag.style.display = "none"
        return
    }

    login_tag.style.display = "none"
    logout_tag.style.display = "inline"
}

login_tag.addEventListener("click", () => {
    modal.style.display = "block"
    login_form.style.display = "block"
})
closeBtn.addEventListener("click", () => {
    resetStatus()
})

goToRegister.addEventListener("click", () => {
    register_form.style.display = "block"
    login_form.style.display = "none"
    login_form_message.textContent = ""
})
goToLogin.addEventListener("click", () => {
    register_form.style.display = "none"
    login_form.style.display = "block"
    register_form_message.textContent = ""
})

registe_btn.addEventListener("click", () => {
    let registrationData = document.querySelectorAll("form.register_form input")
    let data = Array.from(registrationData).reduce((data, e) => {
        if (!data[e.name]) {
            data[e.name] = e.value
        }
        return data
    }, {})
    setUser("POST", data)
})

async function getUser() {
    return new Promise((resolve, reject) => {
        let url = new URL('http://127.0.0.1:3000/api/user');
        // let url = new URL('http://52.68.89.158:3000/api/user');

        let xhr = new XMLHttpRequest();
        xhr.open("GET", url);
        xhr.onload = function () {
            if (this.status !== 200) {
                return reject("資料讀取錯誤");
            }
            resolve(JSON.parse(this.responseText));
        };
        xhr.send();
    })
}

function setUser(method, data) {
    return new Promise((resolve, reject) => {
        // let csrf = "{{ csrf_token() }}";
        let url = new URL('http://127.0.0.1:3000/api/user');
        // let url = new URL('http://52.68.89.158:3000/api/user');

        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.setRequestHeader('Content-Type', 'application/json');
        // xhr.setRequestHeader('x-csrf-token', csrf);
        xhr.onload = function () {
            if (this.status !== 200) {
                return reject("資料讀取錯誤");
            }
            resolve(JSON.parse(this.responseText));
        };
        xhr.send(JSON.stringify(data));
    });
}
