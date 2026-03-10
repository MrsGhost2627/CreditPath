"""
CreditPath Financial Tracker
Author: Thaija Wilson

Description:
This program is a financial tracking GUI application built with Python
and CustomTkinter. It allows users to track savings, log debt payments,
set financial goals, and visualize financial progress.

Main Features:
- Add savings
- Log debt payments
- Track savings goal progress
- Display savings vs debt chart
- Save and load financial data
- Summary window showing financial overview
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as mpl

# -------------------- THEME SETUP --------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Custom color palette — money + happiness
COLORS = {
    "bg":           "#0f1a12",      # Deep forest black-green
    "panel":        "#172318",      # Card background
    "accent":       "#2ecc71",      # Emerald green (money)
    "accent2":      "#f1c40f",      # Gold (wealth)
    "accent3":      "#27ae60",      # Deeper green
    "danger":       "#e74c3c",      # Red for debt
    "text":         "#ecf0e8",      # Warm white
    "muted":        "#7f9e82",      # Muted green-grey
    "card_border":  "#2a3d2b",
}

QUOTES = [
    "💰 Save today, enjoy tomorrow!",
    "🌿 Small savings grow into big dreams.",
    "📈 Your future self will thank you!",
    "🏡 Save smart, buy big.",
    "✨ Control your money, control your life!",
    "🌞 Financial freedom is happiness.",
    "🍀 Every dollar saved is a step forward.",
]

LEVELS = [
    (0,    "🌱  Budget Beginner"),
    (1000, "💳  Credit Builder"),
    (2500, "📊  Financial Planner"),
    (5000, "🏠  Home Buyer Ready"),
    (10000,"🚀  Wealth Builder"),
]

# -------------------- MATPLOTLIB STYLE --------------------

mpl.rcParams.update({
    "figure.facecolor":  COLORS["panel"],
    "axes.facecolor":    COLORS["panel"],
    "axes.edgecolor":    COLORS["card_border"],
    "axes.labelcolor":   COLORS["muted"],
    "xtick.color":       COLORS["muted"],
    "ytick.color":       COLORS["muted"],
    "text.color":        COLORS["text"],
    "grid.color":        COLORS["card_border"],
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
})

# -------------------- HELPER WIDGETS --------------------
# These functions create styled widgets to keep the UI consistent and clean.   
def card_frame(parent, **kwargs):
    """A styled card container."""
    return ctk.CTkFrame(
        parent,
        fg_color=COLORS["panel"],
        border_color=COLORS["card_border"],
        border_width=1,
        corner_radius=16,
        **kwargs
    )
#    these helper functions create styled widgets to keep the UI consistent and clean.
def section_label(parent, text, **kwargs):
    return ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont("Georgia", 11),
        text_color=COLORS["muted"],
        **kwargs
    )
# these helper functions create styled widgets to keep the UI consistent and clean.
def value_label(parent, textvariable=None, text="", color=None, **kwargs):
    return ctk.CTkLabel(
        parent,
        textvariable=textvariable,
        text=text,
        font=ctk.CTkFont("Georgia", 22, weight="bold"),
        text_color=color or COLORS["accent"],
        **kwargs
    )
# These helper functions create styled widgets to keep the UI consistent and clean.
def primary_button(parent, text, command, color=None, **kwargs):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color=color or COLORS["accent3"],
        hover_color=COLORS["accent"],
        text_color=COLORS["bg"],
        font=ctk.CTkFont("Georgia", 12, weight="bold"),
        corner_radius=10,
        height=38,
        **kwargs
    )
# These helper functions create styled widgets to keep the UI consistent and clean.
def ghost_button(parent, text, command, **kwargs):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color="transparent",
        border_color=COLORS["card_border"],
        border_width=1,
        hover_color=COLORS["panel"],
        text_color=COLORS["muted"],
        font=ctk.CTkFont("Georgia", 11),
        corner_radius=10,
        height=34,
        **kwargs
    )

# -------------------- MAIN APP --------------------
# The CreditPathApp class encapsulates the entire application, including the UI setup and the logic for handling user interactions and data management.
class CreditPathApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CreditPath – Smart Finance Tracker")
        self.root.geometry("680x860")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg"])
# Initialize state variables for savings, debt, input amounts, and goal. These are linked to the UI and will automatically
        self.savings = ctk.IntVar(value=0)
        self.debt    = ctk.IntVar(value=0)
        self.amount  = ctk.StringVar(value="")
        self.debt_amount = ctk.StringVar(value="")
        self.goal    = ctk.IntVar(value=1000)
# Create the UI widgets and set up the initial state of the application.
        self.create_widgets()
        self.update_chart()
        self.update_progress()

    # -------------------- BUILD UI --------------------
# The create_widgets method constructs the entire user interface, including the header, stats display, input fields, chart, and action buttons. It organizes these components using frames and applies consistent styling throughout the app.
    def create_widgets(self):
        outer = ctk.CTkFrame(self.root, fg_color=COLORS["bg"])
        outer.pack(fill="both", expand=True, padx=20, pady=20)

        # ── Header ──────────────────────────────────────
        header = ctk.CTkFrame(outer, fg_color="transparent")
        header.pack(fill="x", pady=(0, 8))
# The header includes the app title and a subtitle, styled with custom fonts and colors to create an inviting introduction to the app.
        ctk.CTkLabel(
            header,
            text="💚 CreditPath",
            font=ctk.CTkFont("Georgia", 30, weight="bold"),
            text_color=COLORS["accent"]
        ).pack(side="left")
# The subtitle provides a brief description of the app's purpose, reinforcing the theme of smart financial tracking.
        ctk.CTkLabel(
            header,
            text="Smart Credit & Finance Tracker",
            font=ctk.CTkFont("Georgia", 11),
            text_color=COLORS["muted"]
        ).pack(side="left", padx=14, pady=(8, 0))
# The quote label displays a random motivational quote about saving and financial health, adding a touch of personality and encouragement to the user experience.
        self.quote_label = ctk.CTkLabel(
            outer,
            text=random.choice(QUOTES),
            font=ctk.CTkFont("Georgia", 11, slant="italic"),
            text_color=COLORS["accent2"],
        )
        self.quote_label.pack(pady=(0, 10))
# The quote label displays a random motivational quote about saving and financial health, adding a touch of personality and encouragement to the user experience.
        # ── Stats Row ────────────────────────────────────
        stats = ctk.CTkFrame(outer, fg_color="transparent")
        stats.pack(fill="x", pady=(0, 10))
        stats.columnconfigure((0, 1), weight=1)
 
        # Savings card
        scard = card_frame(stats)
        scard.grid(row=0, column=0, padx=(0, 6), sticky="ew")
        section_label(scard, "TOTAL SAVINGS").pack(pady=(14, 0))
        self.savings_display = value_label(scard, textvariable=self.savings, color=COLORS["accent"])
        self.savings_display.pack()
# The level label provides feedback on the user's financial progress, changing as they save more money and reach different milestones.
        self.level_label = ctk.CTkLabel(
            scard,
            text="🌱  Budget Beginner",
            font=ctk.CTkFont("Georgia", 10, slant="italic"),
            text_color=COLORS["accent2"]
        )
        self.level_label.pack(pady=(2, 14))

        # Debt card
        dcard = card_frame(stats)
        dcard.grid(row=0, column=1, padx=(6, 0), sticky="ew")
        section_label(dcard, "CURRENT DEBT").pack(pady=(14, 0))
        self.debt_display = value_label(dcard, textvariable=self.debt, color=COLORS["danger"])
        self.debt_display.pack()
        section_label(dcard, "tracked payments").pack(pady=(2, 14))
# The level label provides feedback on the user's financial progress, changing as they save more money and reach different milestones.
        # ── Goal & Progress ──────────────────────────────
        prog_card = card_frame(outer)
        prog_card.pack(fill="x", pady=(0, 10))
# The goal row contains an entry for the user to set their savings goal, along with a label that shows the percentage of the goal that has been achieved. This allows users to easily track their progress towards their financial goals.
        goal_row = ctk.CTkFrame(prog_card, fg_color="transparent")
        goal_row.pack(fill="x", padx=18, pady=(14, 6))
# The goal row contains an entry for the user to set their savings goal, along with a label that shows the percentage of the goal that has been achieved. This allows users to easily track their progress towards their financial goals.
        section_label(goal_row, "SAVINGS GOAL  $").pack(side="left")
        self.goal_entry = ctk.CTkEntry(
            goal_row,
            textvariable=self.goal,
            width=90,
            fg_color=COLORS["bg"],
            border_color=COLORS["card_border"],
            text_color=COLORS["accent2"],
            font=ctk.CTkFont("Georgia", 13, weight="bold"),
            justify="center"
        )
        self.goal_entry.pack(side="left", padx=8)
        self.goal_entry.bind("<Return>", lambda e: self.update_progress())
        self.goal_entry.bind("<FocusOut>", lambda e: self.update_progress())
# The percentage label updates dynamically to show how close the user is to reaching their savings goal, providing immediate feedback and motivation.
        self.pct_label = ctk.CTkLabel(
            goal_row,
            text="0%",
            font=ctk.CTkFont("Georgia", 12, weight="bold"),
            text_color=COLORS["accent"]
        )
        self.pct_label.pack(side="right")
# The progress bar visually represents the user's progress towards their savings goal, filling up as they save more money. This provides an intuitive and engaging way for users to see their financial progress at a glance.
        self.progress_bar = ctk.CTkProgressBar(
            prog_card,
            width=580,
            height=14,
            progress_color=COLORS["accent"],
            fg_color=COLORS["bg"],
            corner_radius=8,
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=18, pady=(0, 14))

        # ── Input Row ────────────────────────────────────
        inputs = ctk.CTkFrame(outer, fg_color="transparent")
        inputs.pack(fill="x", pady=(0, 10))
        inputs.columnconfigure((0, 1), weight=1)
# The input row contains two sections: one for adding to savings and another for logging debt payments. Each section has an entry field for the user to input an amount and a button to submit the entry. This allows users to easily update their financial data as they save money or make debt payments.
        # Savings input
        sinput = card_frame(inputs)
        sinput.grid(row=0, column=0, padx=(0, 6), sticky="ew")
        section_label(sinput, "ADD TO SAVINGS  $").pack(pady=(12, 4), padx=16, anchor="w")
        self.savings_entry = ctk.CTkEntry(
            sinput,
            textvariable=self.amount,
            placeholder_text="Enter amount",
            fg_color=COLORS["bg"],
            border_color=COLORS["card_border"],
            text_color=COLORS["text"],
            font=ctk.CTkFont("Georgia", 12),
        )
        self.savings_entry.pack(padx=16, fill="x")
        self.savings_entry.bind("<Return>", lambda e: self.add_savings())
        primary_button(sinput, "＋ Add Savings", self.add_savings).pack(
            padx=16, pady=10, fill="x")
# The add savings button allows users to quickly add to their savings total, while the entry field provides a convenient way to input the amount they want to save. This encourages users to actively engage with their financial tracking and make regular updates to their savings data.
        # Debt input
        dinput = card_frame(inputs)
        dinput.grid(row=0, column=1, padx=(6, 0), sticky="ew")
        section_label(dinput, "ADD DEBT PAYMENT  $").pack(pady=(12, 4), padx=16, anchor="w")
        self.debt_entry = ctk.CTkEntry(
            dinput,
            textvariable=self.debt_amount,
            placeholder_text="Enter amount",
            fg_color=COLORS["bg"],
            border_color=COLORS["card_border"],
            text_color=COLORS["text"],
            font=ctk.CTkFont("Georgia", 12),
        )
        self.debt_entry.pack(padx=16, fill="x")
        self.debt_entry.bind("<Return>", lambda e: self.add_debt())
        primary_button(dinput, "＋ Log Payment", self.add_debt,
                       color=COLORS["danger"]).pack(padx=16, pady=10, fill="x")

        # ── Chart ─────────────────────────────────────────
        chart_card = card_frame(outer)
        chart_card.pack(fill="x", pady=(0, 10))
# The chart section uses Matplotlib to create a bar chart that compares the user's total savings and current debt. This visual representation helps users quickly understand their financial situation and track their progress over time.
        self.figure, self.ax = plt.subplots(figsize=(5.8, 2.2))
        self.figure.tight_layout(pad=1.5)
        self.chart_canvas = FigureCanvasTkAgg(self.figure, master=chart_card)
        self.chart_canvas.get_tk_widget().configure(bg=COLORS["panel"])
        self.chart_canvas.get_tk_widget().pack(padx=10, pady=10)

        # ── Action Buttons ───────────────────────────────
        btn_row = ctk.CTkFrame(outer, fg_color="transparent")
        btn_row.pack(fill="x")
        btn_row.columnconfigure((0, 1, 2, 3), weight=1)
# The action buttons at the bottom of the app provide additional functionality, allowing users to view a summary of their financial data, save their progress to a file, load previously saved data, or reset all data to start fresh. These buttons enhance the usability of the app and give users more control over their financial tracking experience.
        btns = [
            ("📋 Summary",   self.open_summary_window, 0),
            ("💾 Save",      self.save_progress,       1),
            ("📂 Load",      self.load_progress,       2),
            ("🔄 Reset",     self.reset_data,          3),
        ]
        for label, cmd, col in btns:
            ghost_button(btn_row, label, cmd).grid(
                row=0, column=col,
                padx=4, sticky="ew"
            )

    # -------------------- LOGIC --------------------
#  The logic section contains methods that handle the core functionality of the app, including parsing user input, updating financial data, refreshing the UI, and managing file operations for saving and loading progress. These methods ensure that the app responds correctly to user interactions and maintains an accurate representation of the user's financial status.
    def _parse_amount(self, var):
        try:
            val = float(var.get().replace(",", "").strip())
            if val <= 0:
                raise ValueError
            return int(val)
        except (ValueError, AttributeError):
            return None
# The _parse_amount method is a helper function that takes a string input from the user, attempts to convert it to a positive integer, and handles any errors that may occur during this process. This ensures that the app only accepts valid numerical input for savings and debt amounts, improving the robustness of the application.
    def add_savings(self):
        val = self._parse_amount(self.amount)
        if val is None:
            messagebox.showerror("Invalid", "Please enter a positive number.")
            return
        self.savings.set(self.savings.get() + val)
        self.amount.set("")
        self.update_progress()
        self.check_level()
        self.update_chart()
        self.show_random_quote()
# The add_savings method is called when the user clicks the "Add Savings" button or presses Enter in the savings entry field. It validates the input, updates the total savings, and refreshes the UI to reflect the new financial status. It also shows a random motivational quote to encourage continued engagement with the app.
    def add_debt(self):
        val = self._parse_amount(self.debt_amount)
        if val is None:
            messagebox.showerror("Invalid", "Please enter a positive number.")
            return
        self.debt.set(self.debt.get() + val)
        self.debt_amount.set("")
        self.update_chart()
        self.show_random_quote()
# The add_debt method is similar to add_savings but updates the total debt instead. It validates the input, updates the debt total, and refreshes the chart to reflect the new financial status. It also shows a random motivational quote to encourage users to stay on track with their financial goals.
    def update_progress(self):
        goal = self.goal.get()
        if goal > 0:
            pct = min(self.savings.get() / goal, 1.0)
            self.progress_bar.set(pct)
            self.pct_label.configure(text=f"{int(pct*100)}%")
            if pct >= 1.0:
                messagebox.showinfo("🎉 Goal Reached!", "You've hit your savings goal!")
# The update_progress method calculates the percentage of the savings goal that has been achieved and updates the progress bar and percentage label accordingly. If the user reaches or exceeds their savings goal, it displays a congratulatory message to celebrate their achievement.
    def check_level(self):
        s = self.savings.get()
        label = LEVELS[0][1]
        for threshold, lvl in LEVELS:
            if s >= threshold:
                label = lvl
        self.level_label.configure(text=label)
# The check_level method checks the user's total savings against predefined thresholds to determine their financial level and updates the level label accordingly. This provides users with feedback on their financial progress and encourages them to continue saving to reach higher levels.
    def update_chart(self):
        self.ax.clear()
        categories = ["Savings", "Debt"]
        values     = [self.savings.get(), self.debt.get()]
        colors     = [COLORS["accent"], COLORS["danger"]]
# The update_chart method refreshes the bar chart to reflect the current savings and debt values. It clears the previous chart, sets up the new bars with appropriate colors, and adds labels to show the exact amounts. This visual update helps users quickly understand their financial situation at a glance.
        bars = self.ax.bar(categories, values, color=colors,
                           width=0.4, edgecolor="none", zorder=3)
        self.ax.yaxis.grid(True, zorder=0)
        self.ax.set_axisbelow(True)
        self.ax.set_title("Savings vs Debt", color=COLORS["text"],
                          fontsize=11, pad=8)
        self.ax.tick_params(labelsize=9)
        self.ax.spines[:].set_visible(False)
# The loop at the end of the update_chart method adds text labels above each bar to show the exact savings and debt amounts in a clear and visually appealing way. This enhances the readability of the chart and provides users with precise information about their financial status.
        for bar, val in zip(bars, values):
            self.ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(values) * 0.02,
                f"${val:,}",
                ha="center", va="bottom",
                color=COLORS["text"], fontsize=9, fontweight="bold"
            )
        self.chart_canvas.draw()
# The show_random_quote method updates the quote label with a randomly selected quote from the QUOTES list. This adds an element of fun and motivation to the app, encouraging users to stay engaged with their financial tracking.
    def show_random_quote(self):
        self.quote_label.configure(text=random.choice(QUOTES))
# The open_summary_window method creates a new window that displays a summary of the user's financial data, including total savings, total debt, net worth, goal progress percentage, and the savings goal. This provides users with a comprehensive overview of their financial status in a clean and organized format.
    def open_summary_window(self):
        win = ctk.CTkToplevel(self.root)
        win.title("Financial Summary")
        win.geometry("340x320")
        win.configure(fg_color=COLORS["bg"])
        win.grab_set()
# The financial summary window calculates key financial metrics such as net worth and goal progress percentage, and displays them in a visually appealing format with appropriate colors to differentiate between positive and negative values. This allows users to quickly assess their overall financial health and progress towards their goals.
        s = self.savings.get()
        d = self.debt.get()
        g = self.goal.get()
        net = s - d
        pct = (s / g * 100) if g else 0
# The financial summary window calculates key financial metrics such as net worth and goal progress percentage, and displays them in a visually appealing format with appropriate colors to differentiate between positive and negative values. This allows users to quickly assess their overall financial health and progress towards their goals.
        ctk.CTkLabel(win, text="📊 Financial Summary",
                     font=ctk.CTkFont("Georgia", 18, weight="bold"),
                     text_color=COLORS["accent"]).pack(pady=(20, 14))
# The financial summary window calculates key financial metrics such as net worth and goal progress percentage, and displays them in a visually appealing format with appropriate colors to differentiate between positive and negative values. This allows users to quickly assess their overall financial health and progress towards their goals.
        rows = [
            ("Total Savings",  f"${s:,}",        COLORS["accent"]),
            ("Total Debt",     f"${d:,}",         COLORS["danger"]),
            ("Net Worth",      f"${net:,}",       COLORS["accent2"]),
            ("Goal Progress",  f"{pct:.1f}%",     COLORS["text"]),
            ("Savings Goal",   f"${g:,}",         COLORS["muted"]),
        ]
        for label, val, color in rows:
            row = ctk.CTkFrame(win, fg_color="transparent")
            row.pack(fill="x", padx=30, pady=3)
            ctk.CTkLabel(row, text=label,
                         font=ctk.CTkFont("Georgia", 12),
                         text_color=COLORS["muted"]).pack(side="left")
            ctk.CTkLabel(row, text=val,
                         font=ctk.CTkFont("Georgia", 13, weight="bold"),
                         text_color=color).pack(side="right")
# The close button allows users to easily exit the financial summary window and return to the main app interface. It is styled consistently with the rest of the app to maintain a cohesive user experience.
        ctk.CTkButton(win, text="Close", command=win.destroy,
                      fg_color=COLORS["card_border"],
                      hover_color=COLORS["accent3"],
                      text_color=COLORS["text"],
                      corner_radius=10).pack(pady=20)
# The save_progress method allows users to save their current financial data to a JSON file. It prompts the user to choose a location and filename for the saved data, and then writes the savings, debt, and goal values to the file. This enables users to preserve their progress and load it later if needed.
    def save_progress(self):
        data = {
            "savings": self.savings.get(),
            "debt":    self.debt.get(),
            "goal":    self.goal.get()
        }
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if path:
            with open(path, "w") as f:
                json.dump(data, f)
            messagebox.showinfo("Saved", "Progress saved! 💾")
# The load_progress method allows users to load previously saved financial data from a JSON file. It prompts the user to select a file, reads the savings, debt, and goal values from the file, and updates the app's state accordingly. This enables users to easily restore their financial tracking data and continue where they left off.
    def load_progress(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                self.savings.set(data.get("savings", 0))
                self.debt.set(data.get("debt", 0))
                self.goal.set(data.get("goal", 1000))
                self.update_progress()
                self.check_level()
                self.update_chart()
                messagebox.showinfo("Loaded", "Progress loaded! 📂")
            except Exception:
                messagebox.showerror("Error", "Could not load file.")
# The reset_data method allows users to reset all financial data to its initial state. It prompts the user for confirmation before clearing the savings, debt, and goal values, and then updates the UI to reflect the reset state. This provides users with a way to start fresh if they want to track new financial goals or simply clear their current data.
    def reset_data(self):
        if messagebox.askyesno("Reset", "Reset all data?"):
            self.savings.set(0)
            self.debt.set(0)
            self.goal.set(1000)
            self.amount.set("")
            self.debt_amount.set("")
            self.progress_bar.set(0)
            self.pct_label.configure(text="0%")
            self.level_label.configure(text="🌱  Budget Beginner")
            self.update_chart()

# -------------------- ENTRY POINT --------------------

if __name__ == "__main__":
    root = ctk.CTk()
    app = CreditPathApp(root)
    root.mainloop()
