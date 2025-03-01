from algorithms.bfs import bfs
from algorithms.a_star import a_star_search
from algorithms.ucs import uniform_cost_search
from algorithms.gbfs import greedy_best_first_search

class AlgorithmFactory:
    @staticmethod
    def create_algorithm(algorithm_name):
        algorithms = {
            'bfs': bfs,
            'a_star': a_star_search,
            'a*': a_star_search,  # Add this line to accept 'a*' as input
            'ucs': uniform_cost_search,
            'gbfs': lambda s, t, d: greedy_best_first_search(s, t, d)
        }
        
        if algorithm_name.lower() not in algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")
            
        return algorithms[algorithm_name.lower()]