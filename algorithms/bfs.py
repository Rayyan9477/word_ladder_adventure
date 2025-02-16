from collections import deque

def bfs(start_word, target_word, word_dict):
    if start_word == target_word:
        return [start_word]

    queue = deque([[start_word]])
    visited = set([start_word])

    while queue:
        current_path = queue.popleft()
        current_word = current_path[-1]

        for next_word in get_neighbors(current_word, word_dict):
            if next_word not in visited:
                visited.add(next_word)
                new_path = current_path + [next_word]
                if next_word == target_word:
                    return new_path
                queue.append(new_path)

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