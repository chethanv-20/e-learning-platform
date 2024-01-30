from database import connect_to_database
import traceback

def buy_course(student_id, course_id, amount):
    db = connect_to_database()
    cursor = db.cursor()

    try:
        # Check if the student has already bought the course
        check_query = "SELECT * FROM progress WHERE student_id = %s AND course_id = %s"
        cursor.execute(check_query, (student_id, course_id))
        existing_progress = cursor.fetchone()

        if existing_progress:
            return f"Student has already bought this course."

        # If not, add progress and update payment table
        progress_query = "INSERT INTO progress (student_id, course_id, percentage_completed) VALUES (%s, %s, 0)"
        cursor.execute(progress_query, (student_id, course_id))

        payment_query = "INSERT INTO payment (student_id, amount, payment_date) VALUES (%s, %s, NOW())"
        cursor.execute(payment_query, (student_id, amount))

        db.commit()
        return f"Course bought successfully!"

    except Exception as e:
        db.rollback()
        return f"Error buying course: {str(e)}"

    finally:
        db.close()
        
def get_available_courses():
    db = connect_to_database()
    cursor = db.cursor()

    try:
        # Fetch all available courses
        query = "SELECT * FROM course"
        cursor.execute(query)
        courses = cursor.fetchall()

        return courses

    except Exception as e:
        return []

    finally:
        db.close()

def get_courses_by_domain(teacher_id):
    db = connect_to_database()
    cursor = db.cursor()

    try:
        # Fetch domain_id based on teacher_id
        query_domain = "SELECT domain_id FROM teacher WHERE teacher_id = %s"
        cursor.execute(query_domain, (teacher_id,))
        domain_id = cursor.fetchone()[0]

        # Fetch courses based on domain_id
        query_courses = "SELECT * FROM course WHERE domain_id = %s"
        cursor.execute(query_courses, (domain_id,))
        courses = cursor.fetchall()

        return courses

    except Exception as e:
        return []

    finally:
        db.close()

def delete_course(course_id, teacher_id):
    db = connect_to_database()
    cursor = db.cursor()

    try:
        # Fetch the domain_id associated with the teacher
        query_domain = "SELECT domain_id FROM teacher WHERE teacher_id = %s"
        cursor.execute(query_domain, (teacher_id,))
        domain_id = cursor.fetchone()

        if not domain_id:
            return "Teacher not found."

        # Check if the course is associated with the teacher's domain
        check_association_query = "SELECT * FROM course WHERE course_id = %s AND domain_id = %s"
        cursor.execute(check_association_query, (course_id, domain_id[0]))
        association_exists = cursor.fetchone()

        if association_exists:
            # Delete the course from the course table
            delete_course_query = "DELETE FROM course WHERE course_id = %s"
            cursor.execute(delete_course_query, (course_id,))

            db.commit()
            return "Course deleted successfully!"

        else:
            return "Course is not associated with the teacher's domain."

    except Exception as e:
        db.rollback()
        return f"Error deleting course: {str(e)}"

    finally:
        db.close()

