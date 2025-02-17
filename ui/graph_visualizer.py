from graphviz import Digraph

class GraphVisualizer:
    def __init__(self):
        self.graph = Digraph(comment='Word Ladder')

    # def add_edge(self, word1, word2):
    #     self.graph.edge(word1, word2)

    # def render_graph(self, filename='word_ladder'):
    #     self.graph.render(filename, format='png', cleanup=True)

    # def display_graph(self):
    #     self.graph.view()

    # def clear_graph(self):
    #     self.graph = Digraph(comment='Word Ladder')