def greedy_best_first_search(start_word, target_word, word_dict, heuristic=None):

    from queue import PriorityQueue

    if heuristic is None:
        heuristic = lambda word, target: sum(1 for a, b in zip(word, target) if a != b)
    
    open_set = PriorityQueue()
    open_set.put((0, start_word))
    
    came_from = {}
    
    visited = set([start_word])
    
    while not open_set.empty():
        current_cost, current_word = open_set.get()

        if current_word == target_word:
            return reconstruct_path(came_from, current_word)

        for neighbor in get_neighbors(current_word, word_dict):
            if neighbor in visited:
                continue
                
            visited.add(neighbor)
            
            came_from[neighbor] = current_word
                
            priority = heuristic(neighbor, target_word)
            open_set.put((priority, neighbor))

    return None  

def get_neighbors(word, word_dict):
    neighbors = []
    for i in range(len(word)):
        for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if char == word[i]:
                continue
            neighbor = word[:i] + char + word[i+1:]
            if neighbor in word_dict:
                neighbors.append(neighbor)
    return neighbors

def reconstruct_path(came_from, current_word):
    total_path = [current_word]
    while current_word in came_from:
        current_word = came_from[current_word]
        total_path.append(current_word)
    return total_path[::-1]  