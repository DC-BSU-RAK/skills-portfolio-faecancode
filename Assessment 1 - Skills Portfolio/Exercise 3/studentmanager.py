import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk #imports the Image and ImageTk modules from pil
import os

students = []

script_dir = os.path.dirname(os.path.abspath(__file__))  
image_path = os.path.join(script_dir, "students.png")   
data_path = os.path.join(script_dir, "studentMarks.txt") 

def load_students():
    global students
    students = []

    try:
        with open(data_path, "r") as file:
            lines = file.readlines()
            num_students = int(lines[0].strip())
            for line in lines[1:]:
                parts = line.strip().split(",")
                student_code = parts[0]
                student_name = parts[1]
                coursework = list(map(int, parts[2:5]))
                exam = int(parts[5])
                students.append({
                    "code": student_code,
                    "name": student_name,
                    "coursework": coursework,
                    "exam": exam
                })
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found:\n{data_path}")

def calculate_total(student):
    return sum(student["coursework"]) + student["exam"]

def calculate_percentage(student):
    return (calculate_total(student) / 160) * 100

def calculate_grade(percentage):
    if percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"

def display_student(student):
    coursework_total = sum(student["coursework"])
    exam = student["exam"]
    percentage = calculate_percentage(student)
    grade = calculate_grade(percentage)
    return (f"Name: {student['name']} | "
            f"Code: {student['code']} | "
            f"Coursework: {coursework_total} | "
            f"Exam: {exam} | "
            f"Overall %: {percentage:.2f} | "
            f"Grade: {grade}")


def wide_messagebox(title, text):
    top = tk.Toplevel(root)
    top.title(title)
    top.configure(bg="#ffd6e7")
    top.geometry("800x300")
    top.resizable(False, False)
    msg = tk.Message(top, text=text, width=750, bg="#ffd6e7", fg="black", font=("Times new roman", 12))
    msg.pack(pady=20, padx=20)
    tk.Button(top, text="Close", command=top.destroy, bg="#ffecf2", fg="black", font=("Times new roman", 12)).pack(pady=10)

def view_all_students():
    text = ""
    total_percentage = 0
    for s in students:
        text += display_student(s) + "\n"
        total_percentage += calculate_percentage(s)
    if students:
        avg_percentage = total_percentage / len(students)
        text += f"\nTotal Students: {len(students)} | Average %: {avg_percentage:.2f}"
    wide_messagebox("All Students", text)

def view_individual_student():
    code = simpledialog.askstring("Student Code", "Enter student code:", parent=root)
    for s in students:
        if s["code"] == code:
            wide_messagebox("Student Record", display_student(s))
            return
    messagebox.showerror("Error", "Student not found.", parent=root)

def show_highest_score():
    if not students:
        return
    highest = max(students, key=calculate_total)
    wide_messagebox("Highest Score", display_student(highest))

def show_lowest_score():
    if not students:
        return
    lowest = min(students, key=calculate_total)
    wide_messagebox("Lowest Score", display_student(lowest))


root = tk.Tk()
root.title("Student Manager")
root.geometry("500x600")
root.configure(bg="#ffd6e7")


try:
    pil_image = Image.open(image_path)
    pil_image = pil_image.resize((600, 300))  # bigger image
    img = ImageTk.PhotoImage(pil_image)
    image_label = tk.Label(root, image=img, bg="#ffd6e7")
    image_label.pack(pady=20)
except FileNotFoundError:
    tk.Label(root, text="Image not found", bg="#ffd6e7", fg="red", font=("Arial", 16)).pack(pady=20)


load_students()


button_frame = tk.Frame(root, bg="#ffd6e7")
button_frame.pack(expand=True)

btn_options = [
    ("1. View all student records", view_all_students),
    ("2. View individual student record", view_individual_student),
    ("3. Show student with highest total score", show_highest_score),
    ("4. Show student with lowest total score", show_lowest_score),
    ("Quit", root.destroy)
]

for text, cmd in btn_options:
    tk.Button(button_frame, text=text, width=35, command=cmd,
              bg="#ffecf2", fg="black", font=("Times new roman", 14)).pack(pady=8)

root.mainloop() 