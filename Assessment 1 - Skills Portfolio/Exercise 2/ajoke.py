import random
from tkinter import *


jokes = []  #list to hold jokes as tuples
current_joke = None  #the current joke being displayed

def load_jokes():
    global jokes
    jokes = []
    try:
        with open("randomJokes.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if "?" in line:
                    setup, punchline = line.strip().split("?", 1)  #split only at the first question mark
                    jokes.append((setup + "?", punchline))
    except FileNotFoundError:
        print("randomJokes.txt not found!")

def tell_joke():
    global current_joke
    if jokes:
        current_joke = random.choice(jokes)  #picks a random joke
        setup_label.config(text=current_joke[0]) 
        punchline_label.config(text="")  

def show_punchline():
    if current_joke:
        punchline_label.config(text=current_joke[1])  #displays the punchline

def next_joke():
    tell_joke()


root = Tk()
root.title("Joke Assistant")
root.geometry("600x400")
root.configure(bg="#ffd6e7") 

setup_label = Label(root, text="", font=("Arial", 18, "bold"),
                    bg="#ffd6e7", fg="black", wraplength=550, justify="center")
setup_label.pack(pady=40)

punchline_label = Label(root, text="", font=("Arial", 16),
                        bg="#ffd6e7", fg="black", wraplength=550, justify="center")
punchline_label.pack(pady=20)

# Buttons
btn_frame = Frame(root, bg="#ffd6e7")
btn_frame.pack(pady=20)

Button(btn_frame, text="Faiza tell me a Joke", font=("Times new roman", 14),
       bg="#ffecf2", fg="black", command=tell_joke, width=20).grid(row=0, column=0, padx=10, pady=5)

Button(btn_frame, text="Show Punchline", font=("Times new roman", 14),
       bg="#ffecf2", fg="black", command=show_punchline, width=20).grid(row=0, column=1, padx=10, pady=5)

Button(btn_frame, text="Next Joke", font=("Times new roman", 14),
       bg="#ffecf2", fg="black", command=next_joke, width=20).grid(row=1, column=0, padx=10, pady=5)

Button(btn_frame, text="Quit", font=("Times new roman", 14),
       bg="#ffecf2", fg="black", command=root.destroy, width=20).grid(row=1, column=1, padx=10, pady=5)

#loads jokes from txt file
load_jokes()

root.mainloop()