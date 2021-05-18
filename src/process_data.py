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
    pass


def create_reduced_dataset(path: str, size: int, save: str = None) -> pd.Dataframe:
    """

    :param path:
    :param size:
    :param save:
    :return:
    """
    all_activity = pd.read_csv(path, delimiter=" ", names=["SRC", "DST", "TIME", "TYPE"])
    retweet_activity = all_activity[all_activity["TYPE"] == "RT"]
    retweet_activity.drop(columns=["TYPE"], inplace=True)
    retweet_activity.sort_values(by=["TIME"])
    retweet_activity_reduced = retweet_activity.drop(columns=["TIME"])
    retweet_activity_reduced = retweet_activity_reduced.head(size)

    if save is not None:
        retweet_activity_reduced['COUNT'] = np.zeros(len(retweet_activity_reduced))
        retweet_activity_reduced = retweet_activity_reduced.groupby(["SRC", "DST"]).count()
        retweet_activity_reduced.to_csv(save, sep=" ", header=False)

    return retweet_activity_reduced


def get_shortest_paths_from_data(followers: nx.DiGraph, retweet: nx.DiGraph) -> list[list[int], dict]:
    for src, dst, w in retweet.edges.data():
        try:
            path = nx.shortest_path(followers, src, dst)
            yield path, w['weight']
        except:
            pass


def get_edges_from_paths(paths: list[list[int], dict]) -> (int, int, dict):
    edges = {}
    for path, w in paths:
        for i in range(len(path) - 1):
            if (path[i], path[i + 1]) in edges:
                print(path[i])
                edges[(path[i], path[i + 1])] += w
            else:
                edges[(path[i], path[i + 1])] = w

    for key, value in edges.items():
        temp = (*key, {'weights': value})
        yield temp
