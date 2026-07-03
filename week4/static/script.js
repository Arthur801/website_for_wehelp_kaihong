const loginForm = document.getElementById("login-form");
const confirmPolicy = document.querySelector('input[name="confirm-policy"]');
const errorMessageNoChecked = document.getElementById("login-error");

const searchBtn = document.getElementById("search-btn");
const hotelSearchId = document.getElementById("hotel-search-id");


loginForm.addEventListener('submit', function(event) {
    if(!confirmPolicy.checked) {
        event.preventDefault();
        errorMessageNoChecked.style.display = 'block';
        alert("請勾選同意條款")
    }
    else {
        errorMessageNoChecked.style.display = 'none';
    }
});

searchBtn.addEventListener('click', function(event) {
    const hotelId = Number(hotelSearchId.value.trim());
    if (!Number.isInteger(hotelId) || hotelId <= 0) {
        alert("請輸入正整數");
        return;
    }
    window.location.href = `/hotel/${hotelId}`;
});