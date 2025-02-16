def greedy_best_first_search(start_word, target_word, word_dict, heuristic):
    from queue import PriorityQueue

    # Priority queue to store the words to explore
    open_set = PriorityQueue()
    open_set.put((0, start_word))
    
    # Dictionary to keep track of the best path to each word
    came_from = {}
    
    # Cost from start to a given word
    g_score = {start_word: 0}
    
    while not open_set.empty():
        current_cost, current_word = open_set.get()

        # If we reached the target word, reconstruct the path
        if current_word == target_word:
            return reconstruct_path(came_from, current_word)

        # Explore neighbors (valid transformations)
        for neighbor in get_neighbors(current_word, word_dict):
            tentative_g_score = g_score[current_word] + 1  # Each step costs 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                # Record the best path to the neighbor
                came_from[neighbor] = current_word
                g_score[neighbor] = tentative_g_score
                
                # Calculate the priority based on the heuristic
                priority = tentative_g_score + heuristic(neighbor, target_word)
                open_set.put((priority, neighbor))

    return None  # No path found


def get_neighbors(word, word_dict):
    neighbors = []
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            # Generate a new word by changing one letter
            new_word = word[:i] + c + word[i + 1:]
            if new_word in word_dict and new_word != word:
                neighbors.append(new_word)
    return neighbors


def reconstruct_path(came_from, current_word):
    total_path = [current_word]
    while current_word in came_from:
        current_word = came_from[current_word]
        total_path.append(current_word)
    total_path.reverse()
    return total_path


def heuristic(word, target_word):
    # Simple heuristic: the number of letters that are different
    return sum(1 for a, b in zip(word, target_word) if a != b)