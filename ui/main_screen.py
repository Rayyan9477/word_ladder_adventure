import os
import streamlit as st
from game.game_logic import WordLadderGame
from utils.dictionary_loader import DictionaryLoader
from ui.graph_visualizer import GraphVisualizer
from utils.word_generator import RandomWordGenerator
from ui.algorithm_stats import AlgorithmVisualizer

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

    # Initialize random word generator if not in session state
    if 'word_generator' not in st.session_state:
        dictionary = st.session_state.dictionary_loader.get_all_words()
        st.session_state.word_generator = RandomWordGenerator(dictionary)

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
            ['BFS', 'A*', 'UCS', 'GBFS'],
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

        # Auto mode with random words
        st.header("Auto Mode")
        difficulty = st.select_slider(
            "Word Difficulty",
            options=["easy", "medium", "hard"],
            value="medium",
            help="Determines word length and complexity"
        )
        
        if st.button("Generate Random Words"):
            start_word, end_word = st.session_state.word_generator.get_random_pair(difficulty)
            if start_word and end_word:
                st.session_state.random_start = start_word
                st.session_state.random_end = end_word
                st.success(f"Generated: {start_word} → {end_word}")
            else:
                st.error("Couldn't generate suitable word pair, try again")

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
                # Use random word if available
                default_start = st.session_state.get('random_start', '')
                start_word = st.text_input("Start word:", value=default_start).strip().upper()
            with col2:
                default_end = st.session_state.get('random_end', '')
                end_word = st.text_input("End word:", value=default_end).strip().upper()
                
            if st.button("Start Game") and start_word and end_word:
                try:
                    if game.start_game(start_word, end_word):
                        st.success("Game started!")
                        # Clear random words from session state
                        if 'random_start' in st.session_state:
                            del st.session_state['random_start']
                        if 'random_end' in st.session_state:
                            del st.session_state['random_end']
                        st.rerun()
                except ValueError as e:
                    st.error(str(e))
        
        # Game play
        else:
            # Display current game state
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"Start: {game.start_word} → Target: {game.end_word}")
                st.write(f"Current word: {game.current_word}")
                st.write(f"Moves remaining: {game.moves_remaining}")
                st.write(f"Hints remaining: {game.hints_remaining}")
                
                # Allow next word input
                next_word = st.text_input("Enter next word:", key="next_word").strip().upper()
                
                if st.button("Make Move"):
                    if next_word:
                        success, message = game.make_move(next_word)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                
                if st.button("Get Hint"):
                    next_word, hint_message = game.get_hint()
                    if next_word:
                        st.info(hint_message)
                        st.session_state.hint_word = next_word
                    else:
                        st.warning(hint_message)

            # Show visualization of the word ladder
            with col2:
                if 'current_graph' not in st.session_state:
                    # Generate graph visualization
                    graph_data = game.get_graph_data()
                    if graph_data and graph_data.get('nodes'):  # Fixed this line
                        visualizer = GraphVisualizer()
                        visualizer.create_graph(graph_data, image_path)
                        st.session_state.current_graph = True
                    
                if os.path.exists(f"{image_path}.png"):
                    st.image(f"{image_path}.png")
                else:
                    st.info("Graph visualization will appear here")
                    
            # Algorithm Comparison Section
            st.header("Algorithm Comparison")
            algo_stats = game.get_algorithm_comparison()
            if algo_stats:
                try:  # Add try-except block
                    fig = AlgorithmVisualizer.show_algorithm_comparison(algo_stats)
                    if fig:
                        st.pyplot(fig)
                        
                    # Display path differences
                    st.subheader("Paths Found by Different Algorithms")
                    for algo, stats in algo_stats.items():
                        if stats.get('path'):  # Use get() to avoid KeyError
                            st.write(f"**{algo.upper()}**: {' → '.join(stats['path'])}")
                except Exception as e:
                    st.error(f"Error displaying algorithm comparison: {str(e)}")
            else:
                st.write("Algorithm comparison data not available")

    else:
        # Game over screen
        if game.won:
            st.success("🎉 Congratulations! You've completed the word ladder!")
            st.subheader(f"Final score: {game.calculate_score()}")
            
            # Display the path taken
            path_str = " → ".join(game.player_path)
            st.write(f"Your path ({len(game.player_path)-1} moves): {path_str}")
            
            # Display optimal solution for comparison
            if game.solution_path:
                optimal_str = " → ".join(game.solution_path)
                st.write(f"Optimal path ({len(game.solution_path)-1} moves): {optimal_str}")
                
            # Show algorithm comparison at game end too
            st.header("Algorithm Comparison")
            algo_stats = game.get_algorithm_comparison()
            if algo_stats:
                try:  # Add try-except block
                    fig = AlgorithmVisualizer.show_algorithm_comparison(algo_stats)
                    if fig:
                        st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error displaying algorithm comparison: {str(e)}")
        else:
            st.error("Game Over! You've run out of moves.")
            
            # Show how far they got
            path_str = " → ".join(game.player_path)
            st.write(f"Your path: {path_str}")
            
            # Show the optimal solution
            if game.solution_path:
                optimal_str = " → ".join(game.solution_path)
                st.write(f"Optimal path: {optimal_str}")

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
        
        # Algorithm comparison information
        st.markdown("### Algorithm Information")
        st.markdown("""
        **BFS**: Finds shortest path by exploring all neighbors first
        
        **A***: Uses heuristics to find shortest path efficiently
        
        **UCS**: Explores paths with lowest cost first
        
        **GBFS**: Greedily follows heuristic towards goal
        """)
        
        # Add auto mode button for complete autoplay
        st.header("Auto Play")
        if game.start_word and not game.game_over:
            if st.button("Auto Solve"):
                if game.solution_path and len(game.solution_path) > 1:
                    # Get the next word from solution path
                    current_index = game.player_path.index(game.current_word) if game.current_word in game.player_path else 0
                    solution_index = game.solution_path.index(game.current_word) if game.current_word in game.solution_path else 0
                    
                    if solution_index < len(game.solution_path) - 1:
                        next_move = game.solution_path[solution_index + 1]
                        st.session_state.auto_next_word = next_move
                        st.info(f"Auto playing next move: {next_move}")
                        st.rerun()

if __name__ == "__main__":
    main_screen()