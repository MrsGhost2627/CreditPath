import argparse
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar


class CreditPathApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CreditPath – Smart Credit & Finance Tracker")
        self.root.geometry("450x450")
        self.root.resizable(False, False)

        # Variables
        self.savings = tk.IntVar(value=0)
        self.amount = tk.IntVar()
        self.goal = tk.IntVar(value=1000)
        self.level = tk.IntVar(value=1)

        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(
            self.root,
            text="CreditPath",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        tk.Label(
            self.root,
            text="Build smart credit habits and plan for big purchases!",
            font=("Arial", 10)
        ).pack(pady=5)

        # Amount Entry
        tk.Label(self.root, text="Enter amount to add to savings:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.amount).pack()

        # Goal Entry
        tk.Label(self.root, text="Savings Goal:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.goal).pack()

        # Savings Display
        tk.Label(self.root, text="Total Savings:", font=("Arial", 12)).pack(pady=5)
        self.savings_label = tk.Label(
            self.root,
            textvariable=self.savings,
            font=("Arial", 14, "bold")
        )
        self.savings_label.pack()

        # Progress Bar
        self.progress_bar = Progressbar(
            self.root,
            length=300,
            maximum=100
        )
        self.progress_bar.pack(pady=15)

        # Level Display
        self.level_label = tk.Label(
            self.root,
            text="Level: Budget Beginner",
            font=("Arial", 10, "italic")
        )
        self.level_label.pack(pady=5)

        # Buttons
        tk.Button(
            self.root,
            text="Add to Savings",
            command=self.add_savings,
            width=20
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Reset",
            command=self.reset_data,
            width=20
        ).pack(pady=5)

    def add_savings(self):
        try:
            value = self.amount.get()
            if value <= 0:
                raise ValueError

            self.savings.set(self.savings.get() + value)
            self.amount.set(0)
            self.update_progress()
            self.check_level()
            messagebox.showinfo("Success", "Savings updated! 💰")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number.")

    def update_progress(self):
        if self.goal.get() > 0:
            progress = (self.savings.get() / self.goal.get()) * 100
            self.progress_bar["value"] = progress

            if progress >= 100:
                messagebox.showinfo(
                    "Achievement Unlocked!",
                    "🏠 Savings goal reached! You're ready for big purchases!"
                )

    def check_level(self):
        savings = self.savings.get()

        if savings >= 5000:
            self.level.set(4)
            self.level_label.config(text="Level: Home Buyer Ready 🏠")
        elif savings >= 2500:
            self.level.set(3)
            self.level_label.config(text="Level: Financial Planner 📊")
        elif savings >= 1000:
            self.level.set(2)
            self.level_label.config(text="Level: Credit Builder 💳")
        else:
            self.level.set(1)
            self.level_label.config(text="Level: Budget Beginner 🌱")

    def reset_data(self):
        self.savings.set(0)
        self.amount.set(0)
        self.progress_bar["value"] = 0
        self.level_label.config(text="Level: Budget Beginner 🌱")
        messagebox.showinfo("Reset", "All data has been reset.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CreditPath GUI or CLI")
    parser.add_argument("--cli", action="store_true", help="Run a simple CLI fallback (no GUI)")
    parser.add_argument("--test-gui", action="store_true", help="Initialize GUI headlessly for a quick test and exit")
    args = parser.parse_args()

    def run_cli():
        state = {"savings": 0, "goal": 1000}
        def show_state():
            savings = state["savings"]
            goal = state["goal"]
            progress = (savings / goal) * 100 if goal > 0 else 0          
            print(f"Savings: {savings}")
            print(f"Goal: {goal}")
            print(f"Progress: {progress:.1f}%")

        print("CreditPath CLI — type 'help' for commands")
        while True:
            try:
                line = input("> ").strip()
            except EOFError:
                print()
                break
            if not line:
                continue
            parts = line.split()
            cmd = parts[0].lower()
            if cmd in ("exit", "quit", "q"):
                break
            if cmd == "help":
                print("Commands: add <amount>, goal <amount>, show, reset, help, exit")
                continue
            if cmd == "add":
                if len(parts) < 2:
                    print("Usage: add <amount>")
                    continue
                try:
                    v = int(parts[1])
                    if v <= 0:
                        raise ValueError
                    state["savings"] += v
                    print(f"Added {v} to savings.")
                    if state["savings"] >= state["goal"]:
                        print("Achievement Unlocked! Savings goal reached!")
                except ValueError:
                    print("Please provide a positive integer amount.")
                continue
            if cmd == "goal":
                if len(parts) < 2:
                    print("Usage: goal <amount>")
                    continue
                try:
                    g = int(parts[1])
                    if g <= 0:
                        raise ValueError
                    state["goal"] = g
                    print(f"Goal set to {g}.")
                except ValueError:
                    print("Please provide a positive integer goal.")
                continue
            if cmd == "show":
                show_state()
                continue
            if cmd == "reset":
                state["savings"] = 0
                state["goal"] = 1000
                print("State reset.")
                continue
            print("Unknown command. Type 'help' for commands.")

if args.cli:
    run_cli()
    sys.exit(0)

if args.test_gui:
    # Try to initialize the GUI without showing it; useful for CI/headless checks.
    try:
        root = tk.Tk()
        root.withdraw()
        app = CreditPathApp(root)
        root.update_idletasks()
        root.destroy()
        print("GUI initialization succeeded")
        sys.exit(0)
    except tk.TclError:
        print("GUI not available (no display). GUI test failed.")
        sys.exit(1)

try:
    root = tk.Tk()
except tk.TclError:
    print("GUI not available (no display). Falling back to CLI.")
    run_cli()
    sys.exit(0)

app = CreditPathApp(root)
root.mainloop()
