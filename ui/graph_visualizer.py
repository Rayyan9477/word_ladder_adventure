import os
import platform
from graphviz import Digraph

class GraphVisualizer:
    def __init__(self):
        self.graph = Digraph(comment='Word Ladder')
        self.graph.attr(rankdir='LR')
        self.graph.attr('node', shape='rectangle', fontname='Arial')
        self.graph.attr('edge', fontname='Arial')
        
        if platform.system() == 'Windows':
            os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

    def render_graph(self, filename):
        try:
            output_filepath = self.graph.render(
                filename=filename,
                format='png',
                cleanup=True
            )
            return output_filepath
        except Exception as e:
            print("Error rendering graph:", e)
            return None

    def create_graph(self, graph_data, filename):
        self.graph.clear()
        
        if not graph_data:
            return
            
        nodes = graph_data.get('nodes', [])
        edges = graph_data.get('edges', [])
        solution_path = graph_data.get('solution_path', [])
        
        if not nodes:
            return
        
        for i, node in enumerate(nodes):
            if i == 0:
                self.graph.node(node, fillcolor='lightgreen', style='filled')
            elif i == len(nodes) - 1:
                self.graph.node(node, fillcolor='lightblue', style='filled')
            else:
                self.graph.node(node, fillcolor='white', style='filled')
                
        for edge in edges:
            self.graph.edge(edge[0], edge[1], color='blue')
            
        if solution_path:
            added_nodes = set(nodes)
            
            for node in solution_path:
                if node not in added_nodes:
                    self.graph.node(node, fillcolor='lightyellow', style='filled')
                    added_nodes.add(node)
            
            for i in range(len(solution_path)-1):
                if (solution_path[i], solution_path[i+1]) not in edges:
                    self.graph.edge(
                        solution_path[i],
                        solution_path[i+1],
                        color='red',
                        style='dashed'
                    )
        
        return self.render_graph(filename)