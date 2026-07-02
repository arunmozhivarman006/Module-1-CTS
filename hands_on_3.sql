-- Hands-On 3: Advanced SQL - Subqueries, Views & Transactions

USE college_db;

-- -------------------------------------------------------
-- Task 1: Subqueries
-- -------------------------------------------------------

-- Step 1: Students enrolled in more courses than the average
SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS full_name,
       COUNT(e.course_id) AS course_count
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.course_id) > (
    SELECT AVG(enrollment_count)
    FROM (
        SELECT COUNT(course_id) AS enrollment_count
        FROM enrollments
        GROUP BY student_id
    ) AS avg_table
);

-- Step 2: Courses where all enrolled students received grade 'A'
SELECT c.course_id, c.course_name
FROM courses c
WHERE c.course_id IN (
    SELECT e.course_id
    FROM enrollments e
    GROUP BY e.course_id
    HAVING SUM(CASE WHEN e.grade != 'A' THEN 1 ELSE 0 END) = 0
);

-- Step 3: Professor with highest salary in each department (correlated subquery)
SELECT p.prof_name, p.department_id, p.salary
FROM professors p
WHERE p.salary = (
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p.department_id
);

-- Step 4: Departments where average professor salary exceeds 85000 (derived table)
SELECT dept_avg.dept_name, dept_avg.avg_salary
FROM (
    SELECT d.dept_name, ROUND(AVG(p.salary), 2) AS avg_salary
    FROM departments d
    JOIN professors p ON d.department_id = p.department_id
    GROUP BY d.department_id, d.dept_name
) AS dept_avg
WHERE dept_avg.avg_salary > 85000;


-- -------------------------------------------------------
-- Task 2: Creating and Using Views
-- -------------------------------------------------------

-- Step 1: View - student enrollment summary with GPA
CREATE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
    d.dept_name AS department,
    COUNT(e.course_id) AS courses_enrolled,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ), 2) AS gpa
FROM students s
LEFT JOIN departments d ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

-- Step 2: View - course statistics
CREATE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ), 2) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

-- Step 3: Query students with GPA above 3.0
SELECT * FROM vw_student_enrollment_summary
WHERE gpa > 3.0
ORDER BY gpa DESC;

-- Step 4: Attempting UPDATE on multi-table view
-- UPDATE vw_student_enrollment_summary SET department = 'Electronics' WHERE student_id = 1;
-- ERROR: The target table vw_student_enrollment_summary of the UPDATE is not updatable.
-- Multi-table views (joins + aggregations) are not updatable because MySQL/PostgreSQL cannot
-- determine which base table row to modify. Views based on a single table with no aggregation
-- can be updatable, but views with GROUP BY, JOINs, or aggregate functions are read-only.

-- Step 5: Drop and recreate with WITH CHECK OPTION (single-table view example)
DROP VIEW IF EXISTS vw_student_enrollment_summary;
DROP VIEW IF EXISTS vw_course_stats;

CREATE VIEW vw_cs_students AS
SELECT student_id, first_name, last_name, email, enrollment_year, department_id
FROM students
WHERE department_id = 1
WITH CHECK OPTION;
-- WITH CHECK OPTION ensures any INSERT/UPDATE through this view is rejected
-- if the resulting row would not be visible through the view's WHERE clause.
-- Example: trying to UPDATE department_id to 2 through this view would fail.

-- Recreate the original views after the drop
CREATE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
    d.dept_name AS department,
    COUNT(e.course_id) AS courses_enrolled,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ), 2) AS gpa
FROM students s
LEFT JOIN departments d ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

CREATE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ), 2) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;


-- -------------------------------------------------------
-- Task 3: Stored Procedures and Transactions
-- -------------------------------------------------------

-- Step 1: Stored procedure to enroll a student (MySQL)
DELIMITER $$

CREATE PROCEDURE sp_enroll_student(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_enrollment_date DATE
)
BEGIN
    IF EXISTS (
        SELECT 1 FROM enrollments
        WHERE student_id = p_student_id AND course_id = p_course_id
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Student is already enrolled in this course.';
    ELSE
        INSERT INTO enrollments (student_id, course_id, enrollment_date)
        VALUES (p_student_id, p_course_id, p_enrollment_date);
        SELECT 'Enrollment successful.' AS message;
    END IF;
END$$

DELIMITER ;

-- Test sp_enroll_student
CALL sp_enroll_student(1, 3, '2022-07-01');
-- Calling again with same values should raise: 'Student is already enrolled in this course.'
-- CALL sp_enroll_student(1, 3, '2022-07-01');


-- Step 2: Create log table and transfer procedure
CREATE TABLE IF NOT EXISTS department_transfer_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    old_department_id INT,
    new_department_id INT,
    transfer_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

CREATE PROCEDURE sp_transfer_student(
    IN p_student_id INT,
    IN p_new_dept_id INT
)
BEGIN
    DECLARE v_old_dept_id INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Transfer failed. Transaction rolled back.';
    END;

    START TRANSACTION;

    SELECT department_id INTO v_old_dept_id
    FROM students WHERE student_id = p_student_id;

    UPDATE students
    SET department_id = p_new_dept_id
    WHERE student_id = p_student_id;

    INSERT INTO department_transfer_log (student_id, old_department_id, new_department_id)
    VALUES (p_student_id, v_old_dept_id, p_new_dept_id);

    COMMIT;
    SELECT 'Transfer completed successfully.' AS message;
END$$

DELIMITER ;

-- Test sp_transfer_student
CALL sp_transfer_student(2, 3);
-- To test rollback, pass an invalid dept_id like 999 (FK violation triggers rollback):
-- CALL sp_transfer_student(2, 999);


-- Step 3: SAVEPOINT demonstration
START TRANSACTION;

INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
VALUES (3, 2, '2024-01-01', 'B');

SAVEPOINT after_first_insert;

-- Second insert deliberately uses an invalid course_id to simulate failure
-- INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
-- VALUES (3, 999, '2024-01-01', 'A');
-- If the above fails, roll back to savepoint — first insert is preserved:
ROLLBACK TO SAVEPOINT after_first_insert;

COMMIT;

-- Verify only the first enrollment was saved
SELECT * FROM enrollments WHERE student_id = 3;
