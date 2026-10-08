import json
import os
from datetime import datetime


DATA_FILE = "students.json"




def load_students():
    """Load students from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_students(students):
    """Save students to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)




def generate_id(students):
    """Generate a unique student ID."""
    if not students:
        return 1

    return max(student["id"] for student in students) + 1


def calculate_average(grades):
    """Calculate the average grade."""
    if not grades:
        return 0

    return sum(grades.values()) / len(grades)


def get_status(average):
    """Return the student's academic status."""
    if average >= 90:
        return "Excellent"
    elif average >= 75:
        return "Very Good"
    elif average >= 50:
        return "Pass"
    else:
        return "Fail"




def add_student(students):
    print("\n--- Add Student ---")

    name = input("Enter student name: ").strip()
    age = input("Enter age: ").strip()
    department = input("Enter department: ").strip()

    if not name or not age or not department:
        print("All fields are required.")
        return

    try:
        age = int(age)
    except ValueError:
        print("Age must be a number.")
        return

    student = {
        "id": generate_id(students),
        "name": name,
        "age": age,
        "department": department,
        "grades": {},
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    students.append(student)
    save_students(students)

    print(f"\nStudent '{name}' added successfully.")
    print(f"Student ID: {student['id']}")


def list_students(students):
    print("\n--- Student List ---")

    if not students:
        print("No students found.")
        return

    for student in students:
        average = calculate_average(student["grades"])
        status = get_status(average)

        print(
            f"ID: {student['id']} | "
            f"Name: {student['name']} | "
            f"Age: {student['age']} | "
            f"Department: {student['department']} | "
            f"Average: {average:.2f} | "
            f"Status: {status}"
        )


def search_student(students):
    print("\n--- Search Student ---")

    keyword = input("Enter student name or ID: ").strip().lower()

    found = []

    for student in students:
        if (
            keyword in student["name"].lower()
            or keyword == str(student["id"])
        ):
            found.append(student)

    if not found:
        print("No matching students found.")
        return

    for student in found:
        average = calculate_average(student["grades"])

        print("\nStudent found:")
        print(f"ID: {student['id']}")
        print(f"Name: {student['name']}")
        print(f"Age: {student['age']}")
        print(f"Department: {student['department']}")
        print(f"Grades: {student['grades']}")
        print(f"Average: {average:.2f}")
        print(f"Status: {get_status(average)}")


def add_grade(students):
    print("\n--- Add Grade ---")

    student_id = input("Enter student ID: ").strip()

    try:
        student_id = int(student_id)
    except ValueError:
        print("Invalid student ID.")
        return

    student = None

    for item in students:
        if item["id"] == student_id:
            student = item
            break

    if student is None:
        print("Student not found.")
        return

    subject = input("Enter subject: ").strip()

    if not subject:
        print("Subject cannot be empty.")
        return

    try:
        grade = float(input("Enter grade (0-100): "))
    except ValueError:
        print("Grade must be a number.")
        return

    if grade < 0 or grade > 100:
        print("Grade must be between 0 and 100.")
        return

    student["grades"][subject] = grade
    save_students(students)

    print(f"Grade added for {student['name']}.")


def delete_student(students):
    print("\n--- Delete Student ---")

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Invalid student ID.")
        return

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            save_students(students)

            print(f"Student '{student['name']}' deleted.")
            return

    print("Student not found.")


def show_student_statistics(students):
    print("\n--- Statistics ---")

    if not students:
        print("No students available.")
        return

    total_students = len(students)

    averages = []

    for student in students:
        average = calculate_average(student["grades"])

        if student["grades"]:
            averages.append(average)

    print(f"Total students: {total_students}")

    if averages:
        overall_average = sum(averages) / len(averages)

        highest = max(averages)
        lowest = min(averages)

        print(f"Overall average: {overall_average:.2f}")
        print(f"Highest average: {highest:.2f}")
        print(f"Lowest average: {lowest:.2f}")
    else:
        print("No grades have been entered yet.")



def display_menu():
    print("\n")
    print("=" * 40)
    print("       STUDENT MANAGEMENT SYSTEM")
    print("=" * 40)

    print("1. Add student")
    print("2. List students")
    print("3. Search student")
    print("4. Add grade")
    print("5. Delete student")
    print("6. Show statistics")
    print("7. Exit")

    print("=" * 40)




def main():
    students = load_students()

  print("\nWelcome to Mira Student Management System!")

    while True:
        display_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student(students)

        elif choice == "2":
            list_students(students)

        elif choice == "3":
            search_student(students)

        elif choice == "4":
            add_grade(students)

        elif choice == "5":
            delete_student(students)

        elif choice == "6":
            show_student_statistics(students)

        elif choice == "7":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()