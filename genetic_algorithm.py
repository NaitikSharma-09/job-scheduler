import random
from multiprocessing import Pool


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

    makespan = max(cpu_times)
    imbalance = max(cpu_times) - min(cpu_times)

    return makespan + imbalance  # lower is better
    return max(cpu_times)  # minimize this
def select_best(population, num_cpus):
    scores = parallel_fitness(population, num_cpus)
    paired = list(zip(population, scores))
    paired.sort(key=lambda x: x[1])
    return [p[0] for p in paired[:4]]

def crossover(parent1, parent2):
    point = len(parent1) // 2
    child = parent1[:point]

    for job in parent2:
        if job not in child:
            child.append(job)

    return child


def mutate(schedule):
    import random

    if random.random() < 0.5:
        i, j = random.sample(range(len(schedule)), 2)
        schedule[i], schedule[j] = schedule[j], schedule[i]
    return schedule
    from multiprocessing import Pool

def parallel_fitness(population, num_cpus):
    with Pool() as pool:
        scores = pool.starmap(fitness, [(ind, num_cpus) for ind in population])
    return scores