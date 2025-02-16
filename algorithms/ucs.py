from queue import PriorityQueue

class Node:
    def __init__(self, word, cost, parent=None):
        self.word = word
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost

def uniform_cost_search(start_word, target_word, word_dict):
    if start_word == target_word:
        return [start_word]

    visited = set()
    priority_queue = PriorityQueue()
    priority_queue.put(Node(start_word, 0))

    while not priority_queue.empty():
        current_node = priority_queue.get()
        current_word = current_node.word

        if current_word in visited:
            continue
        visited.add(current_word)

        for neighbor in get_neighbors(current_word, word_dict):
            if neighbor == target_word:
                return reconstruct_path(current_node, neighbor)

            new_cost = current_node.cost + 1  # Assuming each transformation has a cost of 1
            priority_queue.put(Node(neighbor, new_cost, current_node))

    return None

def get_neighbors(word, word_dict):
    neighbors = []
    for i in range(len(word)):
        for char in 'abcdefghijklmnopqrstuvwxyz':
            if char != word[i]:
                new_word = word[:i] + char + word[i+1:]
                if new_word in word_dict:
                    neighbors.append(new_word)
    return neighbors

def reconstruct_path(node, target_word):
    path = []
    while node is not None:
        path.append(node.word)
        node = node.parent
    path.reverse()
    return path