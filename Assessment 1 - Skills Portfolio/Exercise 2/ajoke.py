import random
import os
from tkinter import *

print("Current working directory:", os.getcwd())  

jokes = []
current_joke = None

def load_jokes():
    global jokes
    jokes = []

    FILE_PATH = os.path.join(os.path.dirname(__file__), "randomJokes.txt")

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            lines = file.readlines()

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    setup = setup.strip() + "?"
                    punchline = punchline.strip()
                    jokes.append((setup, punchline))
                else:
                    jokes.append((line, ""))

        print(f"Loaded {len(jokes)} jokes.")

    except FileNotFoundError:
        print("ERROR: randomJokes.txt NOT FOUND at:", FILE_PATH)


def tell_joke():
    global current_joke

    if not jokes:
        setup_label.config(text="No jokes found!")
        punchline_label.config(text="")
        return

    current_joke = random.choice(jokes)
    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")


def show_punchline():
    if current_joke:
        punchline_label.config(text=current_joke[1])
    else:
        punchline_label.config(text="Press 'Faiza tell me a Joke' first!")


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

btn_frame = Frame(root, bg="#ffd6e7")
btn_frame.pack(pady=20)

Button(btn_frame, text="Faiza tell me a Joke", font=("Times New Roman", 14),
       bg="#ffecf2", fg="black", command=tell_joke, width=20).grid(row=0, column=0, padx=10, pady=5)

Button(btn_frame, text="Show Punchline", font=("Times New Roman", 14),
       bg="#ffecf2", fg="black", command=show_punchline, width=20).grid(row=0, column=1, padx=10, pady=5)

Button(btn_frame, text="Next Joke", font=("Times New Roman", 14),
       bg="#ffecf2", fg="black", command=next_joke, width=20).grid(row=1, column=0, padx=10, pady=5)

Button(btn_frame, text="Quit", font=("Times New Roman", 14),
       bg="#ffecf2", fg="black", command=root.destroy, width=20).grid(row=1, column=1, padx=10, pady=5)

load_jokes()

root.mainloop()
