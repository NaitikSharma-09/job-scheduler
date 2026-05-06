from job import Job
from scheduler import genetic_schedule

def main():
    jobs = [
        Job(1, 5),
        Job(2, 2),
        Job(3, 8),
        Job(4, 3)
    ]

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

if __name__ == "__main__":
    main()