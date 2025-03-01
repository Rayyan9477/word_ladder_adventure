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

    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
    os.makedirs(static_dir, exist_ok=True)
    image_path = os.path.join(static_dir, 'word_ladder')

    if 'dictionary_loader' not in st.session_state:
        st.session_state.dictionary_loader = DictionaryLoader('data/dictionary.txt')

    if 'word_generator' not in st.session_state:
        dictionary = st.session_state.dictionary_loader.get_all_words()
        st.session_state.word_generator = RandomWordGenerator(dictionary)

    with st.sidebar:
        st.header("Game Settings")
        
        mode = st.selectbox(
            "Select Mode",
            ["Normal", "Beginner", "Advanced", "Challenge"],
            help="Choose game difficulty mode"
        )
        
        algorithm = st.radio(
            "Select Algorithm",
            ['BFS', 'A*', 'UCS', 'GBFS'],
            help="Choose pathfinding algorithm"
        )
        
        base_moves = st.slider(
            "Base Moves", 
            5, 20, 10,
            help="Base number of moves allowed"
        )

        max_moves = base_moves
        if mode == "Beginner":
            st.info("Beginner mode: More hints and moves available")
            max_moves += 5
        elif mode == "Challenge":
            st.warning("Challenge mode: Limited hints and moves")
            max_moves -= 2

        st.header("Auto Mode")
        difficulty = st.select_slider(
            "Word Difficulty",
            options=["easy", "medium", "hard"],
            value="medium",
            help="Determines word length and complexity"
        )
        
        if st.button("Generate Random Words"):
            with st.spinner("Looking for suitable word pairs..."):
                start_word, end_word = st.session_state.word_generator.get_random_pair(difficulty)
                if start_word and end_word:
                    st.session_state.random_start = start_word
                    st.session_state.random_end = end_word
                    st.success(f"Generated: {start_word} → {end_word}")
                else:
                    st.error("Couldn't generate suitable word pair, try again")

        if st.button("New Game"):
            for suffix in ['', '_final']:
                if os.path.exists(f"{image_path}{suffix}.png"):
                    try:
                        os.remove(f"{image_path}{suffix}.png")
                    except Exception:
                        pass
            
            for key in ['current_graph', 'last_word', 'show_comparison']:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.session_state.game = WordLadderGame(
                st.session_state.dictionary_loader.get_all_words(),
                algorithm=algorithm.lower(),
                max_moves=max_moves,
                mode=mode
            )
            st.rerun()

    if 'game' not in st.session_state:
        st.session_state.game = WordLadderGame(
            st.session_state.dictionary_loader.get_all_words(),
            algorithm=algorithm.lower(),
            max_moves=max_moves,
            mode=mode
        )

    game = st.session_state.game

    if not game.game_over:
        if not game.start_word:
            col1, col2 = st.columns(2)
            with col1:
                default_start = st.session_state.get('random_start', '')
                start_word = st.text_input("Start word:", value=default_start).strip().upper()
            with col2:
                default_end = st.session_state.get('random_end', '')
                end_word = st.text_input("End word:", value=default_end).strip().upper()
                
            if st.button("Start Game") and start_word and end_word:
                try:
                    with st.spinner("Starting game..."):
                        if game.start_game(start_word, end_word):
                            st.success("Game started!")
                            if 'random_start' in st.session_state:
                                del st.session_state['random_start']
                            if 'random_end' in st.session_state:
                                del st.session_state['random_end']
                            st.rerun()
                except ValueError as e:
                    st.error(str(e))
        
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"Start: {game.start_word} → Target: {game.end_word}")
                st.write(f"Current word: {game.current_word}")
                st.write(f"Moves remaining: {game.moves_remaining}")
                st.write(f"Hints remaining: {game.hints_remaining}")
                
                next_word = st.text_input("Enter next word:", key="next_word").strip().upper()
                
                if st.button("Make Move"):
                    if next_word:
                        success, message = game.make_move(next_word)
                        if success:
                            st.success(message)
                            if 'current_graph' in st.session_state:
                                del st.session_state['current_graph']
                            
                            if game.game_over:
                                st.session_state.show_comparison = True
                                st.rerun()
                            else:
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

            with col2:
                if len(game.player_path) > 1:
                    if 'current_graph' not in st.session_state or 'last_word' not in st.session_state or st.session_state.last_word != game.current_word:
                        gameplay_data = {
                            'nodes': game.player_path.copy(),
                            'edges': [(game.player_path[i], game.player_path[i+1]) 
                                    for i in range(len(game.player_path)-1)],
                            'solution_path': []
                        }
                        
                        visualizer = GraphVisualizer()
                        visualizer.create_graph(gameplay_data, image_path)
                        st.session_state.current_graph = True
                        st.session_state.last_word = game.current_word
                    
                    if os.path.exists(f"{image_path}.png"):
                        st.image(f"{image_path}.png")
                else:
                    st.info("Graph will appear when you make your first move")

    else:
        if game.won:
            st.balloons()
            
            st.markdown("""
            <style>
            @keyframes victory-pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            .victory-banner {
                background: linear-gradient(135deg, #4CAF50, #8BC34A);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                margin-bottom: 25px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                animation: victory-pulse 1.5s infinite;
            }
            .victory-title {
                color: white;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .victory-subtitle {
                color: white;
                font-size: 1.5em;
                margin-bottom: 5px;
            }
            </style>
            
            <div class="victory-banner">
                <div class="victory-title">🏆 VICTORY! 🏆</div>
                <div class="victory-subtitle">Brilliant work! You've mastered the word ladder!</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader(f"🌟 Final score: {game.calculate_score()} 🌟")
            
            path_str = " → ".join(game.player_path)
            st.write(f"Your path ({len(game.player_path)-1} moves): {path_str}")
            
            if game.solution_path:
                optimal_str = " → ".join(game.solution_path)
                st.write(f"Optimal path ({len(game.solution_path)-1} moves): {optimal_str}")
                
                player_moves = len(game.player_path) - 1
                optimal_moves = len(game.solution_path) - 1
                if player_moves == optimal_moves:
                    st.success("🎯 Perfect! You found the optimal solution!")
                elif player_moves <= optimal_moves + 2:
                    st.success("👏 Great job! Your solution was very close to optimal!")
                else:
                    st.info("Next time, try to find a shorter path!")
                
        else:
            st.error("Game Over! You've run out of moves.")
            
            path_str = " → ".join(game.player_path)
            st.write(f"Your path: {path_str}")
            
            if game.solution_path:
                optimal_str = " → ".join(game.solution_path)
                st.write(f"Optimal path: {optimal_str}")

        st.header("Final Path Visualization")
        
        if not os.path.exists(f"{image_path}_final.png"):
            final_graph_data = {
                'nodes': game.player_path.copy(),
                'edges': [(game.player_path[i], game.player_path[i+1]) 
                        for i in range(len(game.player_path)-1)],
                'solution_path': game.solution_path
            }
            
            visualizer = GraphVisualizer()
            visualizer.create_graph(final_graph_data, f"{image_path}_final")
        
        if os.path.exists(f"{image_path}_final.png"):
            st.image(f"{image_path}_final.png")
        else:
            st.error("Could not generate final visualization")
        
        # ALWAYS show algorithm comparison at the end of the game
        st.header("Algorithm Comparison")
        algo_stats = game.get_algorithm_comparison()
        
        if algo_stats:
            try:
                fig = AlgorithmVisualizer.show_algorithm_comparison(algo_stats)
                if fig:
                    st.pyplot(fig)
                    
                st.subheader("Paths Found by Different Algorithms")
                for algo, stats in algo_stats.items():
                    if stats and stats.get('path'):
                        path = stats.get('path')
                        if path:
                            st.write(f"**{algo.upper()}** ({len(path)-1} moves): {' → '.join(path)}")
                        else:
                            st.write(f"**{algo.upper()}**: No path found")
            except Exception as e:
                st.error(f"Error displaying algorithm comparison: {str(e)}")
        else:
            st.warning("Algorithm comparison data not available")
            
        # Ensure algorithm comparison is always shown by forcing reload if not present
        if 'algorithm_displayed' not in st.session_state:
            st.session_state.algorithm_displayed = True
            st.rerun()

        st.markdown("""
        <style>
        .play-again-btn {
            background-color: #2E86C1;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            text-align: center;
            margin: 20px 0;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: all 0.3s;
        }
        .play-again-btn:hover {
            background-color: #1A5276;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("Play Again", key="play_again"):
            for suffix in ['', '_final']:
                if os.path.exists(f"{image_path}{suffix}.png"):
                    try:
                        os.remove(f"{image_path}{suffix}.png")
                    except Exception:
                        pass
            
            for key in ['current_graph', 'last_word', 'show_comparison', 'algorithm_displayed']:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.session_state.game = WordLadderGame(
                st.session_state.dictionary_loader.get_all_words(),
                algorithm=algorithm.lower(),
                max_moves=max_moves,
                mode=mode
            )
            st.rerun()

    with st.sidebar:
        st.markdown("### How to Play")
        st.markdown("""
        1. Enter start and target words
        2. Change one letter at a time
        3. Each new word must be valid
        4. Reach the target word within moves limit
        """)
        
        st.markdown("### Algorithm Information")
        st.markdown("""
        **BFS**: Finds shortest path by exploring all neighbors first
        
        **A***: Uses heuristics to find shortest path efficiently
        
        **UCS**: Explores paths with lowest cost first
        
        **GBFS**: Greedily follows heuristic towards goal
        """)
        
        st.header("Auto Play")
        if game.start_word and not game.game_over:
            if st.button("Auto Solve"):
                if game.solution_path and len(game.solution_path) > 1:
                    current_index = game.player_path.index(game.current_word) if game.current_word in game.player_path else 0
                    solution_index = game.solution_path.index(game.current_word) if game.current_word in game.solution_path else 0
                    
                    if solution_index < len(game.solution_path) - 1:
                        next_move = game.solution_path[solution_index + 1]
                        st.session_state.auto_next_word = next_move
                        st.info(f"Auto playing next move: {next_move}")
                        st.rerun()

if __name__ == "__main__":
    main_screen()