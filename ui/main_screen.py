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

    # Initialize session state
    if 'game' not in st.session_state:
        dictionary_loader = DictionaryLoader('data/dictionary.txt')
        st.session_state.game = WordLadderGame(dictionary_loader.get_all_words())
        st.session_state.dictionary_loader = dictionary_loader

    # Game options in sidebar
    with st.sidebar:
        st.header("Game Options")
        algorithm = st.radio("Select Algorithm", ['BFS', 'A*', 'UCS'])
        max_moves = st.slider("Max Moves", 5, 20, 10)
        
        if st.button("New Game"):
            if os.path.exists(f"{image_path}.png"):
                try:
                    os.remove(f"{image_path}.png")
                except Exception:
                    pass
            st.session_state.game = WordLadderGame(
                st.session_state.dictionary_loader.get_all_words(),
                algorithm.lower(),
                max_moves
            )
            st.rerun()

    game = st.session_state.game
    
    # Main game area
    if hasattr(game, 'game_over') and not game.game_over:
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
            # Display game state
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"Start: {game.start_word}")
            with col2:
                st.write(f"Current: {game.current_word}")
            with col3:
                st.write(f"Target: {game.end_word}")

            # Display game progress
            st.write(f"Moves remaining: {game.moves_remaining}")
            st.write("Current path:", " → ".join(game.player_path))
            
            # Input for next move
            new_word = st.text_input("Enter next word:").strip().upper()
            
            # Game controls
            col1, col2 = st.columns(2)
            with col1:
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
                                    graph_bytes = f.read()
                                st.session_state['current_graph'] = graph_bytes
                        except Exception as e:
                            st.error(f"Error updating graph: {str(e)}")
                        st.rerun()
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
                            graph_bytes = f.read()
                        st.session_state['current_graph'] = graph_bytes
                        st.image(graph_bytes, caption="Word Ladder Progress")
                except Exception as e:
                    st.error(f"Error displaying graph: {str(e)}")

    else:
        if hasattr(game, 'won') and game.won:
            st.success("Congratulations! You've won!")
            if 'current_graph' in st.session_state:
                st.image(st.session_state['current_graph'], caption="Final Word Ladder")
        else:
            st.error("Game Over!")
        
        if st.button("Play Again"):
            if os.path.exists(f"{image_path}.png"):
                try:
                    os.remove(f"{image_path}.png")
                except Exception:
                    pass
            if 'current_graph' in st.session_state:
                del st.session_state['current_graph']
            st.session_state.game = WordLadderGame(
                st.session_state.dictionary_loader.get_all_words(),
                algorithm.lower(),
                max_moves
            )
            st.rerun()

if __name__ == "__main__":
    main_screen()