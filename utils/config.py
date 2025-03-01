
GAME_SETTINGS = {
    "max_attempts": 5,  
    "time_limit": 60,   
    "score_multiplier": 10,  
}

DIFFICULTY_SETTINGS = {
    "beginner": {
        "max_word_length": 5,  
        "min_word_length": 3, 
    },
    "advanced": {
        "max_word_length": 7,
        "min_word_length": 4,  
    },
    "challenge": {
        "max_word_length": 8,  
        "min_word_length": 5,   
        "additional_constraints": True,  
    },
}

ALGORITHM_SETTINGS = {
    "default_algorithm": "a_star",  
    "available_algorithms": ["ucs", "a_star", "bfs", "gbfs"],  
}

VISUALIZATION_SETTINGS = {
    "show_graph": True, 
    "graph_color_scheme": "viridis", 
}