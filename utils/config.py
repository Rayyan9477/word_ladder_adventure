# Configuration settings for the Word Ladder Adventure Game

# Game settings
GAME_SETTINGS = {
    "max_attempts": 5,  # Maximum number of attempts for each word transformation
    "time_limit": 60,   # Time limit for each game in seconds
    "score_multiplier": 10,  # Multiplier for scoring based on performance
}

# Difficulty settings
DIFFICULTY_SETTINGS = {
    "beginner": {
        "max_word_length": 5,  # Maximum word length for beginner mode
        "min_word_length": 3,   # Minimum word length for beginner mode
    },
    "advanced": {
        "max_word_length": 7,  # Maximum word length for advanced mode
        "min_word_length": 4,   # Minimum word length for advanced mode
    },
    "challenge": {
        "max_word_length": 8,  # Maximum word length for challenge mode
        "min_word_length": 5,   # Minimum word length for challenge mode
        "additional_constraints": True,  # Enable additional constraints
    },
}

# Algorithm settings
ALGORITHM_SETTINGS = {
    "default_algorithm": "a_star",  # Default algorithm for hint generation
    "available_algorithms": ["ucs", "a_star", "bfs", "gbfs"],  # List of available algorithms
}

# Visualization settings
VISUALIZATION_SETTINGS = {
    "show_graph": True,  # Whether to show graph visualization
    "graph_color_scheme": "viridis",  # Color scheme for graph visualization
}