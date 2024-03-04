import networkx as nx
from monitor_network import read_cap
from pyvis.network import Network

def make_nodes(net, data):
    """ Method for making the nodes on the graph"""
    for coms, protos in zip(data["comms_tuples"], data["protocol_stack"]):
        net.add_node(coms[0]) # add src_addr
        net.add_node(coms[1]) # add dst_addr
        net.add_edge(coms[0], coms[1], value=protos)
        print(net.nodes)
        exit()
    net.show(".\\test.html", notebook=False)

def main() -> None:
    data = read_cap()
    net = Network(bgcolor="#222222", font_color="white")
    make_nodes(net, data)

if __name__ == "__main__":
    main()
