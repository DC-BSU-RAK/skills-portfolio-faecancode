from tkinter import *

root = Tk()

import tkinter as tk
from tkinter import messagebox
import random

def displayMenu():
    """Show difficulty selection screen."""
    clear_frame()
    title = tk.Label(root, text="DIFFICULTY LEVEL", font=("Arial", 24))
    title.pack(pady=20)

    tk.Button(root, text="1. Easy", width=20, command=lambda: start_quiz(1)).pack(pady=10)
    tk.Button(root, text="2. Moderate", width=20, command=lambda: start_quiz(2)).pack(pady=10)
    tk.Button(root, text="3. Advanced", width=20, command=lambda: start_quiz(3)).pack(pady=10)

def randomInt(level):
    """Return random numbers based on difficulty."""
    if level == 1:   # 1-digit
        return random.randint(1, 9)
    elif level == 2: # 2-digit
        return random.randint(10, 99)
    elif level == 3: # 4-digit
        return random.randint(1000, 9999)

def decideOperation():
    """Randomly choose + or -."""
    return random.choice(["+", "-"])

def displayProblem():
    """Display the current math question."""
    global num1, num2, operation, attempts

    clear_frame()
    question = f"{num1} {operation} {num2} = "

    tk.Label(root, text=f"Question {current_question}/10", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text=question, font=("Arial", 30)).pack(pady=15)

    answer_entry.delete(0, tk.END)
    answer_entry.pack(pady=10)

    tk.Button(root, text="Submit Answer", command=check_answer).pack(pady=10)

def isCorrect(user_answer):
    """Return True if answer correct."""
    if operation == "+":
        return user_answer == (num1 + num2)
    else:
        return user_answer == (num1 - num2)

def check_answer():
    """Check user’s input and score it."""
    global score, attempts, current_question, num1, num2, operation

    try:
        user_answer = int(answer_entry.get())
    except:
        messagebox.showinfo("Error", "Please enter a number.")
        return

    if isCorrect(user_answer):
        if attempts == 1:
            score += 10
            messagebox.showinfo("Correct!", "Correct! +10 points")
        else:
            score += 5
            messagebox.showinfo("Correct!", "Correct on second try! +5 points")

        current_question += 1
        if current_question > 10:
            displayResults()
        else:
            # generate next question
            attempts = 1
            generate_question()
            displayProblem()

    else:
        if attempts == 1:
            attempts = 2
            messagebox.showinfo("Wrong", "Incorrect! Try again.")
        else:
            messagebox.showinfo("Wrong", "Still incorrect. Moving to next question.")
            current_question += 1
            if current_question > 10:
                displayResults()
            else:
                attempts = 1
                generate_question()
                displayProblem()

def generate_question():
    """Generate new question variables."""
    global num1, num2, operation
    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    operation = decideOperation()

def displayResults():
    """Show final score + ranking."""
    clear_frame()
    grade = ""

    if score >= 90: grade = "A+"
    elif score >= 80: grade = "A"
    elif score >= 70: grade = "B"
    elif score >= 60: grade = "C"
    else: grade = "D"

    tk.Label(root, text=f"Your Final Score: {score}/100", font=("Arial", 24)).pack(pady=20)
    tk.Label(root, text=f"Grade: {grade}", font=("Arial", 20)).pack(pady=10)

    tk.Button(root, text="Play Again", command=displayMenu).pack(pady=20)
    tk.Button(root, text="Exit", command=root.quit).pack()

def start_quiz(level):
    """Initialize quiz values."""
    global difficulty, score, current_question, attempts

    difficulty = level
    score = 0
    current_question = 1
    attempts = 1

    generate_question()
    displayProblem()

def clear_frame():
    """Remove all widgets from the window."""
    for widget in root.winfo_children():
        widget.pack_forget()

# -----------------------------
# MAIN WINDOW
# -----------------------------

root = tk.Tk()
root.title("Maths Quiz")
root.geometry("500x400")

answer_entry = tk.Entry(root, font=("Arial", 20))

displayMenu()

root.mainloop()



root.mainloop()