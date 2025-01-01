document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.querySelector('form');
    const errorMessage = document.createElement('div'); 
    registerForm.appendChild(errorMessage); // Append the error message at the end

    registerForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent default form submission
        let valid = true;
        errorMessage.innerHTML = ''; // Clear previous error messages
        errorMessage.classList.add('error-messages'); // Add a class for styling errors

        // Retrieve all form data
        const formData = new FormData(registerForm);

        // Validation checks
        if (!validateEmail(formData.get('email'))) {
            valid = false;
            errorMessage.innerHTML += '<p>Invalid email address.</p>';
        }

        if (formData.get('password').length < 6) {
            valid = false;
            errorMessage.innerHTML += '<p>Password must be at least 6 characters long.</p>';
        }

        if (!formData.get('confirm')) {
            valid = false;
            errorMessage.innerHTML += '<p>You must confirm that the provided information is correct.</p>';
        }

        if (valid) {
            // Submit the form via an AJAX request
            try {
                const response = await fetch('/user/register', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (response.ok) {
                    alert('Registration successful!');
                    window.location.href = '/user/login'; // Redirect to login page
                } else {
                    errorMessage.innerHTML += `<p>Error: ${result.error}</p>`;
                }
            } catch (error) {
                errorMessage.innerHTML += '<p>An unexpected error occurred. Please try again later.</p>';
            }
        }
    });

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
});
