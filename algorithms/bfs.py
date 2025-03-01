from collections import deque
import logging

def bfs(start_word, target_word, word_dict):

    if start_word == target_word:
        return [start_word]

    queue = deque([(start_word, [start_word])])
    visited = {start_word}

    while queue:
        current_word, path = queue.popleft()
        
        for i in range(len(current_word)):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                next_word = current_word[:i] + c + current_word[i+1:]
                
                if next_word in word_dict and next_word not in visited:
                    if next_word == target_word:
                        return path + [next_word]
                    visited.add(next_word)
                    queue.append((next_word, path + [next_word]))
    
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