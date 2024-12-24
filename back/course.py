class Course:
    def __init__(self, course_id, course_name, instructor):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.students = []
        self.materials = []
        self.assignments = []

    def add_material(self, material):
        self.materials.append(material)

    def add_assignment(self, assignment):
        self.assignments.append(assignment)

    def enroll_student(self, student):
        self.students.append(student)