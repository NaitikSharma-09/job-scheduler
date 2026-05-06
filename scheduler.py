from genetic_algorithm import create_population, select_best, crossover, mutate, fitness
import random

def genetic_schedule(jobs, num_cpus=2):
    population = create_population(jobs, size=20)

    for _ in range(50):
        best = select_best(population, num_cpus)

        new_population = best[:]

        while len(new_population) < len(population):
            parent1, parent2 = random.sample(best, 2)
            child = crossover(parent1, parent2)

            if random.random() < 0.3:
                child = mutate(child)

            new_population.append(child)

        population = new_population

    return sorted(population, key=lambda s: fitness(s, num_cpus))[0]

def genetic_schedule_live(jobs, num_cpus=2):
    population = create_population(jobs, size=20)
    history = []

    for _ in range(50):
        best = select_best(population, num_cpus)

        best_score = fitness(best[0], num_cpus)
        history.append(best_score)

        new_population = best[:]

        while len(new_population) < len(population):
            parent1, parent2 = random.sample(best, 2)
            child = crossover(parent1, parent2)

            if random.random() < 0.3:
                child = mutate(child)

            new_population.append(child)

        population = new_population

    return best[0], history