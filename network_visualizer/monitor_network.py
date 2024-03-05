""" This module is for reading in the pcap file """

import pyshark
from pathlib import Path
"""
TODO:
    Once static file suppport is worked out, need to implement live traffic support
"""

def read_cap(infile: str) -> None:
    """ Method to read in the capture file
    
    Args:
        None

    Returns:
        None
    """
    cap = pyshark.FileCapture(Path(infile))
    nx_data = {
        "comms_tuples": [],
        "protocol_stack": []
        }
    for packet in cap:
        nx_data["comms_tuples"].append(
            (packet.eth.src, packet.eth.dst))
        nx_data["protocol_stack"].append(packet.frame_info.protocols)
    return nx_data
