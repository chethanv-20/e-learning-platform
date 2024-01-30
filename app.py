# app.py
import streamlit as st
from PIL import Image
from student import login_student, edit_student_name, get_student_profile, create_student_account,get_all_courses
from teacher import login_teacher, get_teacher_profile, delete_course_by_teacher, get_courses_by_teacher,create_teacher_account,get_all_domains,buy_course

def initialize_state():
    return {
        "user_type": None,
        "login_or_create": None,
        "username": None,
        "password": None,
        "new_name": None,
        "new_contact_info": None,
        "selected_course_id": None,
    }

def display_student_profile(profile_data):
    st.subheader("Student Profile:")
    st.write("Name:", profile_data[0][1])
    st.write("Contact Info:", profile_data[0][2])
    st.write("Courses Bought:")
    for row in profile_data:
        st.write(f"- {row[5]}: {row[6]}% completed")

    # Display available courses for purchase
    st.subheader("Available Courses:")
    available_courses = get_all_courses()
    for course in available_courses:
        st.write(f"- Course ID: {course[0]}, Name: {course[1]}")

    # Option to buy a course
    selected_course_id = st.text_input("Enter the Course ID to buy:")
    buy_course_button = st.button("Buy Course")

    if buy_course_button and selected_course_id:
        # Assuming you have a function to handle course purchase
        purchase_result = buy_course(profile_data[0][0], selected_course_id)
        st.success(purchase_result)
def display_teacher_profile_with_delete_dropdown(profile_data):
    st.subheader("Teacher Profile:")
    st.write("Name:", profile_data[0][1])
    st.write("Contact Info:", profile_data[0][2])
    st.write("Specialization:", profile_data[0][3])

    st.subheader("Courses Taught:")

    # Fetch courses under the teacher's domain

    teacher_id = profile_data[0][0]
    courses_under_teacher = get_courses_by_teacher(teacher_id)

    if courses_under_teacher:
        st.write("Courses Taught:")
        for course in courses_under_teacher:
            st.write(f"- {course[0]} - {course[1]}")
    else:
        st.write("No courses found for this teacher.")



    st.header("Delete Course needs conformation in CMD!(please give course id in cmd)")
    print("Enter Course Id  to delete: ")
    selected_course_key = int(input())

    x = int(input())
        # Check if the checkbox is selected and the "Delete Course" button is clicked
    if (x==1):
            print("course id you deleted was sucessfully deleted sucessfully deleted")
            course_id_to_delete = selected_course_key
            # Delete the course
            delete_result = delete_course_by_teacher(course_id_to_delete)
            st.success(delete_result)
    else:
            st.warning("Please confirm the deletion by checking the checkbox.")




def delete_course_callback(course):
    teacher_id = course[0]
    course_id = course[4]
    delete_result = delete_course_by_teacher(course_id, teacher_id)
    st.success(delete_result)


def main():
    global state
    st.header('ONLINE LEARNING PLATFORM', divider='rainbow')
    # image = Image.open('e-learning-image.jpg')
    # st.image(image, caption=None, width=400)
    video_file = open('online.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    state = initialize_state()

    state["user_type"] = st.sidebar.radio("User Type", ("Student", "Teacher"))
    state["login_or_create"] = st.sidebar.radio("Login or Create Account", ("Login", "Create Account"))

    if state["login_or_create"] == "Login":
        state["username"] = st.text_input("Username:")
        state["password"] = st.text_input("Password:", type="password")

        if st.button("Login"):
            if not state["username"] or not state["password"]:
                st.warning("Please enter both username and password.")
            else:
                if state["user_type"] == "Student":
                    student = login_student(state["username"], state["password"])
                    if student:
                        st.success("Login Successful! Welcome, {}".format(student[1]))

                        # Display student profile
                        student_id = student[0]
                        profile_data = get_student_profile(student_id)
                        display_student_profile(profile_data)

                        # Option to edit profile details
                        st.subheader("Edit Profile Details in cmd!")
                        print("enter new name to update and type confirm to confirm : ")
                        new_name_ = input()
                        y =input()
                        if y == "confirm" and new_name_:
                            print("yes")
                            # Update the student name
                            update_result = edit_student_name(student_id, new_name_)
                            st.success(update_result)

                            # Display the updated student profile
                            st.subheader("Updated Student Profile:")
                            updated_profile_data = get_student_profile(student_id)
                            display_student_profile(updated_profile_data)

                        # Other student-related functionality...

                    else:
                        st.error("Invalid username or password.")

                elif state["user_type"] == "Teacher":
                    teacher = login_teacher(state["username"], state["password"])
                    if teacher:
                        st.success("Login Successful! Welcome, {}".format(teacher[1]))

                        # Display teacher profile
                        teacher_id = teacher[0]
                        profile_data = get_teacher_profile(teacher_id)
                        display_teacher_profile_with_delete_dropdown(profile_data)

                    else:
                        st.error("Invalid username or password.")

    elif state["login_or_create"] == "Create Account":
        if state["user_type"] == "Student":
            st.subheader("Create Student Account")
            state["new_name"] = st.text_input("Name:")
            state["new_contact_info"] = st.text_input("Contact Info:")
            state["password"] = st.text_input("Password:", type="password")

            if st.button("Create Account") and state["new_name"] and state["new_contact_info"] and state["password"]:
                result = create_student_account(state["new_name"], state["new_contact_info"], state["password"])
                st.success(result)

        elif state["user_type"] == "Teacher":
            st.subheader("Create Teacher Account")
            state["new_name"] = st.text_input("Name:")
            state["new_contact_info"] = st.text_input("Contact Info:")
            state["specialization"] = st.text_input("Specialization:")
            state["password"] = st.text_input("Password:", type="password")

            # Add domain selection for the teacher
            domains = get_all_domains()
            domain_names = [domain[1] for domain in domains]
            state["selected_domain"] = st.selectbox("Select a domain for the teacher:", domain_names)

            if st.button("Create Account") and state["new_name"] and state["new_contact_info"] and state["specialization"] and state["password"]:
                result = create_teacher_account(state["new_name"], state["new_contact_info"],
                                                state["specialization"], state["password"], state["selected_domain"])
                st.success(result)

if __name__ == "__main__":
    main()
