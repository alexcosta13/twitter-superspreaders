import networkx as nx


def content_generators(graph: nx.DiGraph, k: int) -> list[int]:
    """
    Identify k content generators in graph

    :param graph: directed graph to analyse
    :param k: number of generators to be identified
    :return: list of the top k content generators in graph
    """
    in_degree_sorted = sorted([(n, d) for n, d in graph.in_degree()], reverse=True, key=lambda x: x[1])
    content_generators_list = in_degree_sorted[:k]
    return list(dict(content_generators_list).keys())


def content_spreaders(graph: nx.DiGraph, k: int) -> list[int]:
    """
    Identify k content spreaders in graph

    :param graph: directed graph to analyse
    :param k: number of spreaders to be identified
    :return: list of the top k content spreaders in graph
    """
    pass
