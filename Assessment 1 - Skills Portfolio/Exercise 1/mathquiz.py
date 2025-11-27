from tkinter import *  #imports the Tkinter functions, classes and widgets
import random  #imports the random module to generate random numbers 
from tkinter import messagebox  #imports messagebox to show pop ups


score = 0  #stores the user's score
question_count = 0  #keeps track of how many questions have been asked so far
difficulty = None  #stores the selected difficulty level
correct_answer = None  #stores the correct answer for the current question 
first_attempt = True  #checks if user is on first attempt for a question 
answer_history = []  #stores tuples of question, user answer, correct answer

def displayTitleScreen():
    clear_window()

    Label(root, text="Math Quiz", bg=bg_color, fg="black",
          font=("Times New Roman", 28, "bold")).pack(pady=80)

    Button(root, text="Play", command=displayMenu,
           bg=btn_color, fg="black", font=("Arial", 18), width=10).pack(pady=20)

def displayMenu():
    clear_window()  #removes all widgets from the window

    #title 
    Label(root, text="Select Difficulty", bg=bg_color, fg="black",
          font=("Times New roman", 20, "bold")).pack(pady=20)

    #buttons for the difficulty level
    Button(root, text="Easy",
           command=lambda: start_quiz("Easy"), 
           bg=btn_color, fg="black", font=("Arial", 15)).pack(pady=12)

    Button(root, text="Moderate",
           command=lambda: start_quiz("Moderate"),  
           bg=btn_color, fg="black", font=("Arial", 15)).pack(pady=12)

    Button(root, text="Advanced",
           command=lambda: start_quiz("Advanced"),  
           bg=btn_color, fg="black", font=("Arial", 15)).pack(pady=12)

def randomInt(level):
    if level == "Easy":
        return random.randint(1, 9)  #random number from 1-10
    elif level == "Moderate":
        return random.randint(10, 99)  #random number from 10-99
    elif level == "Advanced":
        return random.randint(1000, 9999)  #random number from 1000-9999 
    
def generate_problem():
    op = random.choice(["+", "-"])  #randomly choose + for addition or - for subtraction
    n1 = randomInt(difficulty)  #generates first number
    n2 = randomInt(difficulty)  #generates second number

    #ensure easy difficulty subtraction never goes negative to keep the questions easy
    if difficulty == "Easy" and op == "-" and n2 > n1:
        n1, n2 = n2, n1  #swaps numbers so result is positive

    return n1, op, n2  #return numbers and operator

def show_question():
    global correct_answer, num1, num2, op, first_attempt

    first_attempt = True  #reset first_attempt for new question
    clear_window() 

    num1, op, num2 = generate_problem()  #generate question
    correct_answer = eval(f"{num1} {op} {num2}")  #calculate correct answer
    question_text = f"{num1} {op} {num2} ="  #format question string

    #shows question number
    Label(root, text=f"Question {question_count + 1}/10", bg=bg_color,
          fg="black", font=("Arial", 18)).pack(pady=12)

    #shows question
    Label(root, text=question_text, bg=bg_color,
          fg="black", font=("Arial", 32, "bold")).pack(pady=20)

    #inputing the answer
    global answer_entry
    answer_entry = Entry(root, font=("Arial", 18), width=10, justify="center")
    answer_entry.pack(pady=10)

    #submit button
    Button(root, text="Submit", command=lambda: check_answer(question_text),
           bg=btn_color, fg="black", font=("Arial", 15)).pack(pady=14)
    
def check_answer(question_text):
    global score, question_count, first_attempt

    user_ans = answer_entry.get()  #get the user's input
    if user_ans.strip() == "":
        messagebox.showwarning("Error", "please write your answer")  #warning pop up if answer is left blank
        return

    try:
        user_ans = int(user_ans)  #convert input to integer
    except:
        messagebox.showwarning("Error", "please write a number")  #warning pop up if user did not input a integer
        return

    if user_ans == correct_answer:  #correct answer
        if first_attempt:
            score += 10  #adds 10 points for first try
        else:
            score += 5  #adds 5 points for second try
        answer_history.append((question_text, user_ans, correct_answer, True))  #saves history of answers
        question_count += 1

        if question_count == 10:
            displayResults()  #if 10 questions done, show results
        else:
            show_question()  #shows next question

    else:  #if its the wrong answer
        if first_attempt:
            messagebox.showerror("Incorrect", "wrong answer :( please try again")  #first attempt warning
            first_attempt = False  # next try won't show message
        else:
            answer_history.append((question_text, user_ans, correct_answer, False))  #saves wrong attempt
            question_count += 1
            if question_count == 10:
                displayResults()
            else:
                show_question()

def displayResults():
    clear_window()  

    #shows the final score
    Label(root, text="Quiz Finished!", bg=bg_color, fg="black",
          font=("Times new roman", 22, "bold")).pack(pady=18)
    Label(root, text=f"Score: {score}/100", bg=bg_color,
          fg="black", font=("Arial", 18)).pack(pady=10)

    #shows personalized feedback
    if score == 100:
        feedback = "Good job! You're so smart"
    elif score >= 60:
        feedback = "Good job! You can do better next time"
    else:
        feedback = "It's okay you tried! I know you can do it next time"

    Label(root, text=feedback, bg=bg_color, fg="black",
          font=("Arial", 16)).pack(pady=12)

    #a scrollable frame to show all questions and answers
    summary_frame = Frame(root, bg=bg_color)
    summary_frame.pack(pady=10, fill=BOTH, expand=True)

    canvas = Canvas(summary_frame, bg=bg_color)
    scrollbar = Scrollbar(summary_frame, orient=VERTICAL, command=canvas.yview)
    scroll_frame = Frame(canvas, bg=bg_color)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    #displays all questions with the correct/incorrect answers
    for q, user, correct, correct_bool in answer_history:
        color = "green" if correct_bool else "red"
        Label(scroll_frame, text=f"{q} Your answer: {user} | Correct: {correct}",
              fg=color, bg=bg_color, font=("Arial", 14)).pack(anchor="w", pady=3)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    #play again and quit buttons
    Button(root, text="Play Again", command=reset_quiz,
           bg=btn_color, fg="black", font=("Arial", 15)).pack(pady=10)
    Button(root, text="Quit", command=root.destroy,
           bg="#ffffff", fg="black", font=("Arial", 15)).pack(pady=6)

def start_quiz(level):
    global difficulty, score, question_count, answer_history
    difficulty = level
    score = 0
    question_count = 0
    answer_history = []
    show_question()  #show first question

def reset_quiz():
    displayMenu()

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

root = Tk()
root.title("Math Quiz")
root.geometry("500x600")   

bg_color = "#ffd6e7"  
btn_color = "#ffecf2"  

root.configure(bg=bg_color)

displayTitleScreen()
root.mainloop()
    
