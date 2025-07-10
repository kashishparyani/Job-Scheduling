# 🛠️ Job Scheduling Optimizer (Tkinter + PuLP)

This is a Python GUI-based Job Scheduling Optimizer using Integer Linear Programming. Users can input job details (name, duration, and deadline), and the program will compute an optimal schedule that minimizes total tardiness.

## 🚀 Features

- Add multiple jobs with custom name, duration, and deadline
- View added jobs in a table format
- Solve using Integer Linear Programming (via PuLP)
- Display optimal start time, completion time, and tardiness for each job
- Simple and user-friendly Tkinter interface

## 🧰 Requirements

- Python 3.x
- `pulp` library

Install PuLP via pip:
```bash
pip install pulp
