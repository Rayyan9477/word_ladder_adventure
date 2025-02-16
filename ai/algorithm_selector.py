from algorithms.ucs import UniformCostSearch
from algorithms.a_star import AStarSearch
from algorithms.bfs import BreadthFirstSearch
from algorithms.gbfs import GreedyBestFirstSearch

class AlgorithmSelector:
    def __init__(self):
        self.algorithms = {
            "Uniform Cost Search": UniformCostSearch(),
            "A* Search": AStarSearch(),
            "Breadth-First Search": BreadthFirstSearch(),
            "Greedy Best-First Search": GreedyBestFirstSearch()
        }
        self.selected_algorithm = None

    def select_algorithm(self, algorithm_name):
        if algorithm_name in self.algorithms:
            self.selected_algorithm = self.algorithms[algorithm_name]
            return f"{algorithm_name} selected."
        else:
            return "Invalid algorithm selection."

    def get_selected_algorithm(self):
        return self.selected_algorithm

    def list_algorithms(self):
        return list(self.algorithms.keys())