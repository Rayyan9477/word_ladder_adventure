from queue import PriorityQueue

def a_star_search(start_word, target_word, word_dict):
    def heuristic(word1, word2):
        return sum(1 for a, b in zip(word1, word2) if a != b)

    def get_neighbors(word, word_dict):
        neighbors = []
        for i in range(len(word)):
            for char in 'abcdefghijklmnopqrstuvwxyz':
                if char != word[i]:
                    new_word = word[:i] + char + word[i+1:]
                    if new_word in word_dict:
                        neighbors.append(new_word)
        return neighbors

    def reconstruct_path(came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current)
        path.reverse()
        return path

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