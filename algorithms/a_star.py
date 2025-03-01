from queue import PriorityQueue
import logging

def a_star_search(start_word, target_word, word_dict):
    
    def heuristic(word1, word2):
        return sum(1 for a, b in zip(word1, word2) if a != b)

    def get_neighbors(word, word_dict):
        neighbors = []
        word = word.upper()
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        for i in range(len(word)):
            for c in letters:
                if c != word[i]:
                    neighbor = word[:i] + c + word[i+1:]
                    if neighbor in word_dict:
                        neighbors.append(neighbor)
        return neighbors

    def reconstruct_path(came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current)
        path.reverse()
        return path

    try:
        open_set = PriorityQueue()
        open_set.put((0, start_word))
        came_from = {}
        g_score = {word: float('inf') for word in word_dict}
        g_score[start_word] = 0
        f_score = {word: float('inf') for word in word_dict}
        f_score[start_word] = heuristic(start_word, target_word)

        while not open_set.empty():
            current = open_set.get()[1]

            if current == target_word:
                return reconstruct_path(came_from, current)

            for neighbor in get_neighbors(current, word_dict):
                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, target_word)
                    open_set.put((f_score[neighbor], neighbor))

        return None
    except Exception as e:
        logging.error(f"Error in A* search: {e}")
        return None