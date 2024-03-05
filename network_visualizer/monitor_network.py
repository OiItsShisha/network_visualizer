import pyshark

def read_cap() -> None:
    cap = pyshark.FileCapture("./home_wifi.pcapng")
    nx_data = {
        "comms_tuples": [],
        "protocol_stack": []
        }
    for packet in cap:
        nx_data["comms_tuples"].append(
            (packet.eth.src, packet.eth.dst))
        nx_data["protocol_stack"].append(packet.frame_info.protocols)
    return nx_data

if __name__ == "__main__":
    dict_ = read_cap()
    print(dict_)