import networkx as nx

def make_grid_graph(m, n):
    """
    Create an m x n 2D grid graph and relabel nodes 0..mn-1.
    """
    G = nx.grid_2d_graph(m, n)
    G = nx.convert_node_labels_to_integers(G)
    return G

def draw_graph(G, ax=None):
    """
    Draw the grid graph with consistent layout.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        fig, ax = plt.subplots()

    pos = {i: (i % 5, -(i // 5)) for i in G.nodes()}  # good for up to 5x5
    nx.draw(G, pos, with_labels=True, node_size=600, ax=ax)
    return ax
