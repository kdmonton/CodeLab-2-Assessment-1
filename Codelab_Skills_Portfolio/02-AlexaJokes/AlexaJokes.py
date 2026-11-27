from tkinter import *
from tkinter import messagebox, filedialog
import random


root = Tk()
root.title('Alexa, tell me a Joke')
root.geometry('500x500')
root.configure(bg='gray')


# LOAD JOKES FUNCTION
def load_jokes (jokes_path):
    try:
        with open(jokes_path, 'r')as file:
            jokes = [[p.strip().lstrip('|').strip() for p in line.strip().split('?', 1)] for line in file if '?' in line] #Asked AI on the this bit, because when it answer it has | on the start of every punchline
        return jokes
    except FileNotFoundError:
        return[]


# SHOW JOKE FUNCTION (Displays Setup)
def show_jokes():
    global current_joke
    if jokes:
        current_joke = random.choice(jokes)
        txtarea.delete('1.0', 'end')
        txtarea.insert('1.0', f'Setup: {current_joke[0]}?')
        answer_btn.config(state='normal')
    else:
        txtarea.delete('1.0', 'end')
        txtarea.insert('1.0', 'Cannot find joke')


# SHOW ANSWER FUNCTION (Displays Punchline)
def joke_answer():
    if current_joke:
        txtarea.insert(END, f'\n\nAnswer: {current_joke[1]}')
        answer_btn.config(state='disabled')


# INITIALIZING DATA
jokes = load_jokes("randomJokes.txt")
current_joke = None

# GUI HEADER SECTION
header_frame = Frame(root, bg='orange')
header_frame.place(x=0, y=0, width=500, height=60)
header_label = Label(header_frame, text="Dad Jokes by Alexa", font=("Arial", 22), bg='orange', fg='black', pady=10)
header_label.pack()

# TRIGGER BUTTON (Get a Joke)
setup_btn = Button(root, text='Alexa, tell me a Joke', font=('Impact', 16), bg='red', fg='white', command=show_jokes)
setup_btn.place(x=50, y=75, width=400, height=45)

# TEXT DISPLAY AREA SECTION
text_frame = Frame(root, bg='gray')
text_frame.place(x=50, y=130, width=400, height=250)

txtarea = Text(text_frame, wrap=WORD, font=('Italic', 18), bg='green', fg='black', padx=10, pady=10, relief=GROOVE, bd=2)
txtarea.pack(fill=BOTH, expand=TRUE)

# ANSWER BUTTON (Show the Line)
answer_btn = Button(root, text="Show the LINE", font=('Impact', 16), bg='red', fg='white', 
                    activebackground='blue', activeforeground='white', command=joke_answer, state='disabled')
answer_btn.place(x=50, y=395, width=400, height=45)

# EXIT/QUIT BUTTON (Done?)
quit_btn = Button(root, text="Done?", font=('Roboto', 16), bg='pink', fg='black', activebackground='blue', activeforeground='white', command=root.destroy)
quit_btn.place(x=175, y=450, width=150, height=35)

# MAIN APPLICATION LOOP
root.mainloop()
