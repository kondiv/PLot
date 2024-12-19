function togglePasswordVisibility() {
    const passwordInput = document.getElementById('password');
    const showPasswordBtn = document.querySelector('.show-password-btn');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        showPasswordBtn.textContent = 'Скрыть';
    } else {
        passwordInput.type = 'password';
        showPasswordBtn.textContent = 'Показать';
    }
}


