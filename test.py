from helpers import overlaps
import networkx as nx

graph1 = nx.Graph()
graph1.add_node("a")
graph1.add_node("b")
graph1.add_node("c")

graph2 = nx.Graph()
graph2.add_node("a")
graph2.add_node("b")
graph2.add_node("c")

does_overlap = overlaps(graph1,graph2)

print("overlaps:")
print(does_overlap)
