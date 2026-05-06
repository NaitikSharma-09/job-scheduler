import tkinter as tk
from job import Job
from scheduler import genetic_schedule
import random

def run_scheduler():
    jobs = [Job(i, random.randint(1, 10)) for i in range(1, 11)]
    result = genetic_schedule(jobs, num_cpus=2)

    output.delete("1.0", tk.END)

    cpu_times = [0, 0]

    for i, job in enumerate(result):
        cpu_index = i % 2
        cpu_times[cpu_index] += job.execution_time
        output.insert(tk.END, f"CPU {cpu_index+1} → Job {job.id} ({job.execution_time}s)\n")

    output.insert(tk.END, f"\nMakespan: {max(cpu_times)}")


# UI
root = tk.Tk()
root.title("Genetic Algorithm Scheduler")

btn = tk.Button(root, text="Run Scheduler", command=run_scheduler)
btn.pack()

output = tk.Text(root, height=20, width=50)
output.pack()

root.mainloop()