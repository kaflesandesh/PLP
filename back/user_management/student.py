from back.user_management.user import User

class Student(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.enrolled_courses = []
        self.progress = {}

    def enroll_in_course(self, course):
        self.enrolled_courses.append(course)

    def submit_assignment(self, course_id, assignment_id, submission):
        pass  # Add logic for assignment submission

    def view_progress(self):
        return self.progress
