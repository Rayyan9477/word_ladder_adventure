def is_valid_word(word, dictionary):
    """Check if word exists in dictionary, case-insensitive"""
    return word.upper() in dictionary or word.lower() in dictionary

def is_one_letter_diff(word1, word2):
    """Check if words differ by exactly one letter"""
    if len(word1) != len(word2):
        return False
    return sum(c1 != c2 for c1, c2 in zip(word1.upper(), word2.upper())) == 1

def validate_transformation(start_word, end_word, dictionary):
    """Validate both words exist in dictionary"""
    if not is_valid_word(start_word, dictionary) or not is_valid_word(end_word, dictionary):
        return False
    return True

def find_valid_transformations(current_word, dictionary):
    """Find all valid one-letter transformations"""
    current_word = current_word.upper()
    return [word for word in dictionary if is_one_letter_diff(current_word, word)]