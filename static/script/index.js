
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.querySelector('.menu-toggle');
    const navLinks = document.getElementById('nav-links');
    
    toggleButton.addEventListener('click', () => {
        navLinks.classList.toggle('visible');
    });
});
