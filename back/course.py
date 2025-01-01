from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from sqlalchemy.orm import joinedload
from back.system_utilities.dbmanage import get_db, Course, Enrollment
from back.system_utilities.user import login_required

course_bp = Blueprint('course', __name__)

@course_bp.route('/create_course', methods=['POST'])
@login_required
def create_course():
    if session['user_type'] != 'instructor':
        flash('Only instructors can create courses.', 'warning')
        return redirect(url_for('course.courses'))
    
    course_name = request.form['course_name']
    instructor_id = session['user_id']
    
    db = next(get_db())
    new_course = Course(name=course_name, instructor_id=instructor_id)
    db.add(new_course)
    db.commit()
    db.close()
    
    flash('Course created successfully!', 'success')
    return redirect(url_for('course.courses'))

@course_bp.route('/request_course', methods=['POST'])
@login_required
def request_course():
    if session['user_type'] != 'student':
        flash('Only students can request enrollment.', 'warning')
        return redirect(url_for('course.courses'))
    
    course_id = request.form['course_id']
    student_id = session['user_id']
    
    db = next(get_db())
    new_enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.add(new_enrollment)
    db.commit()
    db.close()
    
    flash('Enrollment request sent!', 'success')
    return redirect(url_for('course.courses'))

@course_bp.route('/approve_enrollment/<int:enrollment_id>', methods=['POST'])
@login_required
def approve_enrollment(enrollment_id):
    if session['user_type'] != 'instructor':
        flash('Only instructors can approve enrollments.', 'warning')
        return redirect(url_for('course.courses'))
    
    db = next(get_db())
    enrollment = db.query(Enrollment).options(joinedload(Enrollment.student)).filter(Enrollment.id == enrollment_id).first()
    if enrollment and enrollment.course.instructor_id == session['user_id']:
        enrollment.status = 'approved'
        db.commit()
        flash('Enrollment approved!', 'success')
    else:
        flash('Enrollment not found or not authorized.', 'danger')
    db.close()
    
    return redirect(url_for('course.courses'))

@course_bp.route('/courses')
@login_required
def courses():
    db = next(get_db())
    user_id = session.get('user_id')
    user_type = session.get('user_type', 'guest')
    
    if user_type == 'instructor':
        courses = db.query(Course).options(joinedload(Course.instructor), joinedload(Course.enrollments).joinedload(Enrollment.student)).filter(Course.instructor_id == user_id).all()
    else:
        courses = db.query(Course).options(joinedload(Course.instructor), joinedload(Course.enrollments).joinedload(Enrollment.student)).all()
    
    available_courses = db.query(Course).options(joinedload(Course.instructor), joinedload(Course.enrollments).joinedload(Enrollment.student)).all()
    db.close()
    
    return render_template('courses.html', courses=courses, available_courses=available_courses, user_type=user_type)

@course_bp.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    db = next(get_db())
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if request.method == 'POST':
        if session['user_type'] != 'instructor':
            flash('Only instructors can edit courses.', 'warning')
            return redirect(url_for('course.courses'))
        
        course.name = request.form['course_name']
        db.commit()
        db.close()
        
        flash('Course updated successfully!', 'success')
        return redirect(url_for('course.courses'))
    
    db.close()
    return render_template('edit_course.html', course=course)

@course_bp.route('/delete_course/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    if session['user_type'] != 'instructor':
        flash('Only instructors can delete courses.', 'warning')
        return redirect(url_for('course.courses'))
    
    db = next(get_db())
    course = db.query(Course).filter(Course.id == course_id).first()
    if course:
        db.delete(course)
        db.commit()
        flash('Course deleted successfully!', 'success')
    else:
        flash('Course not found.', 'danger')
    db.close()
    
    return redirect(url_for('course.courses'))