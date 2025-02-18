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

    def create_graph(self, nodes, edges, solution_path=None):
        """Create graph with player path and solution path"""
        self.graph.clear()

        # Add nodes
        for node in nodes:
            if node == nodes[0]:
                self.graph.node(node, style='filled', fillcolor='lightgreen')
            elif node == nodes[-1]:
                self.graph.node(node, style='filled', fillcolor='lightblue')
            else:
                self.graph.node(node, style='filled', fillcolor='white')

        # Add edges for player path
        for edge in edges:
            self.graph.edge(edge[0], edge[1], color='blue', penwidth='2.0')

        # Add solution path edges (if requested)
        if solution_path:
            for i in range(len(solution_path)-1):
                if solution_path[i] not in nodes or solution_path[i+1] not in nodes:
                    self.graph.edge(solution_path[i], solution_path[i+1], 
                                  color='red', style='dashed')

    def render_graph(self, filename=None):
        """Render the graph to a file"""
        try:
            if filename is None:
                dir_path = os.path.join(os.path.dirname(__file__), '..', 'static')
                os.makedirs(dir_path, exist_ok=True)
                filename = os.path.join(dir_path, 'word_ladder')
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Generate the graph
            png_filename = f"{filename}.png"
            self.graph.render(filename, format='png', cleanup=True)
            
            if not os.path.exists(png_filename):
                raise Exception("Failed to create graph image")
            
            return png_filename
                
        except Exception as e:
            alt_paths = [
                r"C:\Program Files\Graphviz\bin\dot.exe",
                r"C:\Program Files (x86)\Graphviz\bin\dot.exe"
            ]
            for path in alt_paths:
                if os.path.exists(path):
                    os.environ["GRAPHVIZ_DOT"] = path
                    png_filename = f"{filename}.png"
                    self.graph.render(filename, format='png', cleanup=True)
                    if os.path.exists(png_filename):
                        return png_filename
                    
            raise Exception(f"Error rendering graph: {str(e)}\nPlease ensure Graphviz is installed and in your system PATH")