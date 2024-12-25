document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const errorMessage = document.getElementById('errorMessage');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        let valid = true;
        errorMessage.innerHTML = '';

        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        if (!validateEmail(email)) {
            valid = false;
            errorMessage.innerHTML += '<p>Invalid email address.</p>';
        }

        if (password.length < 6) {
            valid = false;
            errorMessage.innerHTML += '<p>Password must be at least 6 characters long.</p>';
        }

        if (valid) {
            // Submit the form or perform AJAX login
            console.log('Form is valid. Submitting...');
            loginForm.submit();
        }
    });

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
});