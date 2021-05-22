import networkx as nx
import numpy as np
import pandas as pd


def build_spreading_graph(followers: nx.DiGraph, retweets: nx.DiGraph) -> nx.DiGraph:
    """

    :param followers:
    :param retweets:
    :type retweets:
    :return:
    """
    paths = get_shortest_paths_from_data(followers, retweets)
    edges = get_edges_from_paths(paths)
    edges = get_edges_with_normalized_weights(edges)
    spreading = nx.DiGraph()
    spreading.add_edges_from(edges)
    return spreading


def create_retweet_reduced_dataset(path: str, size: int, save: str = None):
    """
    Creates a subgraph of size number of edges and returns its nodes
    :param path: location of the graph file
    :param size: number of edges in the subgraph
    :param save: path to save the created graph, if not None
    :return: list of unique nodes
    """
    all_activity = pd.read_csv('Data/higgs-activity_time.txt', delimiter = " ", names=["SRC", "DST", "TIME", "TYPE"])
    retweet_activity = all_activity[all_activity["TYPE"] == "RT"]
    retweet_activity.drop(columns=["TYPE"], inplace=True)
    retweet_activity.sort_values(by=["TIME"])
    retweet_activity_reduced = retweet_activity.drop(columns=["TIME"])
    retweet_activity_reduced['COUNT'] = np.zeros(len(retweet_activity_reduced))
    retweet_activity_reduced = retweet_activity_reduced.groupby(["SRC", "DST"]).count()
    retweet_activity_reduced = retweet_activity_reduced.head(size)

    if save is not None:
        retweet_activity_reduced.to_csv(save, sep=" ", header=False)

    return retweet_activity_reduced

def create_followers_reduced_dataset(followers_path, retweets_path, save: str = None):
    """
    Creates a subgraph ...
    :param followers_path: 
    :param retweets_path: 
    :param save: path to save the created graph, if not None
    :return: 
    """

def get_unique_nodes_from_dataframe(df: pd.DataFrame) -> list:
    """
    Returns a list of nodes from a pandas DataFrame
    :param df: pandas DataFrame as the one returned from the create_reduced_dataset function
    :return: list[int] corresponding to the nodes
    """
    return list(set(df["SRC"].to_list() + df["DST"].to_list()))

def get_shortest_paths_from_data(followers: nx.DiGraph, retweets: nx.DiGraph):
    """

    :param followers:
    :param retweets:
    :return:
    """
    for src, dst, w in retweets.edges.data():
        try:
            path = nx.shortest_path(followers, src, dst)
            yield path, w['weight']
        except:
            pass

def get_edges_from_paths(paths):
    """

    :param paths:
    :return:
    """
    edges = {}
    for path, w in paths:
        for i in range(len(path) - 1):
            if (path[i], path[i + 1]) in edges:
                edges[(path[i], path[i + 1])] += w
            else:
                edges[(path[i], path[i + 1])] = w
    
    return edges

def get_edges_with_normalized_weights(edges):
    """

    :param edges:
    :return:
    """
    weights = {}

    for (src, dst), value in edges.items():
        weights[(src, dst)] = value

    weights_normalized = normalize_data(list(weights.values()))

    # Update of the weight. Set a minimum normalized weight of 0.1
    for i, ((src, dst), value) in enumerate(edges.items()):
        weights[(src, dst)] = weights_normalized[i] if weights_normalized[i] > 0.1 else 0.1

    output_edges = []

    for (src, dst), value in edges.items():
        temp = (src, dst, {"weight": weights[(src, dst)]})
        output_edges.append(temp)
    
    return output_edges

def normalize_data(data):
    """

    :param data:
    :return:
    """
    return (data - np.min(data)) / (np.max(data) - np.min(data))