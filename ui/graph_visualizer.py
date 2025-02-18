from graphviz import Digraph

class GraphVisualizer:
    def __init__(self):
        """Initialize the graph visualizer."""
        self.graph = Digraph(comment='Word Ladder')
        self.graph.attr(rankdir='LR')  # Left to right layout
        self.graph.attr('node', shape='rectangle')

    def add_edge(self, word1, word2, color='black'):
        """Add an edge between two words in the graph."""
        self.graph.edge(word1, word2, color=color)

    def render_graph(self, filename='word_ladder'):
        """Render the graph to a file."""
        try:
            self.graph.render(filename, format='png', cleanup=True)
        except Exception as e:
            print(f"Error rendering graph: {e}")

    def display_graph(self):
        """Display the graph."""
        self.graph.view()

    def clear_graph(self):
        """Clear the graph and reset it."""
        self.graph = Digraph(comment='Word Ladder')
        self.graph.attr(rankdir='LR')
        self.graph.attr('node', shape='rectangle')