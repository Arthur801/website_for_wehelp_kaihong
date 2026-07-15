// 前端檢查註冊資料是否有空值
const signupForm = document.getElementById("signup-form");
const signupName = document.getElementById("signup-user-name");
const signupEmail = document.getElementById("signup-email");
const signupPwd = document.getElementById("signup-password");

signupForm.addEventListener('submit', function(event) {
    const userName = signupName.value.trim();
    const email = signupEmail.value.trim();
    const password = signupPwd.value.trim();
    if (userName === '') {
        event.preventDefault();
        alert("請填寫姓名");
    } else if (email === '') {
        event.preventDefault();
        alert("請填寫email");
    } else if (password === '') {
        event.preventDefault();
        alert("請填寫密碼");
    } 
});

// 前端檢查登入資料是否有空值
const loginForm = document.getElementById("login-form");
const loginEmail = document.getElementById("login-email");
const loginPwd = document.getElementById("login-password");

loginForm.addEventListener('submit', function(event){ 
    const email = loginEmail.value.trim();
    const password = loginPwd.value.trim();
    if (email === "") {
        event.preventDefault();
        alert("請填寫email");
    } else if (password === '') {
        event.preventDefault();
        alert("請填寫密碼");
    } 
});