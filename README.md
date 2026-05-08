# 🧬 Parallel Genetic Algorithm Job Scheduler

## 🚀 Overview
This project implements a job scheduling system using a Genetic Algorithm to optimize task distribution across multiple CPUs.

## 🔥 Features
- Genetic Algorithm optimization
- Multi-CPU scheduling
- Load balancing
- Random job generation
- Visualization of CPU usage

## 🧠 How it works
1. Generate random job schedules
2. Evaluate using fitness function (makespan)
3. Select best solutions
4. Apply crossover & mutation
5. Repeat for multiple generations

## 📊 Output
- Optimized job assignment
- CPU load distribution graph

## 🛠️ Technologies Used
- Python
- Genetic Algorithms
- Multiprocessing
- Matplotlib

## ▶️ Run the project

### 1) Backend setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run CLI scheduler

```bash
python3 main.py
```

### 3) Run web app

```bash
python3 app.py
```

Open `http://127.0.0.1:5000/login` and log in with:
- username: `admin`
- password: `123456`

### 4) Frontend (optional)

```bash
cd frontend
npm install
npm run dev
```