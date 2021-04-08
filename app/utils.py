import networkx as nx
import pickle


def save_graph(connections: list[tuple[str, str]]):
    G = nx.Graph()
    G.add_edges_from(connections)
    positions = nx.spring_layout(G)
    with open("data/cop-graph.pkl", "wb") as f:
        pickle.dump(G, f)
    with open("data/cop-graph-positions.pkl", "wb") as f:
        pickle.dump(positions, f)


def load_graph_from_files() -> tuple[nx.Graph, nx.layout]:
    with open("data/cop-graph.pkl", "rb") as f:
        g = pickle.load(f)
    with open("data/cop-graph-positions.pkl", "rb") as f:
        positions = pickle.load(f)
    return g, positions
