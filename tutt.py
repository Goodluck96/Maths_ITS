import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random


SKILLS = {
    "Addition": {
        "easy": lambda: (random.randint(1, 10), random.randint(1, 10), "+"),
        "hard": lambda: (random.randint(10, 50), random.randint(10, 50), "+")
    },
    "Multiplication": {
        "easy": lambda: (random.randint(1, 5), random.randint(1, 5), "*"),
        "hard": lambda: (random.randint(5, 12), random.randint(5, 12), "*")
    }
}


class Student:
    def __init__(self):
        self.mastery = {
            "Addition": 0.6,
            "Multiplication": 0.4
        }

    def update_mastery(self, skill, correct):
        delta = 0.1 if correct else -0.1
        self.mastery[skill] = max(0.0, min(1.0, self.mastery[skill] + delta))


class Tutor:
    def __init__(self, student):
        self.student = student
        self.current_skill = None
        self.correct_answer = None
        self.operator = None

    def select_skill(self):
        self.current_skill = min(self.student.mastery, key=self.student.mastery.get)
        return self.current_skill

    def difficulty(self, skill):
        return "easy" if self.student.mastery[skill] < 0.7 else "hard"

    def generate_problem(self):
        skill = self.select_skill()
        diff = self.difficulty(skill)
        a, b, op = SKILLS[skill][diff]()
        self.correct_answer = eval(f"{a}{op}{b}")
        self.operator = op
        return f"{a} {op} {b}"

    def hint(self):
        return {
            "+": "Break numbers into smaller parts.",
            "*": "Think of multiplication as repeated addition."
        }.get(self.operator, "Check your operation.")


#GUI with Matplotlib dashboard

class ITSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Math Tutor Dashboard")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")

        self.student = Student()
        self.tutor = Tutor(self.student)

        # Problem display
        self.problem_label = tk.Label(root, text="", font=("Arial", 18), bg="#f0f0f0")
        self.problem_label.pack(pady=10)

        # Answer input
        self.answer_entry = tk.Entry(root, font=("Arial", 16))
        self.answer_entry.pack(pady=5)

        self.submit_btn = tk.Button(root, text="Submit Answer", font=("Arial", 12),
                                    command=self.submit)
        self.submit_btn.pack(pady=5)

        # Feedback
        self.feedback_label = tk.Label(root, text="", font=("Arial", 12), bg="#f0f0f0")
        self.feedback_label.pack(pady=5)

        # Mastery chart
        self.fig, self.ax = plt.subplots(figsize=(5,2))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(pady=10)
        self.update_chart()

        self.next_problem()

    def next_problem(self):
        self.problem_label.config(text=self.tutor.generate_problem())
        self.answer_entry.delete(0, tk.END)

    def submit(self):
        try:
            answer = int(self.answer_entry.get())
            correct = answer == self.tutor.correct_answer
        except ValueError:
            correct = False

        self.student.update_mastery(self.tutor.current_skill, correct)

        if correct:
            self.feedback_label.config(text="✅ Correct!", fg="green")
        else:
            self.feedback_label.config(
                text=f"❌ Incorrect. Hint: {self.tutor.hint()}",
                fg="red"
            )

        self.update_chart()
        self.next_problem()

    def update_chart(self):
        self.ax.clear()
        skills = list(self.student.mastery.keys())
        mastery = [self.student.mastery[s] for s in skills]
        bars = self.ax.bar(skills, mastery, color=["#4caf50", "#2196f3"])
        self.ax.set_ylim(0,1)
        self.ax.set_ylabel("Mastery Level")
        self.ax.set_title("Current Mastery Progress")
        self.ax.bar_label(bars, fmt="%.2f")
        self.fig.tight_layout()
        self.canvas.draw()


# Run application
if __name__ == "__main__":
    root = tk.Tk()
    app = ITSGUI(root)
    root.mainloop()
