// Hands-On 5: MongoDB - Document Modelling, CRUD & Aggregation
// Run these commands in mongosh or MongoDB Compass shell

// -------------------------------------------------------
// Task 1: Create Collection and Insert Documents
// -------------------------------------------------------

// Step 1: Switch to college_nosql database
use college_nosql

// Step 2 & 3: Create feedback collection and insert 10+ documents
db.feedback.insertMany([
  {
    student_id: 1,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "The course was very well structured. Concepts were explained clearly.",
    tags: ["challenging", "well-structured", "good-examples"],
    submitted_at: ISODate("2022-11-30T10:15:00Z"),
    attachments: [{ filename: "notes.pdf", size_kb: 240 }]
  },
  {
    student_id: 2,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 4,
    comments: "Good teaching style. Assignments were helpful.",
    tags: ["challenging", "practical", "good-examples"],
    submitted_at: ISODate("2022-11-28T09:00:00Z"),
    attachments: [{ filename: "assignment1.pdf", size_kb: 120 }]
  },
  {
    student_id: 5,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 3,
    comments: "Content was okay but could use more real-world examples.",
    tags: ["average", "needs-improvement"],
    submitted_at: ISODate("2022-11-29T11:30:00Z"),
    attachments: [{ filename: "notes2.pdf", size_kb: 95 }]
  },
  {
    student_id: 1,
    course_code: "CS102",
    semester: "2022-ODD",
    rating: 5,
    comments: "Loved the database design sessions. Very practical.",
    tags: ["well-structured", "practical", "insightful"],
    submitted_at: ISODate("2022-12-01T14:00:00Z"),
    attachments: [{ filename: "db_notes.pdf", size_kb: 310 }]
  },
  {
    student_id: 5,
    course_code: "CS102",
    semester: "2022-ODD",
    rating: 4,
    comments: "Queries section was really useful. Good pace.",
    tags: ["practical", "good-examples"],
    submitted_at: ISODate("2022-12-02T10:45:00Z"),
    attachments: [{ filename: "query_notes.pdf", size_kb: 180 }]
  },
  {
    student_id: 3,
    course_code: "EC101",
    semester: "2021-ODD",
    rating: 2,
    comments: "Too theoretical. Needed more lab sessions.",
    tags: ["theoretical", "needs-improvement"],
    submitted_at: ISODate("2021-11-20T08:30:00Z"),
    attachments: [{ filename: "ec_notes.pdf", size_kb: 75 }]
  },
  {
    student_id: 6,
    course_code: "EC101",
    semester: "2021-EVEN",
    rating: 1,
    comments: "Very hard to follow. Slides were not clear.",
    tags: ["confusing", "needs-improvement"],
    submitted_at: ISODate("2021-04-15T09:00:00Z"),
    attachments: [{ filename: "ec_summary.pdf", size_kb: 50 }]
  },
  {
    student_id: 8,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "Excellent content. Best course this semester.",
    tags: ["challenging", "well-structured", "insightful"],
    submitted_at: ISODate("2022-11-30T16:00:00Z")
    // Step 4: intentionally no attachments field - valid in MongoDB
  },
  {
    student_id: 2,
    course_code: "CS103",
    semester: "2022-ODD",
    rating: 4,
    comments: "OOP concepts were clearly demonstrated with good examples.",
    tags: ["practical", "good-examples", "well-structured"],
    submitted_at: ISODate("2022-12-03T13:00:00Z"),
    attachments: [{ filename: "oop_notes.pdf", size_kb: 200 }]
  },
  {
    student_id: 8,
    course_code: "CS103",
    semester: "2022-ODD",
    rating: 3,
    comments: "Decent course but pace was too fast at times.",
    tags: ["average", "challenging"],
    submitted_at: ISODate("2022-12-04T10:00:00Z"),
    attachments: [{ filename: "oop_summary.pdf", size_kb: 140 }]
  }
])

// Step 4: Verify insert count
db.feedback.countDocuments()
// Expected output: 10


// -------------------------------------------------------
// Task 2: CRUD Operations
// -------------------------------------------------------

// Step 1 - READ: All feedback with rating 5
db.feedback.find({ rating: 5 })

// Step 2 - READ: CS101 feedback with tag 'challenging'
db.feedback.find({
  course_code: "CS101",
  tags: "challenging"
})

// Step 3 - READ: Projection - only student_id, course_code, rating (exclude _id)
db.feedback.find(
  {},
  { student_id: 1, course_code: 1, rating: 1, _id: 0 }
)

// Step 4 - UPDATE: Add needs_review: true for rating < 3
db.feedback.updateMany(
  { rating: { $lt: 3 } },
  { $set: { needs_review: true } }
)

// Step 5 - UPDATE: Push 'reviewed' tag into needs_review documents
db.feedback.updateMany(
  { needs_review: true },
  { $push: { tags: "reviewed" } }
)

// Step 6 - DELETE: Remove all feedback from semester '2021-EVEN'
db.feedback.deleteMany({ semester: "2021-EVEN" })

// Verify remaining count after delete
db.feedback.countDocuments()
// Expected: 9 (one 2021-EVEN document deleted)


// -------------------------------------------------------
// Task 3: Aggregation Pipeline
// -------------------------------------------------------

// Step 1 & 2: Filter by semester, group by course, sort by avg rating
db.feedback.aggregate([
  // Stage 1: Filter to 2022-ODD semester
  { $match: { semester: "2022-ODD" } },

  // Stage 2: Group by course_code, calculate avg rating and total count
  {
    $group: {
      _id: "$course_code",
      avg_rating: { $avg: "$rating" },
      total_feedback: { $sum: 1 }
    }
  },

  // Stage 3: Sort by avg_rating descending
  { $sort: { avg_rating: -1 } },

  // Step 2 extension: Project to rename and round avg_rating
  {
    $project: {
      _id: 0,
      course_code: "$_id",
      average_rating: { $round: ["$avg_rating", 1] },
      total_feedback: 1
    }
  }
])

// Step 3: Tag frequency leaderboard using $unwind
db.feedback.aggregate([
  // Stage 1: Deconstruct tags array - each tag becomes a separate document
  { $unwind: "$tags" },

  // Stage 2: Group by tag and count occurrences
  {
    $group: {
      _id: "$tags",
      count: { $sum: 1 }
    }
  },

  // Stage 3: Sort by count descending
  { $sort: { count: -1 } },

  // Stage 4: Clean up output
  {
    $project: {
      _id: 0,
      tag: "$_id",
      count: 1
    }
  }
])

// Step 4: Create index on course_code and verify with explain
db.feedback.createIndex({ course_code: 1 })

// Verify index is used (look for IXSCAN instead of COLLSCAN in winningPlan)
db.feedback.find({ course_code: "CS101" }).explain("executionStats")
