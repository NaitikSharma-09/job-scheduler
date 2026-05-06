from genetic_algorithm import create_population, select_best, crossover, mutate, fitness

def genetic_schedule(jobs, num_cpus=2):
    population = create_population(jobs)

    for _ in range(20):
        best = select_best(population, num_cpus)

        new_population = best[:]

        while len(new_population) < len(population):
            child = crossover(best[0], best[1])
            child = mutate(child)
            new_population.append(child)

        population = new_population

    return sorted(population, key=lambda s: fitness(s, num_cpus))[0]