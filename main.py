import tkinter as tk
import random

# Colors
BG = "#EAF4FF"
WHITE = "#FFFFFF"
BLUE = "#2878C8"
DARK = "#183B5B"
GREEN = "#16845B"
RED = "#D94A4A"

WORDS = [
    "python", "computer", "keyboard", "challenge",
    "program", "developer", "database", "science",
    "project", "function", "variable", "internet",
    "software", "student", "learning", "coding",
    "algorithm", "digital", "monitor", "success",
    "technology", "network", "practice", "solution"
]


class ReverseTypingChallenge:
    def __init__(self, root):
        self.root = root
        self.root.title("Reverse Typing Challenge")
        self.root.geometry("700x600")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.timer_job = None
        self.build_start_screen()

    def clear_screen(self):
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        for widget in self.root.winfo_children():
            widget.destroy()

    def build_start_screen(self):
        self.clear_screen()

        tk.Label(
            self.root,
            text="Reverse Typing Challenge",
            font=("Segoe UI", 25, "bold"),
            bg=BG, fg=DARK
        ).pack(pady=(35, 8))

        tk.Label(
            self.root,
            text="See the word. Type it backwards. Beat the clock!",
            font=("Segoe UI", 11),
            bg=BG, fg=DARK
        ).pack(pady=(0, 25))

        card = tk.Frame(self.root, bg=WHITE, padx=35, pady=25)
        card.pack(padx=55, fill="x")

        tk.Label(
            card,
            text="Enter your name",
            font=("Segoe UI", 11, "bold"),
            bg=WHITE, fg=DARK
        ).pack(anchor="w")

        self.name_entry = tk.Entry(
            card, font=("Segoe UI", 13), justify="center"
        )
        self.name_entry.pack(fill="x", pady=(8, 20), ipady=6)

        tk.Label(
            card,
            text="Choose your time limit",
            font=("Segoe UI", 11, "bold"),
            bg=WHITE, fg=DARK
        ).pack(pady=(0, 10))

        self.duration_var = tk.IntVar(value=25)

        options = tk.Frame(card, bg=WHITE)
        options.pack(pady=(0, 20))

        for seconds in (25, 45, 60):
            tk.Radiobutton(
                options,
                text=f"{seconds} seconds",
                variable=self.duration_var,
                value=seconds,
                font=("Segoe UI", 10),
                bg=WHITE, fg=DARK,
                selectcolor=BG,
                activebackground=WHITE
            ).pack(side="left", padx=10)

        tk.Button(
            card,
            text="START GAME",
            command=self.start_game,
            font=("Segoe UI", 12, "bold"),
            bg=BLUE, fg=WHITE,
            activebackground="#1E63A6",
            activeforeground=WHITE,
            relief="flat", cursor="hand2",
            pady=12
        ).pack(fill="x")

        tk.Label(
            self.root,
            text="Reverse each word before time runs out!",
            font=("Segoe UI", 10),
            bg=BG, fg=DARK
        ).pack(pady=20)

        self.name_entry.focus_set()

    def start_game(self):
        name = self.name_entry.get().strip()

        if not name:
            tk.messagebox.showwarning(
                "Name Required",
                "Please enter your name before starting."
            )
            self.name_entry.focus_set()
            return

        self.player_name = name
        self.duration = self.duration_var.get()
        self.remaining = self.duration
        self.correct = 0
        self.wrong = 0
        self.attempts = 0
        self.running = True

        self.clear_screen()

        tk.Label(
            self.root,
            text=f"Good luck, {self.player_name}!",
            font=("Segoe UI", 18, "bold"),
            bg=BG, fg=DARK
        ).pack(pady=(25, 10))

        self.timer_label = tk.Label(
            self.root,
            text=str(self.remaining),
            font=("Segoe UI", 30, "bold"),
            bg=BG, fg=BLUE
        )
        self.timer_label.pack()

        tk.Label(
            self.root,
            text="SECONDS LEFT",
            font=("Segoe UI", 9, "bold"),
            bg=BG, fg=DARK
        ).pack(pady=(0, 20))

        self.word_label = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 30, "bold"),
            bg=WHITE, fg=BLUE,
            width=18, pady=20
        )
        self.word_label.pack(padx=40, fill="x")

        tk.Label(
            self.root,
            text="Type the word backwards",
            font=("Segoe UI", 11),
            bg=BG, fg=DARK
        ).pack(pady=(20, 8))

        self.answer_entry = tk.Entry(
            self.root,
            font=("Segoe UI", 16),
            justify="center"
        )
        self.answer_entry.pack(padx=65, fill="x", ipady=7)
        self.answer_entry.bind("<Return>", self.check_answer)

        self.feedback = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg=BG, fg=GREEN
        )
        self.feedback.pack(pady=10)

        self.score_label = tk.Label(
            self.root,
            text="Correct: 0   Wrong: 0",
            font=("Segoe UI", 12, "bold"),
            bg=BG, fg=DARK
        )
        self.score_label.pack(pady=8)

        self.next_word()
        self.answer_entry.focus_set()
        self.timer_job = self.root.after(1000, self.update_timer)

    def next_word(self):
        self.current_word = random.choice(WORDS)
        self.word_label.config(text=self.current_word)
        self.answer_entry.delete(0, tk.END)

    def check_answer(self, event=None):
        if not self.running:
            return

        answer = self.answer_entry.get().strip().lower()

        if not answer:
            return

        self.attempts += 1
        expected = self.current_word[::-1]

        if answer == expected:
            self.correct += 1
            self.feedback.config(
                text="Correct! Great job!", fg=GREEN
            )
        else:
            self.wrong += 1
            self.feedback.config(
                text=f"Incorrect! Answer: {expected}", fg=RED
            )

        self.score_label.config(
            text=f"Correct: {self.correct}   Wrong: {self.wrong}"
        )

        self.next_word()

    def update_timer(self):
        if not self.running:
            return

        self.remaining -= 1
        self.timer_label.config(text=str(self.remaining))

        if self.remaining <= 0:
            self.finish_game()
        else:
            self.timer_job = self.root.after(
                1000, self.update_timer
            )

    def finish_game(self):
        self.running = False
        self.timer_job = None
        self.clear_screen()

        accuracy = (
            self.correct / self.attempts * 100
            if self.attempts else 0
        )

        tk.Label(
            self.root,
            text="Game Completed!",
            font=("Segoe UI", 25, "bold"),
            bg=BG, fg=DARK
        ).pack(pady=(55, 20))

        tk.Label(
            self.root,
            text=(
                f"Player: {self.player_name}\n\n"
                f"Time limit: {self.duration} seconds\n"
                f"Correct answers: {self.correct}\n"
                f"Wrong answers: {self.wrong}\n"
                f"Total attempts: {self.attempts}\n"
                f"Accuracy: {accuracy:.1f}%\n"
                f"Final score: {self.correct}"
            ),
            font=("Segoe UI", 13),
            bg=BG, fg=DARK,
            justify="center"
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="PLAY AGAIN",
            command=self.build_start_screen,
            font=("Segoe UI", 12, "bold"),
            bg=BLUE, fg=WHITE,
            relief="flat", cursor="hand2",
            padx=25, pady=12
        ).pack(pady=25)


if __name__ == "__main__":
    from tkinter import messagebox

    tk.messagebox = messagebox

    root = tk.Tk()
    app = ReverseTypingChallenge(root)
    root.mainloop()
