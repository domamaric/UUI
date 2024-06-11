import csv
import math
import random


def read_csv(filepath):
    cities_dict = {}

    with open(filepath, mode="r") as f:
        reader = csv.DictReader(f)
        for line in reader:
            cities_dict[line["city"]] = (float(line["x_coordinate"]),
                                         float(line["y_coordinate"]))

    return cities_dict


class AntColony:
    def __init__(self, epochs, alpha, beta, decay, ant_count):
        self._epochs = epochs
        self._alpha = alpha
        self._beta = beta
        self._decay = decay
        self._ant_count = ant_count

    def _distance(self, city1, city2):
        return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

    def _initialize_pheromones(self, cities):
        pheromones = {}
        for city1 in cities:
            for city2 in cities:
                if city1 != city2:
                    pheromones[(city1, city2)] = 1.0  # initial pheromone level

        return pheromones

    def _update_pheromones(self, pheromones, all_solutions):
        for (city1, city2) in pheromones:
            pheromones[(city1, city2)] *= (1 - self._decay)  # evaporate pheromones

        for solution, cost in all_solutions:
            for i in range(len(solution) - 1):
                city1, city2 = solution[i], solution[i + 1]
                pheromones[(city1, city2)] += 1.0 / cost  # deposit pheromones

    def _construct_solution(self, cities, pheromones):
        solution = []
        unvisited = set(cities.keys())
        current_city = random.choice(list(unvisited))
        solution.append(current_city)
        unvisited.remove(current_city)

        while unvisited:
            probabilities = []
            total = 0
            for next_city in unvisited:
                pheromone_level = pheromones[(current_city, next_city)] ** self._alpha
                visibility = (1.0 / self._distance(cities[current_city], cities[next_city])) ** self._beta
                prob = pheromone_level * visibility
                probabilities.append((next_city, prob))
                total += prob

            if total == 0:
                next_city = random.choice(list(unvisited))
            else:
                r = random.uniform(0, total)
                cumulative_prob = 0
                for next_city, prob in probabilities:
                    cumulative_prob += prob
                    if r <= cumulative_prob:
                        break

            solution.append(next_city)
            unvisited.remove(next_city)
            current_city = next_city

        solution.append(solution[0])  # return to the starting city
        return solution

    def _calculate_cost(self, solution, cities):
        cost = 0
        for i in range(len(solution) - 1):
            cost += self._distance(cities[solution[i]], cities[solution[i + 1]])
        return cost

    def fit(self, cities):
        pheromones = self._initialize_pheromones(cities)
        best_solution = None
        best_cost = float('inf')

        for epoch in range(self._epochs):
            all_solutions = []
            for _ in range(self._ant_count):
                solution = self._construct_solution(cities, pheromones)
                cost = self._calculate_cost(solution, cities)
                all_solutions.append((solution, cost))
                if cost < best_cost:
                    best_solution = solution
                    best_cost = cost

            self._update_pheromones(pheromones, all_solutions)

            print(f'Epoch {epoch+1}/{self._epochs}, Best Cost: {best_cost:.4f}')

        return best_solution, best_cost
