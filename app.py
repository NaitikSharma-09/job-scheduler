from flask import Flask, render_template_string, request
from job import Job
from scheduler import genetic_schedule_live
import random
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

HTML = """
<h1>🧬 Genetic Job Scheduler</h1>

<form method="post">
    Jobs: <input type="number" name="jobs" value="10"><br><br>
    CPUs: <input type="number" name="cpus" value="2"><br><br>
    <button type="submit">Run</button>
</form>

{% if result %}
<h2>Result:</h2>
<pre>{{ result }}</pre>

<h2>📊 CPU Load</h2>
<img src="/static/cpu_load.png" width="400">

<h2>📈 Evolution</h2>
<img src="/static/evolution.png" width="400">
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        num_jobs = int(request.form["jobs"])
        num_cpus = int(request.form["cpus"])

        jobs = [Job(i, random.randint(1, 10)) for i in range(1, num_jobs + 1)]

        best_schedule, history = genetic_schedule_live(jobs, num_cpus)

        cpu_times = [0] * num_cpus
        output = ""

        for i, job in enumerate(best_schedule):
            cpu_index = i % num_cpus
            cpu_times[cpu_index] += job.execution_time
            output += f"CPU {cpu_index+1} → Job {job.id} ({job.execution_time}s)\n"

        output += f"\nMakespan: {max(cpu_times)}"
        result = output

        # 🔷 Ensure static folder exists
        os.makedirs("static", exist_ok=True)

        # =====================
        # 📊 CPU LOAD GRAPH
        # =====================
        cpu_labels = [f"CPU {i+1}" for i in range(num_cpus)]

        plt.bar(cpu_labels, cpu_times)
        plt.xlabel("CPUs")
        plt.ylabel("Execution Time")
        plt.title("CPU Load")

        plt.savefig("static/cpu_load.png")
        plt.clf()

        # =====================
        # 📈 EVOLUTION GRAPH
        # =====================
        plt.plot(history)
        plt.xlabel("Generation")
        plt.ylabel("Makespan")
        plt.title("Evolution")

        plt.savefig("static/evolution.png")
        plt.clf()

    return render_template_string(HTML, result=result)


if __name__ == "__main__":
 app.run(debug=True, port=5001)