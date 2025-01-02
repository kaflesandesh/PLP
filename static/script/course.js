document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems);

    // Handle edit button click
    document.querySelectorAll('.edit-course').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            var courseId = this.getAttribute('data-course-id');
            var courseName = this.getAttribute('data-course-name');

            // Populate the form with the course name and ID
            document.getElementById('course-id').value = courseId;
            document.getElementById('course-name').value = courseName;

            // Change the button text to "Update Course"
            document.getElementById('course-submit-button').textContent = 'Update Course';

            // Change the form action to the edit course endpoint
            document.getElementById('course-form').action = `/course/edit_course/${courseId}`;
        });
    });
});