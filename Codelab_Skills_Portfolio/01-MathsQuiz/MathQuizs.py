from tkinter import *
from tkinter import messagebox, font
import random

class mathquizs:
    # Initialize the main application window and variables
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quizs")
        self.root.geometry("1200x800")
        self.root.configure(bg='gray')

        # Quiz Tally Variables
        self.difficulty = None
        self.question = 0
        self.score = 0
        self.total_question = 10

        # Main container frame for switching pages
        self.main_frame = Frame(root, bg='gray')
        self.main_frame.pack(expand=True, fill=BOTH)

        self.title_font = font.Font(family="Arial", size=24, weight="bold")

        # Load the initial welcome screen
        self.start_page()

    # Reusable helper to create custom styled labels
    def create_label(self, text, font_size=15, fg_color='gray', pady=10):
        style_label = Label(
            self.main_frame,
            text=text,
            font=("Arial", font_size, "bold"), bg='gray', fg='white', pady=pady
        )
        style_label.pack(pady=pady)
        return style_label

    # Reusable helper to create custom styled buttons
    def create_button(self, text, command):
        btn = Button(
            self.main_frame, 
            text=text, 
            command=command,
            font=('Roboto', 14), bg='white', fg='black'
        )
        btn.pack(pady=20)
        return btn

    # Displays the welcome page
    def start_page(self):
        self.clear_frame()
        self.create_label("Math Quiz", 30, fg_color='blue', pady=20),
        self.create_label("Try and know your arithemtic skills", 18, fg_color='cyan')
        self.create_button("Start", self.difficulty_select)

    # Displays the difficulty selection menu
    def difficulty_select(self):
        self.clear_frame()
        self.create_label("Select Quiz Difficulty", 24, fg_color='pink')
        difficulties = [
            ("Easy (0-10)","Easy"),
            ("Moderate (11-100)", "Moderate"),
            ("Advance (101-999)", "Advance")
        ]

        for label, diff in difficulties:
            self.create_button(label, lambda d=diff: self.start_quiz(d))

    # Randomly generates math problems based on the selected difficulty
    def generate_problems(self):
        difficulty_range = {
            "Easy": (0, 10),
            "Moderate": (11, 100),
            "Advance": (101, 999)
        }

        num_range = difficulty_range[self.difficulty]
        num1 = random.randint(*num_range)
        num2 = random.randint(*num_range)
        operator = random.choice(['+', '-'])
        answer = num1 + num2 if operator == '+' else num1 - num2
        return f'{num1} {operator} {num2}', answer

    # Resets variables and starts the quiz session
    def start_quiz(self, difficulty):
        self.difficulty = difficulty
        self.question = 0
        self.score = 0
        self.next_question()

    # Loads the next question or finishes the quiz if the limit is reached
    def next_question(self):
        if self.question >= self.total_question:
            self.quiz_complete()
            return

        self.clear_frame()
        self.question += 1
        self.current_problem, self.correct_answer = self.generate_problems()
        self.create_label(f"Question {self.question}/{self.total_question}", 22)
        self.create_label(f"{self.current_problem} = ?", 22)

        # Input box for the user's answer
        self.answer_input = Entry(
            self.main_frame, 
            font=('Arial', 16),
            bg='gray',
            fg='blue',
            bd=2,
            relief='groove',
            justify='center'
        )
        self.answer_input.pack(pady=20)
        self.answer_input.focus()

        self.create_button("Enter", self.check_answer)

    # Validates the user's input against the correct answer
    def check_answer(self):
        try:
            user_answer = int(self.answer_input.get())
            if user_answer == self.correct_answer:
                self.score += 1
            self.next_question()
        except ValueError:
            messagebox.showerror("Invalid Input")

    # Displays final score and feedback when the quiz ends
    def quiz_complete(self):
        self.clear_frame()
        self.create_label("Quiz Complete", 28, fg_color='black', pady=20)
        percentage = (self.score / self.total_question)* 100
        self.create_label(f"Your Score: {self.score}/{self.total_question}\n{percentage:.1f}%", 22)

        if percentage == 100:
            total_output = "Perfect!, Unbelievable!"
        elif percentage >= 80:
            total_output = "Good Job!"
        elif percentage >= 60:
            total_output = "Nice"
        else:
            total_output = "You can do Better! I know it!\nJust need to study more."

        self.create_label(total_output, 18)
        self.create_button("Try Again?", self.start_page)

    # Clears all widgets from the main frame for page switching
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Main entry point to run the application
def main():
    root = Tk()
    app = mathquizs(root)
    root.mainloop()

if __name__ == "__main__":
    main()







