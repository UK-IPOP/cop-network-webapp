import csv
import scholar_network as sn
from utils import utils
import pickle
import networkx as nx


def load_scholar_names_from_file() -> list[str]:
    """Loads scholars from file.

    Returns:
        list[str]: A list of scholar names.
    """
    with open("data/COPscholars.csv", "r") as f:
        csvreader = csv.DictReader(f)
        authors = []
        for row in csvreader:
            authors.append(row.get("Name"))
        return authors


def load_ipop_scholar_names_from_file() -> list[str]:
    """Loads, specifically, IPOP scholars from file.

    Returns:
        list[str]: List of IPOP scholar names.
    """
    with open("data/IPOP-Scholars.csv", "r") as f:
        csvreader = csv.DictReader(f)
        authors = []
        for row in csvreader:
            authors.append(row.get("Name"))
        return authors


def parse_name(name: str) -> str:
    """Extracts first and last parts of a name.

    This could be first and last name or any variation.

    Args:
        name (str): String name to be parsed

    Returns:
        str: Extracted 2-part name.
    """
    parts = name.split()
    parsed = f"{parts[0]} {parts[-1]}"
    return parsed


cop = [parse_name(x) for x in load_scholar_names_from_file()]
ipop = [parse_name(x) for x in load_ipop_scholar_names_from_file()]

graph = sn.build_graph()

G = nx.Graph()
G.add_edges_from(
    [(parse_name(pair[0]), parse_name(pair[1])) for pair in graph.node_pairs()]
)


cop_pairs = [
    (parse_name(pair[0]), parse_name(pair[1]))
    for pair in graph.node_pairs()
    if parse_name(pair[0]) in cop or parse_name(pair[1]) in cop
]
ipop_pairs = [
    (parse_name(pair[0]), parse_name(pair[1]))
    for pair in graph.node_pairs()
    if parse_name(pair[0]) in ipop or parse_name(pair[1]) in ipop
]

print(len(cop_pairs))
print(len(ipop_pairs))


with open("data/full_graph.pkl", "wb") as f:
    pickle.dump(G, f)

utils.save_graph(cop_pairs)
utils.save_ipop_graph(ipop_pairs)
