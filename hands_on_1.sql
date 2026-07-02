-- Hands-On 1: Schema Design & Core SQL

-- Task 1: Create the Database and Tables

CREATE DATABASE IF NOT EXISTS college_db;
USE college_db;

CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);

CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    department_id INT,
    enrollment_year INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    grade CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE professors (
    professor_id INT PRIMARY KEY AUTO_INCREMENT,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);


-- Task 2: Normalisation Analysis

-- 1NF: Every column in all tables stores a single atomic value.
--       For example, the tags or phone numbers are not bundled into one field.
--       Each row in students, courses, enrollments, etc. is uniquely identifiable.

-- 2NF: All non-key columns depend on the full primary key.
--       In enrollments, the candidate key is (student_id, course_id).
--       The grade column depends on both student_id and course_id together, not just one.
--       enrollment_date also depends on the full key (when a student joined a specific course).
--       No partial dependencies exist.

-- 3NF: No transitive dependencies are present.
--       For example, dept_name is stored only in departments, not in students.
--       If dept_name were in students, it would depend on department_id, not directly on student_id.
--       That would be a transitive dependency: student_id -> department_id -> dept_name.
--       By keeping dept_name in its own table, we satisfy 3NF throughout the schema.


-- Task 3: Alter and Extend the Schema

-- Step 1: Add phone_number to students
ALTER TABLE students ADD COLUMN phone_number VARCHAR(15);

-- Step 2: Add max_seats to courses
ALTER TABLE courses ADD COLUMN max_seats INT DEFAULT 60;

-- Step 3: Add CHECK constraint on grade in enrollments
ALTER TABLE enrollments ADD CONSTRAINT chk_grade CHECK (grade IN ('A','B','C','D','F') OR grade IS NULL);

-- Step 4: Rename hod_name to head_of_dept in departments
-- MySQL syntax:
ALTER TABLE departments CHANGE hod_name head_of_dept VARCHAR(100);
-- PostgreSQL syntax (comment out whichever doesn't apply):
-- ALTER TABLE departments RENAME COLUMN hod_name TO head_of_dept;

-- Step 5: Drop phone_number column (rollback)
ALTER TABLE students DROP COLUMN phone_number;
