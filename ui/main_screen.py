import os
import streamlit as st
from game.game_logic import WordLadderGame
from utils.dictionary_loader import DictionaryLoader
from ui.graph_visualizer import GraphVisualizer

def main_screen():
    st.set_page_config(page_title="Word Ladder Adventure", layout="wide")
    st.title("Word Ladder Adventure Game")
    st.write("Transform one word into another by changing one letter at a time!")

    # Create static directory for images if it doesn't exist
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
    os.makedirs(static_dir, exist_ok=True)
    image_path = os.path.join(static_dir, 'word_ladder')

    # Initialize dictionary loader if not in session state
    if 'dictionary_loader' not in st.session_state:
        st.session_state.dictionary_loader = DictionaryLoader('data/dictionary.txt')

    # Game options in sidebar
    with st.sidebar:
        st.header("Game Settings")
        
        # Mode selection
        mode = st.selectbox(
            "Select Mode",
            ["Normal", "Beginner", "Advanced", "Challenge"],
            help="Choose game difficulty mode"
        )
        
        # Algorithm selection
        algorithm = st.radio(
            "Select Algorithm",
            ['BFS', 'A*', 'UCS'],
            help="Choose pathfinding algorithm"
        )
        
        # Moves configuration
        base_moves = st.slider(
            "Base Moves", 
            5, 20, 10,
            help="Base number of moves allowed"
        )

        # Adjust moves based on mode
        max_moves = base_moves
        if mode == "Beginner":
            st.info("Beginner mode: More hints and moves available")
            max_moves += 5
        elif mode == "Challenge":
            st.warning("Challenge mode: Limited hints and moves")
            max_moves -= 2

        # New Game button
        if st.button("New Game"):
            # Clean up old graph
            if os.path.exists(f"{image_path}.png"):
                try:
                    os.remove(f"{image_path}.png")
                except Exception:
                    pass
            
            # Reset session state
            if 'current_graph' in st.session_state:
                del st.session_state['current_graph']
            
            # Create new game instance
            st.session_state.game = WordLadderGame(
                st.session_state.dictionary_loader.get_all_words(),
                algorithm=algorithm.lower(),
                max_moves=max_moves
            )
            st.rerun()

    # Initialize game if not in session state
    if 'game' not in st.session_state:
        st.session_state.game = WordLadderGame(
            st.session_state.dictionary_loader.get_all_words(),
            algorithm=algorithm.lower(),
            max_moves=max_moves
        )

    game = st.session_state.game

    # Main game area
    if not game.game_over:
        # Game initialization
        if not game.start_word:
            col1, col2 = st.columns(2)
            with col1:
                start_word = st.text_input("Start word:").strip().upper()
            with col2:
                end_word = st.text_input("End word:").strip().upper()
                
            if st.button("Start Game") and start_word and end_word:
                try:
                    if game.start_game(start_word, end_word):
                        st.success("Game started!")
                        st.rerun()
                except ValueError as e:
                    st.error(str(e))
        
        # Game play
        else:
            # Game stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Word", game.current_word)
            with col2:
                st.metric("Moves Left", game.moves_remaining)
            with col3:
                st.metric("Target Word", game.end_word)

            # Display current path
            st.write("Current path:", " → ".join(game.player_path))
            
            # Game controls
            col1, col2 = st.columns(2)
            with col1:
                new_word = st.text_input("Enter next word:").strip().upper()
                if st.button("Make Move") and new_word:
                    success, message = game.make_move(new_word)
                    if success:
                        st.success(message)
                        # Update graph
                        try:
                            graph_data = game.get_graph_data()
                            visualizer = GraphVisualizer()
                            visualizer.create_graph(
                                graph_data['nodes'],
                                graph_data['edges'],
                                graph_data['solution_path']
                            )
                            png_path = visualizer.render_graph(filename=image_path)
                            if os.path.exists(png_path):
                                with open(png_path, "rb") as f:
                                    st.session_state['current_graph'] = f.read()
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error updating graph: {str(e)}")
                    else:
                        st.error(message)
            
            with col2:
                if st.button("Get Hint"):
                    hint, message = game.get_hint()
                    if hint:
                        st.info(message)
                    else:
                        st.warning(message)

            # Display graph
            if 'current_graph' in st.session_state:
                st.image(st.session_state['current_graph'], caption="Word Ladder Progress")

    else:
        # Game Over state
        if game.won:
            st.success(f"Congratulations! You've won with a score of {game.calculate_score()}!")
            if 'current_graph' in st.session_state:
                st.image(st.session_state['current_graph'], caption="Final Word Ladder")
        else:
            st.error("Game Over! Try again!")
        
        # Play Again button
        if st.button("Play Again"):
            # Clean up
            if os.path.exists(f"{image_path}.png"):
                try:
                    os.remove(f"{image_path}.png")
                except Exception:
                    pass
            if 'current_graph' in st.session_state:
                del st.session_state['current_graph']
            
            # New game
            st.session_state.game = WordLadderGame(
                st.session_state.dictionary_loader.get_all_words(),
                algorithm=algorithm.lower(),
                max_moves=max_moves
            )
            st.rerun()

    # Game instructions
    with st.sidebar:
        st.markdown("### How to Play")
        st.markdown("""
        1. Enter start and target words
        2. Change one letter at a time
        3. Each new word must be valid
        4. Reach the target word within moves limit
        """)

if __name__ == "__main__":
    main_screen()