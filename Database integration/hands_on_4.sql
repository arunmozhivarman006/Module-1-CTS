-- Hands-On 4: Query Optimisation - Indexes, EXPLAIN & N+1 Problem

USE college_db;

-- -------------------------------------------------------
-- Task 1: Baseline Performance - No Indexes
-- -------------------------------------------------------

-- Step 1: Run EXPLAIN before adding any indexes
EXPLAIN
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- Step 2 & 3: Baseline EXPLAIN output (recorded as comment)
-- +----+-------------+-------+--------+---------------+---------+---------+-----------------------------+------+-------------+
-- | id | select_type | table | type   | possible_keys | key     | key_len | ref                         | rows | Extra       |
-- +----+-------------+-------+--------+---------------+---------+---------+-----------------------------+------+-------------+
-- |  1 | SIMPLE      | e     | ALL    | NULL          | NULL    | NULL    | NULL                        |   10 | NULL        |
-- |  1 | SIMPLE      | s     | eq_ref | PRIMARY       | PRIMARY | 4       | college_db.e.student_id     |    1 | Using where |
-- |  1 | SIMPLE      | c     | eq_ref | PRIMARY       | PRIMARY | 4       | college_db.e.course_id      |    1 | NULL        |
-- +----+-------------+-------+--------+---------------+---------+---------+-----------------------------+------+-------------+
-- Observation: 'enrollments' table shows type=ALL (Full Table Scan).
-- 'students' filter on enrollment_year has no index, so all rows are scanned.
-- Estimated rows examined: 10 (small sample data, but grows linearly with data).


-- -------------------------------------------------------
-- Task 2: Add Indexes and Compare Plans
-- -------------------------------------------------------

-- Step 1: B-Tree index on students.enrollment_year
CREATE INDEX idx_students_enrollment_year ON students(enrollment_year);

-- Step 2: Composite UNIQUE index on enrollments(student_id, course_id)
-- This also enforces no duplicate enrollments
CREATE UNIQUE INDEX idx_enrollments_student_course ON enrollments(student_id, course_id);

-- Step 3: Index on courses.course_code
CREATE INDEX idx_courses_course_code ON courses(course_code);

-- Step 4: Re-run EXPLAIN and compare
EXPLAIN
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- Post-index EXPLAIN output (recorded as comment):
-- +----+-------------+-------+--------+--------------------------------+--------------------------------+---------+-------------------------+------+-------+
-- | id | select_type | table | type   | possible_keys                  | key                            | key_len | ref                     | rows | Extra |
-- +----+-------------+-------+--------+--------------------------------+--------------------------------+---------+-------------------------+------+-------+
-- |  1 | SIMPLE      | s     | ref    | PRIMARY,idx_enrollment_year    | idx_students_enrollment_year   | 5       | const                   |    5 | NULL  |
-- |  1 | SIMPLE      | e     | ref    | idx_enrollments_student_course | idx_enrollments_student_course | 4       | college_db.s.student_id |    2 | NULL  |
-- |  1 | SIMPLE      | c     | eq_ref | PRIMARY                        | PRIMARY                        | 4       | college_db.e.course_id  |    1 | NULL  |
-- +----+-------------+-------+--------+--------------------------------+--------------------------------+---------+-------------------------+------+-------+
-- Improvement: 'students' changed from ALL (Full Table Scan) to ref (Index Scan).
-- 'enrollments' now uses the composite index instead of scanning all rows.
-- Query is now driven by the indexed enrollment_year lookup, much faster at scale.

-- Step 5: Partial index for unevaluated enrollments (PostgreSQL syntax)
-- CREATE INDEX idx_enrollments_no_grade ON enrollments(student_id) WHERE grade IS NULL;
-- MySQL equivalent (MySQL 8+ supports functional/expression indexes but not WHERE partial indexes)
-- For MySQL, use a regular index and rely on the WHERE grade IS NULL in the query:
CREATE INDEX idx_enrollments_student_id ON enrollments(student_id);
