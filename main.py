import matplotlib.pyplot as plt
import random
from job import Job
from scheduler import genetic_schedule

def main():
    # Random jobs
    jobs = [Job(i, random.randint(1, 10)) for i in range(1, 11)]

    best_schedule = genetic_schedule(jobs, num_cpus=2)

    print("Best Schedule Across CPUs:\n")

    cpu_times = [0, 0]
    cpu_jobs = [[], []]

    for i, job in enumerate(best_schedule):
        cpu_index = i % 2
        cpu_jobs[cpu_index].append(job)
        cpu_times[cpu_index] += job.execution_time

    for i in range(2):
        print(f"CPU {i+1}:")
        for job in cpu_jobs[i]:
            print(f"  Job {job.id} -> {job.execution_time}s")
        print(f"  Total: {cpu_times[i]}s\n")

    print(f"Best makespan: {max(cpu_times)}")

    # ✅ Visualization (FIXED - inside main)
    cpu_labels = [f"CPU {i+1}" for i in range(len(cpu_times))]

    plt.bar(cpu_labels, cpu_times)
    plt.xlabel("CPUs")
    plt.ylabel("Execution Time")
    plt.title("CPU Load Distribution")

    plt.savefig("cpu_load.png")
    print("Graph saved as cpu_load.png")

    plt.clf()  # optional: clears plot for next run


if __name__ == "__main__":
    main()