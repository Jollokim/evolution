import numpy as np

class Individual:
    def __init__(self, genom: np.ndarray) -> None:
        self.genom = genom

    def get_fitness(self):
        count_ones = 0

        for gene in self.genom:
            if gene == 1:
                count_ones += 1

        return count_ones

    def is_perfect_individual(self):
        if self.get_fitness() == len(self.genom):
            return True

        return False

    def __str__(self) -> str:
        return f'Individual: fitness={self.get_fitness()}, genom={self.genom}'