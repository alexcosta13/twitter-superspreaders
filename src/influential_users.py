from warnings import warn
import networkx as nx
import snap
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm


def content_generators(graph: nx.DiGraph, k: int) -> list:
    """
    Identify k content generators in graph

    :param graph: directed graph to analyse
    :param k: number of generators to be identified
    :return: list of the top k content generators in graph
    """
    if k * 20 > graph.number_of_nodes():
        warn("It does not make sense to have more than 5% of content generators")

    in_degree_sorted = sorted([(n, d) for n, d in graph.in_degree()], reverse=True, key=lambda x: x[1])
    content_generators_list = in_degree_sorted[:k]
    return list(dict(content_generators_list).keys())


def content_spreaders_pagerank(graph: snap.TNGraph, k: int, C=0.85, Eps=0.0001, MaxIter=100) -> list:
    """
    Identify k content spreaders in graph using pagerank

    :param graph: directed graph to analyse
    :param k: number of spreaders to be identified
    :param C: Damping factor
    :param Eps: Convergence difference
    :param MaxIter: Maximum number of iterations
    :return: list of the top k content spreaders in graph
    """
    if k * 20 > graph.GetNodes():
        warn("It does not make sense to have more than 5% of content spreaders")

    PRankH = graph.GetPageRank(C, Eps, MaxIter) # returns the PageRank for every node 
    pageRankList = [] 
    for item in PRankH: 
        pageRankList.append([item, PRankH[item]])

    dfPageRank = pd.DataFrame(pageRankList,columns=['Node', 'PageRank']) # create df with each node and the corresponding pagerank 
    dfPageRank.sort_values(by=['PageRank'], inplace=True, ascending=False);
    return dfPageRank["Node"].head(k).to_list()

def IC(g,S,mc=100):
    global cont
    """
    Input:  graph object, set of seed nodes, propagation probability
            and the number of Monte-Carlo simulations
    Output: average number of nodes influenced by the seed nodes
    """

    # Loop over the Monte-Carlo Simulations
    spread = []
    for i in range(mc):
        # Simulate propagation process      
        new_active, A = S[:], S[:]
        while new_active:

            # For each newly active node, find its neighbors that become activated
            new_ones = []
            for node in new_active:
                # get weight of the edges witht the neighborgs

                # Determine neighbors that become infected
                np.random.seed(i)
                success = np.random.uniform(0,1,len(list(g.neighbors(node)))) < [g[node][neighborg]["weight"] for neighborg in g.neighbors(node)]
                new_ones += list(np.extract(success, list(g.neighbors(node))))

            new_active = list(set(new_ones) - set(A))
            
            # Add newly activated nodes to the set of activated nodes
            A += new_active
            
        spread.append(len(A))
        
    return(np.mean(spread))

def content_spreaders_celf(g: nx.DiGraph, k: int, mc=100):  
    """
    Identify k content spreaders in graph using CELF

    :param g: directed graph to analyse
    :param k: number of spreaders to be identified
    :param mc: numper of Monte Carlo iterations
    :return: list of the top k content spreaders in graph
    """
    if k * 20 > g.number_of_nodes():
        warn("It does not make sense to have more than 5% of content spreaders")
      
    # --------------------
    # Find the first node with greedy algorithm
    # --------------------
    
    # Calculate the first iteration sorted list
    print("Inizialization:")
    marg_gain = [IC(g,[node],mc) for node in tqdm(g.nodes)]

    # Create the sorted list of nodes and their marginal gain 
    Q = sorted(zip(g.nodes, marg_gain), key=lambda x: x[1],reverse=True)

    # Select the first node and remove from candidate list
    S, spread = [Q[0][0]], Q[0][1]
    Q = Q[1:]
    
    # --------------------
    # Find the next k-1 nodes using the list-sorting procedure
    # --------------------
    print("Superspreaders extraction:")
    for _ in tqdm(range(k-1)):

        check, node_lookup = False, 0
        
        while not check:
            
            # Count the number of times the spread is computed
            node_lookup += 1
            
            # Recalculate spread of top node
            current = Q[0][0]
            
            # Evaluate the spread function and store the marginal gain in the list
            Q[0] = (current,IC(g,S+[current],mc) - spread)

            # Re-sort the list
            Q = sorted(Q, key = lambda x: x[1], reverse = True)

            # Check if previous top node stayed on top after the sort
            check = (Q[0][0] == current)

        # Select the next node
        spread += Q[0][1]
        S.append(Q[0][0])

        # Remove the selected node from the list
        Q = Q[1:]

    return(S)