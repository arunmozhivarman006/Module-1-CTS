"""
Hands-On 4 - Task 3: Identify and Fix the N+1 Problem
"""

import time
import mysql.connector

# DB connection config
config = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",  # replace with your password
    "database": "college_db"
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor(dictionary=True)


# ---------------------------------------------------
# VERSION 1: N+1 Problem
# ---------------------------------------------------
print("=" * 50)
print("VERSION 1: N+1 Approach")
print("=" * 50)

query_count = 0
start = time.time()

# Query 1: fetch all enrollments
cursor.execute("SELECT * FROM enrollments")
enrollments = cursor.fetchall()
query_count += 1

results_v1 = []
for row in enrollments:
    # 1 extra query per enrollment row to get student name
    cursor.execute(
        "SELECT first_name, last_name FROM students WHERE student_id = %s",
        (row["student_id"],)
    )
    student = cursor.fetchone()
    query_count += 1
    results_v1.append({
        "enrollment_id": row["enrollment_id"],
        "student_name": f"{student['first_name']} {student['last_name']}",
        "course_id": row["course_id"],
        "grade": row["grade"]
    })

end = time.time()

print(f"Total queries executed : {query_count}")
print(f"Time taken             : {round((end - start) * 1000, 2)} ms")
print(f"Rows returned          : {len(results_v1)}")
print()
for r in results_v1:
    print(f"  Enrollment {r['enrollment_id']} | {r['student_name']} | Course {r['course_id']} | Grade: {r['grade']}")


# ---------------------------------------------------
# VERSION 2: Fixed with a single JOIN query
# ---------------------------------------------------
print()
print("=" * 50)
print("VERSION 2: JOIN Approach (Fixed)")
print("=" * 50)

query_count_v2 = 0
start2 = time.time()

cursor.execute("""
    SELECT
        e.enrollment_id,
        CONCAT(s.first_name, ' ', s.last_name) AS student_name,
        c.course_name,
        e.grade
    FROM enrollments e
    JOIN students s ON e.student_id = s.student_id
    JOIN courses c ON e.course_id = c.course_id
""")
results_v2 = cursor.fetchall()
query_count_v2 += 1

end2 = time.time()

print(f"Total queries executed : {query_count_v2}")
print(f"Time taken             : {round((end2 - start2) * 1000, 2)} ms")
print(f"Rows returned          : {len(results_v2)}")
print()
for r in results_v2:
    print(f"  Enrollment {r['enrollment_id']} | {r['student_name']} | {r['course_name']} | Grade: {r['grade']}")


# ---------------------------------------------------
# Summary
# ---------------------------------------------------
print()
print("=" * 50)
print("COMPARISON SUMMARY")
print("=" * 50)
print(f"  N+1 version  : {len(enrollments) + 1} queries  (1 + {len(enrollments)} per-row lookups)")
print(f"  JOIN version : 1 query")
print()
# In production with 10,000 enrollments:
# N+1 version would issue 10,001 queries — 10,000 extra round-trips to the DB.
# JOIN version still issues just 1 query regardless of data size.
print("  With 10,000 enrollments in production:")
print("    N+1  -> 10,001 queries (severe performance bottleneck)")
print("    JOIN ->      1 query  (scales with no extra round-trips)")

cursor.close()
conn.close()
