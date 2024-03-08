import networkx as nx
from monitor_network import read_cap
from pyvis.network import Network
import matplotlib.pyplot as plt
import argparse
import random
import pandas as pd

def get_args():
    """The method to read in the terminal arguments
    
    Args:
        None
    
    Returns:
        None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", 
        "--input_file", 
        help="The input capture file", 
        required=True
    )
    args = parser.parse_args()
    return args

def generate_color_map(data) -> dict:
    """ Method to generate random RGB color map
    
    This method takes in the data and pulls out the protocol stack. From there it randomly generates
        a RGB combination for each protocol.
        
    Args:
        data: the dictionary holding the communication tuple and the protocol stacks
    
    Returns:
        color_map: dictionary holding protocols and their associatied colors.
    """
    min_rgb, max_rgb = 0, 255
    color_map = {}
    protocol_list = list(pd.DataFrame(data)["protocol_stack"].unique())
    for proto in protocol_list:
        color_map[proto] = (
            random.randint(min_rgb, max_rgb),  # Red
            random.randint(min_rgb, max_rgb),  # Green
            random.randint(min_rgb, max_rgb)   # Blue
        )
    return color_map

def make_network(net: nx.MultiDiGraph, data: dict) -> nx.MultiDiGraph:
    """ Method for making the nodes on the graph
    
    Args:
        net: a networkx multidigraph instance
        data: the data to plot

    Returns:
        net: The constructed networkx MultiDiGraph
    """
    idx = 0
    for coms, protos in zip(data["comms_tuples"], data["protocol_stack"]):
        # If the graph is empty make the first nodes / edges
        if not net.edges:
            net.add_edge(coms[0], coms[1], value=protos)
        else:
            if net.has_edge(coms[0], coms[1]):
                edge_data = net.get_edge_data(coms[0], coms[1])
                if edge_data[0]["value"].split(":")[-1] != protos:
                    net.add_edge(coms[0], coms[1], value=protos)
            else:
                net.add_edge(coms[0], coms[1], value=protos)
        if idx == 100:
            break
        idx += 1
    return net

def plot_net(net: nx.MultiDiGraph, color_map: dict) -> None:
    """ The method to plot the network
    
    Args:
        net: the completed networkx object
        color_map: the protocol based color map
    
    Returns:
        None
    """
    net_graph = Network(bgcolor="#222222", font_color="white", directed=True)
    nx.set_edge_attributes(net, color_map, name="color")
    net_graph.from_nx(net, show_edge_weights=False)
    net_graph.set_edge_smooth('dynamic')
    net_graph.show("./test.html", notebook=False)

def main() -> None:
    """The main method
    
    Args:
        None
    
    Returns:
        None
    """
    args = get_args()  # Get the terminal args
    data = read_cap(args.input_file) # Parse the data
    color_map = generate_color_map(data) # Generate the protocol color map
    net = nx.MultiDiGraph() 
    net = make_network(net, data) # make the networkx object
    plot_net(net, color_map) # plot the network

if __name__ == "__main__":
    main()
