import random

def create_population(jobs, size=5):
    population = []
    for _ in range(size):
        individual = jobs[:]
        random.shuffle(individual)
        population.append(individual)
    return population


def fitness(schedule, num_cpus=2):
    cpu_times = [0] * num_cpus

    for i, job in enumerate(schedule):
        cpu_index = i % num_cpus
        cpu_times[cpu_index] += job.execution_time

    return max(cpu_times)  # minimize this

def select_best(population, num_cpus):
    return sorted(population, key=lambda s: fitness(s, num_cpus))[:2]

def crossover(parent1, parent2):
    point = len(parent1) // 2
    child = parent1[:point]

    for job in parent2:
        if job not in child:
            child.append(job)

    return child


def mutate(schedule):
    i, j = random.sample(range(len(schedule)), 2)
    schedule[i], schedule[j] = schedule[j], schedule[i]
    return schedule