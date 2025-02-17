import streamlit as st
from game.game_logic import WordLadderGame
from utils.dictionary_loader import DictionaryLoader
from ui.graph_visualizer import GraphVisualizer  # Import GraphVisualizer

def main_screen():
    st.title("Word Ladder Adventure Game")
    st.write("Welcome to the Word Ladder Adventure Game!")
    st.write("Transform one word into another by changing one letter at a time.")
    
    st.sidebar.header("Game Options")
    game_mode = st.sidebar.selectbox("Select Game Mode", ["Beginner", "Advanced", "Challenge"])
    st.sidebar.write("You selected:", game_mode)

    algorithm = st.sidebar.selectbox("Select Algorithm", ["a_star", "bfs", "ucs"])
    st.sidebar.write("You selected:", algorithm)
    
    max_moves = st.sidebar.slider("Max Moves", min_value=5, max_value=30, value=20, step=5)
    st.sidebar.write("You selected:", max_moves)
    
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
                try:
                    game = WordLadderGame(word_dictionary, algorithm, max_moves)
                    game.start_game(start_word, end_word)
                    st.session_state['game'] = game
                    st.write("Game started successfully!")
                    st.write(f"Start Word: {start_word}")
                    st.write(f"End Word: {end_word}")
                    st.write(f"Algorithm: {algorithm}")
                    st.write(f"Max Moves: {max_moves}")

                    # Visualize the graph
                    graph_visualizer = GraphVisualizer()
                    for i in range(len(game.get_word_ladder()) - 1):
                        graph_visualizer.add_edge(game.get_word_ladder()[i], game.get_word_ladder()[i+1])
                    graph_visualizer.render_graph()
                    st.image("word_ladder.png", use_column_width=True)

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
                    st.write(f"Moves Remaining: {game.get_moves_remaining()}")

            if st.button("Get Hint"):
                hint = game.get_hint()
                if hint:
                    st.write(f"Hint: Try '{hint}'")
                else:
                    st.write("No hint available.")
    
    st.write("Instructions:")
    st.write("1. Enter a valid word.")
    st.write("2. Transform it into the target word.")
    st.write("3. Use hints if needed!")
    
    # Placeholder for displaying the current word ladder
    st.write("Current Word Ladder:")
    if 'game' in st.session_state:
        st.write(st.session_state['game'].get_word_ladder())