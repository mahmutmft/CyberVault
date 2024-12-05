import subprocess
import sys
import datetime

try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scapy"])
    from scapy.all import sniff, IP, TCP, UDP, ICMP

log_file = f"packet_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def log_packet(packet_info):
    with open(log_file, "a") as f:
        f.write(packet_info + "\n")

def packet_callback(packet):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        protocol = "Unknown"

        if TCP in packet:
            protocol = "TCP"
        elif UDP in packet:
            protocol = "UDP"
        elif ICMP in packet:
            protocol = "ICMP"

        packet_info = f"[{protocol}] {ip_src} --> {ip_dst}"
        print(packet_info)
        log_packet(packet_info) 

        if TCP in packet or UDP in packet:
            src_port = packet.sport
            dst_port = packet.dport
            packet_info += f" | Src Port: {src_port}, Dst Port: {dst_port}"
            print(f"{packet_info}")
            log_packet(packet_info)

        if ICMP in packet:
            print(f"    ICMP Type: {packet[ICMP].type}")
            log_packet(f"    ICMP Type: {packet[ICMP].type}")

def main():
    print(f"File: {log_file}")
    print(f"Press Ctrl+C to stop.\n")

    filter_protocol = input("Enter protocol to filter (tcp, udp, icmp, all): ").lower()
    filter_map = {
        "tcp": "tcp",
        "udp": "udp",
        "icmp": "icmp",
        "all": None
    }

    if filter_protocol not in filter_map:
        print("Invalid protocol. Capturing all packets.")
        filter_protocol = "all"

    sniff(prn=packet_callback, store=0, filter=filter_map.get(filter_protocol))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\nPackets logged in {log_file}.")
