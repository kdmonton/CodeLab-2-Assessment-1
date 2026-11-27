from tkinter import *
from tkinter import messagebox
import os


class Student_Record_Manager:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Manager")
        self.master.geometry('900x600')
        self.master.resizable(0, 0)
        self.master['bg'] = "#121824"

        self.frame_color = "#334155"
        self.text_color = "#F8FAFC"
        self.txt_file = "studentsMark.txt"

        self.names = [
            "John Curry", "Matt Thompson", "Jo Hyde", "Sam Sturtivant",
            "Ron Herrema", "Gareth Southgate", "Lee Scott", "Jake Hobbs"
        ]

        self.create_initial_file()
        self.setup_ui()


    #  File handling / grade calculation
    def create_initial_file(self):
        """Create the default data file if it does not exist."""
        if not os.path.exists(self.txt_file):
            default_records = [
                "1,John Curry,20,25,30,75",
                "2,Sam Sturtivant,22,24,28,70",
                "3,Lee Scott,25,20,25,65",
                "4,Matt Thompson,18,22,27,80",
                "5,Ron Herrema,20,23,26,72",
                "6,Jake Hobbs,21,24,29,75",
                "7,Jo Hyde,19,21,26,70",
                "8,Gareth Southgate,22,20,25,65"
            ]
            with open(self.txt_file, 'w') as f:
                f.write('\n'.join(default_records))

    def calculate_grade(self, work, test):
        """Return (percentage, grade_letter)."""
        total = work + test
        rating = (total / 160) * 100

        if rating >= 70:
            grade = "A"
        elif rating >= 60:
            grade = "B"
        elif rating >= 50:
            grade = "C"
        elif rating >= 40:
            grade = "D"
        else:
            grade = "F"

        return rating, grade

    #  UI construction
    def setup_ui(self):
        """Create the two main panels – button panel (left) and display panel (right)."""
 
        main_frame = Frame(self.master, bg=self.frame_color)
        main_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

        btn_frame = Frame(main_frame, bg=self.frame_color, width=200)
        btn_frame.pack(side=LEFT, fill=Y, padx=(0, 10))
        btn_frame.pack_propagate(False)    

        # Title above the button column
        title_lbl = Label(
            btn_frame,
            text="Select a student to view information",
            fg=self.text_color,
            bg=self.frame_color,
            font=("Arial", 16, "bold")
        )
        title_lbl.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        self.create_btn(btn_frame)

        display_frame = Frame(main_frame, bg=self.frame_color)
        display_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        self.create_text_display(display_frame)

    def create_btn(self, parent):
        """Create and grid‑place the three main buttons and the drop‑down."""
        # Uniform button style
        btn_opts = dict(
            fg=self.text_color,
            bg="#18181B",
            font=("Arial", 14),
            width=18,
            height=2,
            relief=FLAT,
            activebackground="#27272A",
            activeforeground=self.text_color,
        )

        #View all records
        view_all = Button(
            parent,
            text="View All\nStudents Records",
            command=self.view_all_records,
            **btn_opts
        )
        view_all.grid(row=1, column=0, pady=8, padx=10)

        #Highest score
        high_btn = Button(
            parent,
            text="Show Highest Score",
            command=self.show_highest_score,
            **btn_opts
        )
        high_btn.grid(row=2, column=0, pady=8, padx=10)

        #Lowest score
        low_btn = Button(
            parent,
            text="Show Lowest Score",
            command=self.show_lowest_score,
            **btn_opts
        )
        low_btn.grid(row=3, column=0, pady=8, padx=10)

        ind_lbl = Label(
            parent,
            text="Show Individual Student Record:",
            fg=self.text_color,
            bg=self.frame_color,
            font=("Arial", 12)
        )
        ind_lbl.grid(row=4, column=0, pady=(20, 4), padx=10, sticky="w")

        self.s_select = StringVar(value=self.names[0])
        dropdown = OptionMenu(
            parent,
            self.s_select,
            *self.names,
            command=lambda _: self.display_individual_record(self.s_select.get())
        )
        dropdown.config(
            width=20,
            font=("Arial", 12),
            bg="#18181B",
            fg=self.text_color,
            highlightthickness=0,
            activebackground="#27272A",
            activeforeground=self.text_color,
            relief=FLAT
        )
        dropdown["menu"].config(
            bg="#18181B",
            fg=self.text_color,
            activebackground="#27272A",
            activeforeground=self.text_color,
            font=("Arial", 12)
        )
        dropdown.grid(row=5, column=0, pady=4, padx=10, sticky="w")

    def create_text_display(self, parent):
        """Create the scrollable Text widget."""
        self.showcase = Text(
            parent,
            font=("Arial", 12),
            bg="#1e293b",
            fg=self.text_color,
            insertbackground=self.text_color,
            wrap=WORD,
            spacing3=4,
            relief=FLAT,
            bd=2
        )
        self.showcase.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 2), pady=5)

        scroll = Scrollbar(parent, orient="vertical", command=self.showcase.yview)
        scroll.pack(side=RIGHT, fill=Y, pady=5)
        self.showcase.config(yscrollcommand=scroll.set)

    #  Core actions (unchanged from your original implementation)
    def view_all_records(self):
        self.showcase.delete("1.0", END)
        try:
            with open(self.txt_file, "r") as file:
                for line in file:
                    if not line.strip():
                        continue
                    s_data = line.strip().split(",")
                    s_number, s_name = s_data[0], s_data[1]
                    work_marks = sum(map(int, s_data[2:5]))
                    test_marks = int(s_data[5])

                    rating, grade = self.calculate_grade(work_marks, test_marks)
                    record = (
                        f"Name: {s_name}\n"
                        f"Number: {s_number}\n"
                        f"Total Coursework Score: {work_marks}\n"
                        f"Exam Score: {test_marks}\n"
                        f"Overall Percentage: {rating:.2f}%\n"
                        f"Grade: {grade}\n"
                        "\n" + "─" * 30 + "\n\n"
                    )
                    self.showcase.insert(END, record)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read student records: {e}")

    def display_individual_record(self, student_name):
        self.showcase.delete("1.0", END)
        try:
            with open(self.txt_file, "r") as file:
                for line in file:
                    if not line.strip():
                        continue
                    s_data = line.strip().split(",")
                    if s_data[1] == student_name:
                        s_number = s_data[0]
                        work_marks = sum(map(int, s_data[2:5]))
                        test_marks = int(s_data[5])

                        rating, grade = self.calculate_grade(work_marks, test_marks)

                        record = (
                            f"Name: {student_name}\n"
                            f"Number: {s_number}\n"
                            f"Total Coursework Score: {work_marks}\n"
                            f"Exam Score: {test_marks}\n"
                            f"Overall Percentage: {rating:.2f}%\n"
                            f"Grade: {grade}\n"
                        )
                        self.showcase.insert(END, record)
                        break
        except Exception as e:
            messagebox.showerror("Error", f"Could not read student records: {e}")

    def show_highest_score(self):
        try:
            with open(self.txt_file, "r") as file:
                students = []
                for line in file:
                    if not line.strip():
                        continue
                    s_data = line.strip().split(",")
                    s_name = s_data[1]
                    work_marks = sum(map(int, s_data[2:5]))
                    test_marks = int(s_data[5])

                    rating, _ = self.calculate_grade(work_marks, test_marks)
                    students.append((s_name, rating))

                highest_student = max(students, key=lambda x: x[1])
                self.display_individual_record(highest_student[0])
        except Exception as e:
            messagebox.showerror("Error", f"Could not find highest score: {e}")

    def show_lowest_score(self):
        try:
            with open(self.txt_file, "r") as file:
                students = []
                for line in file:
                    if not line.strip():
                        continue
                    s_data = line.strip().split(",")
                    s_name = s_data[1]
                    work_marks = sum(map(int, s_data[2:5]))
                    test_marks = int(s_data[5])

                    rating, _ = self.calculate_grade(work_marks, test_marks)
                    students.append((s_name, rating))

                lowest_student = min(students, key=lambda x: x[1])
                self.display_individual_record(lowest_student[0])
        except Exception as e:
            messagebox.showerror("Error", f"Could not find lowest score: {e}")


def main():
    root = Tk()
    app = Student_Record_Manager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
