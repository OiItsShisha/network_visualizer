import networkx as nx
from monitor_network import read_cap
from pyvis.network import Network
import matplotlib.pyplot as plt

def make_nodes(net, data):
    """ Method for making the nodes on the graph"""
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
                net.add_node(coms[0]) # add src_addr
                net.add_node(coms[1]) # add dst_addr
                net.add_edge(coms[0], coms[1], value=proto)
        if idx == 100:
            break
        idx += 1
    net_graph = Network(bgcolor="#222222", font_color="white", directed=True)
    net_graph.from_nx(net)
    net_graph.set_edge_smooth('dynamic')
    net_graph.show("./test.html", notebook=False)

def main() -> None:
    data = read_cap()
    net = nx.MultiDiGraph()
    make_nodes(net, data)

if __name__ == "__main__":
    main()
