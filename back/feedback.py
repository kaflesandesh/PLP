# feedback.py
class Feedback:
    def __init__(self, feedback_id, student_id, course_id, content):
        self.feedback_id = feedback_id
        self.student_id = student_id
        self.course_id = course_id
        self.content = content