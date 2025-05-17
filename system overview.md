# System Overview

## 1. Plan the System Workflow

**Core Idea:**  
A personalized educational platform for rural students, enabling interactive learning, progress tracking, and modern technology integration (e.g., LLMs) for accessible, engaging education.

---

### System Workflow

#### Authentication & User Management
- **Roles:**  
    - **Admin:** System management (courses, roles)  
    - **Instructor:** Upload content, assignments, feedback  
    - **Student:** Access materials, submit assignments, view feedback
- **Features:**  
    - Secure login/signup  
    - Role-based access control

#### Course Management
- Instructors create/manage courses and materials
- Students enroll and complete assignments
- Admin oversees approvals and modifications

#### Learning Materials
- Host PDFs, videos, quizzes, interactive content
- Offline access for students

#### Feedback & Progress
- Real-time activity tracking
- Student-instructor feedback loop
- Personalized progress reports

#### System Utilities
- Bug reporting
- Maintenance & updates

#### LLM Integration
- AI chatbot for Q&A and tutoring
- Automated grading
- Content summarization/generation

---

## 2. Development Roadmap

### Phase 1: Backend Development
- **Flask App:** Central controller (`app.py`)
- **Authentication:** Role-based (`login.py`)
- **Database:**  
    - Tables: users, courses, enrollments, materials, assignments, feedback, progress  
    - ORM: SQLAlchemy/Flask-SQLAlchemy
- **Modules:**  
    - User management (`user.py`, `admin.py`, `instructor.py`, `student.py`)  
    - Course/materials (`course.py`, `learning-material.py`)  
    - Assignments/feedback (`assignment.py`, `feedback.py`)  
    - System utilities (`system.py`)
- **Security:** Secure password handling (e.g., Flask-Bcrypt)

### Phase 2: Frontend Development
- **Templates:** Responsive HTML (Bootstrap), role-based dashboards
- **Static Assets:** CSS, JS for interactivity
- **API Integration:** REST APIs for AJAX/frontend-backend communication

### Phase 3: AI-Powered Features
- **LLM Integration:**  
    - Open-source/free-tier LLMs (e.g., Hugging Face, OpenAI)  
    - Chatbot, AI grading, content generation
- **Deployment:** Cloud hosting for LLM APIs

### Phase 4: Testing & Deployment
- **Testing:** Unit/integration tests, beta feedback
- **Deployment:**  
    - Cloud hosting (AWS, Azure, Heroku)  
    - Reverse proxy (Nginx/Apache)  
    - SSL for security

---

## 3. Example Workflow Implementation

| Step                | Action                                                                                  |
|---------------------|----------------------------------------------------------------------------------------|
| **User Login**      | Student logs in → Authenticated (`login.py`) → Redirected to dashboard                 |
| **Course Enrollment** | Student views courses (`course.py`) → Enrolls → Enrollment stored in DB                |
| **Assignment Submission** | Student uploads assignment (`assignment.py`) → File stored, marked pending review     |
| **Feedback**        | Instructor reviews/provides feedback (`feedback.py`) → Student views feedback           |
| **AI Assistance**   | Student asks chatbot → LLM processes → Returns response                                 |

---

## 4. Future Enhancements

- Gamification (badges, leaderboards)
- Offline support (PWA)
- Live virtual classrooms (video conferencing APIs)
