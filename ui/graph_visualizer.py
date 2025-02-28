import os
import platform
from graphviz import Digraph

class GraphVisualizer:
    def __init__(self):
        self.graph = Digraph(comment='Word Ladder')
        self.graph.attr(rankdir='LR')
        self.graph.attr('node', shape='rectangle', fontname='Arial')
        self.graph.attr('edge', fontname='Arial')
        
        # Set Graphviz path for Windows
        if platform.system() == 'Windows':
            os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

    def render_graph(self, filename):
            """Render the graph to a PNG file and open it using the system default viewer."""
            try:
                output_filepath = self.graph.render(
                    filename=filename,
                    format='png',
                    view=True,
                    cleanup=True
                )
                print(f"Graph rendered and available at: {output_filepath}")
            except Exception as e:
                print("Error rendering graph:", e)
            
    def create_graph(self, graph_data, filename):
        """Create an interactive graph visualization"""
        self.graph.clear()
        
        if not graph_data:
            return
            
        nodes = graph_data.get('nodes', [])
        edges = graph_data.get('edges', [])
        solution_path = graph_data.get('solution_path', [])
        
        if not nodes:
            return
        
        # Add nodes with different colors based on their role
        for i, node in enumerate(nodes):
            if i == 0:  # Start word
                self.graph.node(node, fillcolor='lightgreen', style='filled')
            elif i == len(nodes) - 1:  # Current word
                self.graph.node(node, fillcolor='lightblue', style='filled')
            else:  # Intermediate words
                self.graph.node(node, fillcolor='white', style='filled')
                
        # Add edges for player's path
        for edge in edges:
            self.graph.edge(edge[0], edge[1], color='blue')
            
        # Add solution path edges if shown
        if solution_path:
            for i in range(len(solution_path)-1):
                if solution_path[i] not in nodes or solution_path[i+1] not in nodes:
                    self.graph.edge(
                        solution_path[i],
                        solution_path[i+1],
                        color='red',
                        style='dashed'
                    )
        
        # Render the graph
        self.render_graph(filename)