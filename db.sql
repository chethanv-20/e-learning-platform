-- Create the database
CREATE DATABASE IF NOT EXISTS ol_db;

-- Use the database
USE ol_db;

-- Create the domain table
CREATE TABLE domain (
    domain_id INT auto_increment PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Create the course table
CREATE TABLE course (
    course_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    domain_id INT,
    FOREIGN KEY (domain_id) REFERENCES domain(domain_id)
);

-- Create the teacher table
CREATE TABLE teacher (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    contact_info VARCHAR(255),
    specialization VARCHAR(255),
    domain_id int ,
    password VARCHAR(255) NOT NULL
    
);


-- Create the student table
CREATE TABLE student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    contact_info VARCHAR(255),
    password VARCHAR(255) NOT NULL
);
-- Create the progress table
CREATE TABLE progress (
    progress_id INT PRIMARY KEY,
    student_id INT,
    course_id INT,
    percentage_completed DECIMAL(5,2),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

-- Create the resources table
CREATE TABLE resources (
    resource_id INT PRIMARY KEY,
    course_id INT,
    title VARCHAR(255),
    type VARCHAR(50),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

-- Create the payment table
CREATE TABLE payment (
    payment_id INT PRIMARY KEY,
    student_id INT,
    amount DECIMAL(10,2),
    payment_date DATE,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);