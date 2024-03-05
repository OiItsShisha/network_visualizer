import networkx as nx
from monitor_network import read_cap
from pyvis.network import Network
import matplotlib.pyplot as plt
import argparse

def get_args():
    """The method to read in the terminal arguments
    
    Args:
        None
    
    Returns:
        None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i" "--input_file", help="The input capture file", required=True)
    args = parser.parse_args()
    return args


def make_network(net: nx.MultiDiGraph, data: dict) -> nx.MultiDiGraph:
    """ Method for making the nodes on the graph
    
    Args:
        net: a networkx multidigraph instance
        data: the data to plot

    Returns:
        None
    """
    idx = 0
    for coms, protos in zip(data["comms_tuples"], data["protocol_stack"]):
        # If the graph is empty make the first nodes / edges
        proto = protos.split(":")[-1]
        if not net.edges:
            # net.add_edge adds nodes if they don't exist
            net.add_edge(coms[0], coms[1], value=proto)
        else:
            if net.has_edge(coms[0], coms[1]):
                edge_data = net.get_edge_data(coms[0], coms[1])
                if edge_data[0]["value"].split(":")[-1] != proto:
                    net.add_edge(coms[0], coms[1], value=protos)
            else:
                net.add_edge(coms[0], coms[1], value=proto)
        if idx == 100:
            break
        idx += 1
    return net

def plot_net(net: nx.MultiDiGraph):
    net_graph = Network(bgcolor="#222222", font_color="white", directed=True)
    net_graph.from_nx(net)
    net_graph.set_edge_smooth('dynamic')
    net_graph.show("./test.html", notebook=False)

def main() -> None:
    """The main method
    
    Args:
        None
    
    Returns:
        None
    """
    args = get_args()
    data = read_cap(args.input_file)
    net = nx.MultiDiGraph()
    net = make_network(net, data)
    plot_net(net)

if __name__ == "__main__":
    main()
