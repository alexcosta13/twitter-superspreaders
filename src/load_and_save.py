import networkx as nx


def load_directed_graph(path: str, weighted=False) -> nx.DiGraph:
    """
    Loads a directed graph from a path

    :param path: location of the graph file
    :param weighted: indicates whether the graph is weighted
    :return: the loaded graph
    """
    if not weighted:
        graph = nx.read_edgelist(path=path, nodetype=int, create_using=nx.DiGraph())
    else:
        graph = nx.read_edgelist(path=path, nodetype=int, data=(('weight', int),), create_using=nx.DiGraph())
    return graph
