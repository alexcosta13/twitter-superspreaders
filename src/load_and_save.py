import networkx as nx
import snap


def load_networkx_directed_graph(path: str, weighted=False) -> nx.DiGraph:
    """
    Loads a directed graph from a path

    :param path: location of the graph file
    :param weighted: indicates whether the graph is weighted
    :return: the loaded graph in networkx format
    """
    if not weighted:
        graph = nx.read_edgelist(path=path, nodetype=int, create_using=nx.DiGraph())
    else:
        graph = nx.read_edgelist(path=path, nodetype=int, data=(('weight', float),), create_using=nx.DiGraph())
    return graph


def load_snap_directed_graph(path: str) -> snap.TNGraph:
    """
    Loads a directed graph from a path

    :param path: location of the graph file
    :return: the loaded graph in snap format
    """
    return snap.LoadEdgeList(snap.TNGraph, path, 0, 1)


def save_networkx_directed_graph(graph: nx.DiGraph, path: str, weighted=False):
    """
    Saves a directed graph from a path

    :param graph: location of the graph file
    :param path: location of the graph file
    :param weighted: indicates whether the graph is weighted
    :return:
    """
    edge_list = []

    if weighted:
        for src, dst, value in graph.edges.data():
            temp = f"{src} {dst} {value['weight']}\n"
            edge_list.append(temp)
    else:
        for src, dst, value in graph.edges():
            temp = f"{src} {dst}\n"
            edge_list.append(temp)

    with open(path, "w") as file_:
        file_.writelines(edge_list)


def save_list(list_: list, file_path: str) -> None:
    """

    :param list_:
    :param file_path:
    :return:
    """
    list_to_string = ' '.join(map(str, list_))
    with open(file_path, 'w') as f:
        f.write(list_to_string)


def load_list(file_path: str) -> list:
    """

    :param file_path:
    :return:
    """
    with open(file_path, 'r') as f:
        line = f.read()
    return list(map(int, line.split()))
