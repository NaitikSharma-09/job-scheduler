import os
import random
from functools import wraps

import matplotlib.pyplot as plt
from flask import Flask, jsonify, redirect, render_template_string, request, session, url_for
from flask_socketio import SocketIO

from job import Job
from scheduler import genetic_schedule_live

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

USERS = {"admin": {"password": "123456"}}


def is_authenticated():
    return bool(session.get("user_id"))


def login_required(view_fn):
    @wraps(view_fn)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            if request.path.startswith("/api/"):
                return jsonify({"ok": False, "error": "Unauthorized"}), 401
            return redirect(url_for("login"))
        return view_fn(*args, **kwargs)

    return wrapper


def predict_priority_label(execution_time, memory):
    # Lightweight rules approximating a simple classifier.
    score = execution_time * 0.7 + memory * 0.3
    if score >= 5:
        return "High"
    if score >= 3:
        return "Medium"
    return "Low"


def parse_positive_int(value, fallback):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return fallback
    return parsed if parsed > 0 else fallback

HTML = """
<h1>🧬 Genetic Job Scheduler</h1>
<p>
{% if current_user.is_authenticated %}
Logged in as <b>{{ current_user.id }}</b> |
<a href="/dashboard">Dashboard</a> |
<a href="/logout">Logout</a>
{% else %}
<a href="/login">Login</a>
{% endif %}
</p>

<form method="post">
    Jobs: <input type="number" name="jobs" value="10"><br><br>
    CPUs: <input type="number" name="cpus" value="2"><br><br>
    <button type="submit">Run</button>
</form>

{% if result %}
<h2>Result:</h2>
<pre>{{ result }}</pre>
<h3>Live Genetic Updates</h3>
<pre id="live-feed">Waiting for next run...</pre>

<h2>📊 CPU Load</h2>
<img src="/static/cpu_load.png" width="400">

<h2>📈 Evolution</h2>
<img src="/static/evolution.png" width="400">
{% endif %}

<script src="https://cdn.socket.io/4.0.1/socket.io.min.js"></script>
<script>
const socket = io();
const liveFeed = document.getElementById("live-feed");
const lines = [];
socket.on("update_graph", (data) => {
  const line = `Generation ${data.generation}: fitness ${data.fitness}`;
  lines.push(line);
  if (lines.length > 20) lines.shift();
  if (liveFeed) liveFeed.textContent = lines.join("\\n");
});
</script>
"""

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    result = None

    if request.method == "POST":
        num_jobs = parse_positive_int(request.form.get("jobs"), 10)
        num_cpus = parse_positive_int(request.form.get("cpus"), 2)

        jobs = [Job(i, random.randint(1, 10)) for i in range(1, num_jobs + 1)]

        def on_generation(generation, best_score):
            socketio.emit(
                "update_graph",
                {"generation": generation, "fitness": best_score},
            )

        best_schedule, history = genetic_schedule_live(
            jobs, num_cpus, on_generation=on_generation
        )

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

    current_user = {"is_authenticated": is_authenticated(), "id": session.get("user_id")}
    return render_template_string(HTML, result=result, current_user=current_user)


@app.route("/run")
@login_required
def run_scheduler():
    num_jobs = parse_positive_int(request.args.get("jobs"), 10)
    num_cpus = parse_positive_int(request.args.get("cpus"), 2)
    jobs = [Job(i, random.randint(1, 10)) for i in range(1, num_jobs + 1)]
    best_schedule, _ = genetic_schedule_live(jobs, num_cpus)
    output = [f"CPU {(i % num_cpus) + 1} -> Job {job.id} ({job.execution_time}s)" for i, job in enumerate(best_schedule)]
    return {"result": "\n".join(output)}


@app.route("/api/run")
@login_required
def api_run_scheduler():
    return run_scheduler()


@app.route("/api/predict-priority", methods=["POST"])
@login_required
def predict_priority():
    payload = request.get_json(silent=True) or {}
    try:
        execution_time = float(payload.get("execution_time", 1))
        memory = float(payload.get("memory", 1))
    except (TypeError, ValueError):
        return jsonify({"ok": False, "error": "execution_time and memory must be numbers"}), 400

    if execution_time <= 0 or memory <= 0:
        return jsonify({"ok": False, "error": "execution_time and memory must be > 0"}), 400
    prediction = predict_priority_label(execution_time, memory)
    return jsonify(
        {
            "execution_time": execution_time,
            "memory": memory,
            "predicted_priority": prediction,
        }
    )


@app.route("/dashboard")
@login_required
def dashboard():
    return "Protected"


LOGIN_HTML = """
<h2>Login</h2>
<form method="post">
  Username: <input name="username" value="admin"><br><br>
  Password: <input name="password" type="password" value="123456"><br><br>
  <button type="submit">Login</button>
</form>
{% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
"""


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = USERS.get(username)
        if user and user["password"] == password:
            session["user_id"] = username
            return redirect(url_for("home"))
        return render_template_string(LOGIN_HTML, error="Invalid credentials")
    return render_template_string(LOGIN_HTML, error=None)


@app.route("/api/login", methods=["POST"])
def api_login():
    payload = request.get_json(silent=True) or {}
    username = payload.get("username", "")
    password = payload.get("password", "")
    user = USERS.get(username)
    if user and user["password"] == password:
        session["user_id"] = username
        return jsonify({"ok": True, "user": username})
    return jsonify({"ok": False, "error": "Invalid credentials"}), 401


@app.route("/logout")
@login_required
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


@app.route("/api/logout", methods=["POST"])
@login_required
def api_logout():
    session.pop("user_id", None)
    return jsonify({"ok": True})


if __name__ == "__main__":
    socketio.run(app, debug=True)