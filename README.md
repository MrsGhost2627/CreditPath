<<<<<<< Updated upstream
CreditPath is a Python tkinter GUI application that allows users to track savings, manage debt, set financial goals, and visualize progress.

Features
-Add savings
-Record debt payments
-Set savings goal
-Progress bar tracking
-Savings vs Debt bar chart (matplotlib)
-Motivational quotes
-Financial level system
-Save progress to JSON
-Load saved progress
-Reset data

Summary window
-Secure input validation
Technologies Used
-Python 3
-tkinter
-matplotlib
-JSON

Object-Oriented Programming

How to Run
Install matplotlib:
pip install matplotlib

Run the program:
python creditpath.py
Project Structure
creditpath.py – Main application file
README.md – Project documentation

Author: Thaija Wilson
=======
# CreditPath – Smart Credit & Finance Tracker

CreditPath is a Python Tkinter GUI application designed to teach financial literacy
and credit management. It helps users track savings goals, understand responsible
credit habits, and prepare for major purchases such as buying a home.

## Features

## Technologies Used

## Target Audience
High school students learning economics and adults interested in basic financial planning.

## Automated GUI test (headless)

If you need to verify the Tk GUI can initialize in a headless environment (CI or server), use the included wrapper script. It uses `xvfb-run` when available and falls back to a quick headless check.

Usage:

```bash
./scripts/run_gui_test.sh
```

If `xvfb-run` is not installed, install it on Debian/Ubuntu with:

# CreditPath – Smart Credit & Finance Tracker

CreditPath is a Python Tkinter GUI application that helps users track savings,
manage debt, set financial goals, and visualize progress. It is designed to
teach financial literacy and responsible credit habits.

## Features
- Add savings
- Record debt payments
- Set savings goal
- Progress bar tracking
- Savings vs Debt chart (requires matplotlib)
- Motivational quotes
- Financial level system
- Save/load progress (JSON)
- Reset data

## Summary & Design
- Secure input validation
- Object-oriented structure

## Technologies Used
- Python 3
- tkinter
- matplotlib (optional)
- JSON for persistence

## How to Run
Install optional plotting dependency (if using charts):

```bash
pip install matplotlib
```

Run the program:

```bash
python WilsonThaija.py
```

Project Structure
- `WilsonThaija.py` – Main application file
- `README.md` – Project documentation

Author: Thaija Wilson

## Target Audience
High school students learning economics and adults interested in basic financial planning.

## Automated GUI test (headless)

If you need to verify the Tk GUI can initialize in a headless environment (CI or server), use the included wrapper script. It uses `xvfb-run` when available and falls back to a quick headless check.

Usage:

```bash
./scripts/run_gui_test.sh
```

If `xvfb-run` is not installed, install it on Debian/Ubuntu with:

```bash
sudo apt-get update
sudo apt-get install -y xvfb
```

Or run the faster headless check without Xvfb:

```bash
python3 WilsonThaija.py --test-gui
```
