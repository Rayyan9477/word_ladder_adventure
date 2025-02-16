from game.word_validator import is_valid_word

def get_user_input():
    user_input = input("Enter a word (or type 'exit' to quit): ").strip()
    return user_input

def validate_input(word):
    if is_valid_word(word):
        return True
    else:
        print(f"The word '{word}' is not valid. Please try again.")
        return False

def handle_input():
    while True:
        word = get_user_input()
        if word.lower() == 'exit':
            print("Exiting the game. Thank you for playing!")
            break
        if validate_input(word):
            print(f"You entered a valid word: {word}")
            # Further processing can be done here
        else:
            continue