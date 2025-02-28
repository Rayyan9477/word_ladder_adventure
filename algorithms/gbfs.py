def greedy_best_first_search(start_word, target_word, word_dict, heuristic=None):
    """Greedy Best-First Search algorithm implementation
    
    Args:
        start_word: The starting word
        target_word: The target word to reach
        word_dict: Dictionary of valid words
        heuristic: Optional heuristic function, defaults to Hamming distance if None
    
    Returns:
        A list representing the path from start word to target word, or None if no path exists
    """
    from queue import PriorityQueue

    # Use default heuristic if none provided
    if heuristic is None:
        heuristic = lambda word, target: sum(1 for a, b in zip(word, target) if a != b)
    
    # Priority queue to store the words to explore
    open_set = PriorityQueue()
    open_set.put((0, start_word))
    
    # Dictionary to keep track of the best path to each word
    came_from = {}
    
    # Keep track of visited words to avoid cycles
    visited = set([start_word])
    
    while not open_set.empty():
        current_cost, current_word = open_set.get()

        # If we reached the target word, reconstruct the path
        if current_word == target_word:
            return reconstruct_path(came_from, current_word)

        # Explore neighbors (valid transformations)
        for neighbor in get_neighbors(current_word, word_dict):
            if neighbor in visited:
                continue
                
            visited.add(neighbor)
            
            # Record the best path to the neighbor
            came_from[neighbor] = current_word
                
            # Calculate the priority based solely on the heuristic
            priority = heuristic(neighbor, target_word)
            open_set.put((priority, neighbor))

    return None  # No path found

def get_neighbors(word, word_dict):
    """Get all possible one-letter transformations that result in valid words"""
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
    """Reconstruct the path from start word to target word"""
    total_path = [current_word]
    while current_word in came_from:
        current_word = came_from[current_word]
        total_path.append(current_word)
    return total_path[::-1]  # Reverse to get path from start to end