from back.user_management.user import User

class Instructor(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.courses = []

    def create_course(self, course_name):
        pass  # Add logic for creating a course

    def grade_assignment(self, course_id, student_id, assignment_id, grade):
        pass  # Add logic for grading assignments
