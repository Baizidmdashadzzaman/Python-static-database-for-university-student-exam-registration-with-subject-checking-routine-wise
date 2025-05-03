from datetime import datetime

students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
]

semesters = [
    {"id": 1, "name": "Spring 2025"},
    {"id": 2, "name": "Fall 2025"},
]

subjects = [
    {"id": 1, "code": "CSE101", "name": "Introduction to Programming"},
    {"id": 2, "code": "MAT101", "name": "Calculus I"},
    {"id": 3, "code": "PHY101", "name": "Physics I"},
    {"id": 4, "code": "CSE201", "name": "Data Structures"},
    {"id": 5, "code": "MAT201", "name": "Linear Algebra"},
]

registrations = [
    {"student_id": 1, "semester_id": 1},
    {"student_id": 2, "semester_id": 1},
    {"student_id": 3, "semester_id": 2},
]

enrollments = [
    {"student_id": 1, "semester_id": 1, "subject_ids": [1, 2, 3]},
    {"student_id": 2, "semester_id": 1, "subject_ids": [2, 3]},
    {"student_id": 3, "semester_id": 2, "subject_ids": [4, 5]},
]


exam_routines = [
    {"semester_id": 1, "subject_id": 1, "date": "2025-05-10"},
    {"semester_id": 1, "subject_id": 2, "date": "2025-05-12"},
    {"semester_id": 1, "subject_id": 3, "date": "2025-05-14"},
    {"semester_id": 2, "subject_id": 4, "date": "2025-06-01"},
    {"semester_id": 2, "subject_id": 5, "date": "2025-06-03"},
]


def display_data():
    print("Students:")
    for s in students:
        print(f"  ID: {s['id']}, Name: {s['name']}")

    print("\nSemesters:")
    for sem in semesters:
        print(f"  ID: {sem['id']}, Name: {sem['name']}")

    print("\nSubjects:")
    for subj in subjects:
        print(f"  ID: {subj['id']}, Code: {subj['code']}, Name: {subj['name']}")

    print("\nEnrollments:")
    for e in enrollments:
        student_name = next(s["name"] for s in students if s["id"] == e["student_id"])
        semester_name = next(sem["name"] for sem in semesters if sem["id"] == e["semester_id"])
        subject_names = [sub["name"] for sub in subjects if sub["id"] in e["subject_ids"]]
        print(f"  {student_name} -> {semester_name}: {', '.join(subject_names)}")

def get_student_exam_routine(student_id):
    student = next(s for s in students if s["id"] == student_id)
    enrollment = next(e for e in enrollments if e["student_id"] == student_id)
    semester_id = enrollment["semester_id"]
    subject_ids = enrollment["subject_ids"]

    routine = []
    for exam in exam_routines:
        if exam["semester_id"] == semester_id and exam["subject_id"] in subject_ids:
            subject = next(s for s in subjects if s["id"] == exam["subject_id"])
            routine.append({
                "subject": subject["name"],
                "code": subject["code"],
                "date": datetime.strptime(exam["date"], "%Y-%m-%d").strftime("%d-%b-%Y")
            })

    routine.sort(key=lambda x: x["date"])  # Sort by exam date
    return {"student": student["name"], "semester": semester_id, "routine": routine}

def display_all_routines():
    print("Student Exam Routines:\n")
    for student in students:
        info = get_student_exam_routine(student["id"])
        print(f"Student: {info['student']}")
        for r in info["routine"]:
            print(f"  {r['date']} - {r['code']}: {r['subject']}")
        print("")


def display_date_wise_exam_routine():
    print("Date-wise Exam Routine:\n")

    subject_lookup = {subj["id"]: subj for subj in subjects}
    student_lookup = {s["id"]: s["name"] for s in students}
    enrollment_lookup = {
        (e["student_id"], e["semester_id"]): e["subject_ids"]
        for e in enrollments
    }

    date_map = {}

    for exam in exam_routines:
        subject_id = exam["subject_id"]
        semester_id = exam["semester_id"]
        exam_date = datetime.strptime(exam["date"], "%Y-%m-%d").strftime("%d-%b-%Y")
        subject = subject_lookup[subject_id]

        if exam_date not in date_map:
            date_map[exam_date] = []

        students_in_exam = [
            student_lookup[student_id]
            for student_id, sem_id in enrollment_lookup.keys()
            if sem_id == semester_id and subject_id in enrollment_lookup[(student_id, sem_id)]
        ]

        date_map[exam_date].append({
            "subject_code": subject["code"],
            "subject_name": subject["name"],
            "students": students_in_exam
        })


    for date in sorted(date_map):
        print(f"Date: {date}")
        for entry in date_map[date]:
            print(f"  {entry['subject_code']} - {entry['subject_name']}")
            print(f"    Students: {', '.join(entry['students'])}")
        print("")


display_date_wise_exam_routine()
