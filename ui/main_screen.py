import streamlit as st
from game.game_logic import WordLadderGame
from utils.dictionary_loader import DictionaryLoader

def main_screen():
    st.title("Word Ladder Adventure Game")
    st.write("Welcome to the Word Ladder Adventure Game!")
    st.write("Transform one word into another by changing one letter at a time.")
    
    st.sidebar.header("Game Options")
    game_mode = st.sidebar.selectbox("Select Game Mode", ["Beginner", "Advanced", "Challenge"])
    st.sidebar.write("You selected:", game_mode)
    
    start_game = st.sidebar.button("Start Game")
    
    if start_game:
        st.session_state['game_started'] = True
    
    if 'game_started' in st.session_state and st.session_state['game_started']:
        st.write("Game is starting...")
        # Load the word dictionary
        dictionary_loader = DictionaryLoader('data/dictionary.txt')
        word_dictionary = dictionary_loader.get_all_words()
        
        # Initialize the game
        start_word = st.text_input("Enter the start word:", key="start_word")
        end_word = st.text_input("Enter the end word:", key="end_word")
        
        if st.button("Submit Words"):
            if start_word and end_word:
                game = WordLadderGame(word_dictionary)
                try:
                    game.start_game(start_word, end_word)
                    st.session_state['game'] = game
                    st.write("Game started successfully!")
                    st.write(f"Start Word: {start_word}")
                    st.write(f"End Word: {end_word}")
                except ValueError as e:
                    st.error(str(e))
            else:
                st.warning("Please enter both start and end words.")
        
        if 'game' in st.session_state:
            game = st.session_state['game']
            current_word = st.text_input("Enter the next word:", key="current_word")
            if st.button("Make Move"):
                if game.make_move(current_word):
                    st.write("Congratulations! You've completed the word ladder!")
                else:
                    st.write(f"Current Word Ladder: {game.get_word_ladder()}")
                    st.write(f"Current Score: {game.get_score()}")
    
    st.write("Instructions:")
    st.write("1. Enter a valid word.")
    st.write("2. Transform it into the target word.")
    st.write("3. Use hints if needed!")
    
    # Placeholder for displaying the current word ladder
    st.write("Current Word Ladder:")
    if 'game' in st.session_state:
        st.write(st.session_state['game'].get_word_ladder())

if __name__ == "__main__":
    main_screen()