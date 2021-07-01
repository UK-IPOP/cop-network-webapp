import networkx as nx
import pickle


def save_graph(connections: list[tuple[str, str]]):
    """Utility function to save a networkx graph from connection pairs.

    Args:
        connections (list[tuple[str, str]]): A list of connection pairs.
    """
    G = nx.Graph()
    G.add_edges_from(connections)
    positions = nx.spring_layout(G)
    with open("data/cop-graph.pkl", "wb") as f:
        pickle.dump(G, f)
    with open("data/cop-graph-positions.pkl", "wb") as f:
        pickle.dump(positions, f)


def load_graph_from_files() -> tuple[nx.Graph, nx.layout]:
    """Utility function to load a networkx graph from files.

    Returns:
        tuple[nx.Graph, nx.layout]: Networkx graph and spring_layout positions.
    """
    with open("data/cop-graph.pkl", "rb") as f:
        g = pickle.load(f)
    with open("data/cop-graph-positions.pkl", "rb") as f:
        positions = pickle.load(f)
    return g, positions


def save_ipop_graph(connections: list[tuple[str, str]]):
    """Utility function to save a networkx graph from connection pairs.

    Should be used ONLY on IPOP authors connections.

    Args:
        connections (list[tuple[str, str]]): A list of connection pairs.
    """
    G = nx.Graph()
    G.add_edges_from(connections)
    positions = nx.spring_layout(G)
    with open("data/ipop-graph.pkl", "wb") as f:
        pickle.dump(G, f)
    with open("data/ipop-graph-positions.pkl", "wb") as f:
        pickle.dump(positions, f)


def load_ipop_graph_from_files() -> tuple[nx.Graph, nx.layout]:
    """Utility function to load a networkx graph from files.

    Should be used ONLY on IPOP authors connections.

    Returns:
        tuple[nx.Graph, nx.layout]: Networkx graph and spring_layout positions.
    """
    with open("data/ipop-graph.pkl", "rb") as f:
        g = pickle.load(f)
    with open("data/ipop-graph-positions.pkl", "rb") as f:
        positions = pickle.load(f)
    return g, positions