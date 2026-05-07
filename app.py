from flask import Flask, render_template_string, request
from job import Job
from scheduler import genetic_schedule_live
import random
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Genetic Scheduler Dashboard</title>

    <style>
        body {
            background-color: #0f172a;
            color: white;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 40px;
        }

        .container {
            max-width: 1000px;
            margin: auto;
        }

        h1 {
            text-align: center;
            color: #38bdf8;
            margin-bottom: 30px;
        }

        .card {
            background: #1e293b;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
        }

        input {
            padding: 10px;
            width: 100%;
            margin-top: 10px;
            margin-bottom: 20px;
            border-radius: 8px;
            border: none;
            background: #334155;
            color: white;
        }

        button {
            background: #38bdf8;
            color: black;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            width: 100%;
        }

        button:hover {
            background: #0ea5e9;
        }

        pre {
            background: #0f172a;
            padding: 15px;
            border-radius: 10px;
            overflow-x: auto;
        }

        .graphs {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }

        .graphs img {
            width: 450px;
            border-radius: 12px;
            background: white;
            padding: 10px;
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            color: #94a3b8;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>🧬 Genetic Algorithm Scheduler</h1>

    <div class="card">
        <form method="post">

            <label>Number of Jobs</label>
            <input type="number" name="jobs" value="10">

            <label>Number of CPUs</label>
            <input type="number" name="cpus" value="2">

            <button type="submit">Run Scheduler</button>

        </form>
    </div>

    {% if result %}

    <div class="card">
        <h2>📋 Scheduling Result</h2>
        <pre>{{ result }}</pre>
    </div>

    <div class="card">
        <h2>📊 Analytics</h2>

        <div class="graphs">
            <div>
                <h3>CPU Load</h3>
                <img src="/static/cpu_load.png">
            </div>

            <div>
                <h3>Evolution Graph</h3>
                <img src="/static/evolution.png">
            </div>
        </div>
    </div>

    {% endif %}

    <div class="footer">
        Built with Python, Flask & Genetic Algorithms 🚀
    </div>

</div>

</body>
</html>
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