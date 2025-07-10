import tkinter as tk
from tkinter import messagebox, ttk
import pulp

# Initialize main GUI window
root = tk.Tk()
root.title("Job Scheduling Optimizer")
root.geometry("600x400")

jobs = []

# Function to add job details
def add_job():
    name = entry_name.get()
    duration = entry_duration.get()
    deadline = entry_deadline.get()

    if not name or not duration or not deadline:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        duration = int(duration)
        deadline = int(deadline)
    except ValueError:
        messagebox.showerror("Input Error", "Duration and Deadline must be integers.")
        return

    jobs.append({'name': name, 'duration': duration, 'deadline': deadline})
    update_job_list()
    entry_name.delete(0, tk.END)
    entry_duration.delete(0, tk.END)
    entry_deadline.delete(0, tk.END)

# Display job list in GUI
def update_job_list():
    job_list.delete(*job_list.get_children())
    for idx, job in enumerate(jobs):
        job_list.insert("", "end", values=(idx + 1, job['name'], job['duration'], job['deadline']))

# Optimization function using Integer Programming
def optimize_schedule():
    if not jobs:
        messagebox.showwarning("No Jobs", "Add at least one job.")
        return

    n = len(jobs)
    prob = pulp.LpProblem("Job_Scheduling", pulp.LpMinimize)

    # Decision Variables: start time for each job
    start_times = [pulp.LpVariable(f'start_{i}', lowBound=0, cat='Integer') for i in range(n)]
    completion_times = [start_times[i] + jobs[i]['duration'] for i in range(n)]

    # Objective: Minimize total tardiness
    tardiness = [pulp.LpVariable(f'tardiness_{i}', lowBound=0, cat='Integer') for i in range(n)]
    prob += pulp.lpSum(tardiness)

    # Constraints
    for i in range(n):
        # Completion time should be greater than or equal to job's start time + duration
        prob += completion_times[i] >= start_times[i] + jobs[i]['duration']
        
        # Tardiness constraint: Tardiness occurs if completion time is greater than deadline
        prob += tardiness[i] >= completion_times[i] - jobs[i]['deadline']
    
    # Ensure that jobs are scheduled in a sequence (i.e., no overlap)
    for i in range(1, n):
        prob += start_times[i] >= completion_times[i - 1]

    # Solve the optimization problem
    prob.solve()

    if prob.status == 1:
        result_text.delete(1.0, tk.END)
        for i in range(n):
            result_text.insert(tk.END, f"Job: {jobs[i]['name']}, Start: {pulp.value(start_times[i])}, "
                                       f"Completion: {pulp.value(completion_times[i])}, "
                                       f"Tardiness: {pulp.value(tardiness[i])}\n")
    else:
        messagebox.showerror("Optimization Error", "Failed to find an optimal solution.")

# GUI Elements
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Job Name:").grid(row=0, column=0, padx=5)
entry_name = tk.Entry(frame_inputs)
entry_name.grid(row=0, column=1, padx=5)

tk.Label(frame_inputs, text="Duration:").grid(row=0, column=2, padx=5)
entry_duration = tk.Entry(frame_inputs)
entry_duration.grid(row=0, column=3, padx=5)

tk.Label(frame_inputs, text="Deadline:").grid(row=0, column=4, padx=5)
entry_deadline = tk.Entry(frame_inputs)
entry_deadline.grid(row=0, column=5, padx=5)

btn_add = tk.Button(root, text="Add Job", command=add_job)
btn_add.pack(pady=5)

# Job list table
columns = ("#", "Name", "Duration", "Deadline")
job_list = ttk.Treeview(root, columns=columns, show='headings', height=5)
for col in columns:
    job_list.heading(col, text=col)
job_list.pack(pady=10)

btn_optimize = tk.Button(root, text="Optimize Schedule", command=optimize_schedule)
btn_optimize.pack(pady=5)

result_text = tk.Text(root, height=10)
result_text.pack(pady=10)

root.mainloop()
