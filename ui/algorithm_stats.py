import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

class AlgorithmVisualizer:
    @staticmethod
    def show_algorithm_comparison(algorithm_stats):
        """Visualize algorithm performance comparison"""
        if not algorithm_stats:
            st.warning("No algorithm data available for comparison")
            return None
            
        # Extract data for visualization
        algorithms = list(algorithm_stats.keys())
        
        # Check for None values and filter them out
        times = []
        path_lengths = []
        valid_algorithms = []
        
        for algo, stats in algorithm_stats.items():
            time_taken = stats.get('time_taken')
            path_length = stats.get('path_length')
            
            if time_taken is not None and path_length is not None:
                times.append(time_taken)
                path_lengths.append(path_length)
                valid_algorithms.append(algo)
        
        # If no valid data, return None
        if not valid_algorithms:
            st.warning("No valid algorithm comparison data available")
            return None
            
        # Create a figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Time comparison
        bars1 = ax1.bar(valid_algorithms, times, color=['blue', 'green', 'red', 'purple'][:len(valid_algorithms)])
        ax1.set_title('Execution Time Comparison')
        ax1.set_ylabel('Time (seconds)')
        ax1.set_xlabel('Algorithm')
        if times:  # Check if times list is not empty
            ax1.set_ylim(0, max(times) * 1.1)  # Add some padding at the top
        
        # Add labels on top of bars
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}s',
                    ha='center', va='bottom', rotation=0)
        
        # Path length comparison
        bars2 = ax2.bar(valid_algorithms, path_lengths, color=['blue', 'green', 'red', 'purple'][:len(valid_algorithms)])
        ax2.set_title('Path Length Comparison')
        ax2.set_ylabel('Path Length')
        ax2.set_xlabel('Algorithm')
        
        # Add labels on top of bars
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', rotation=0)
        
        plt.tight_layout()
        return fig