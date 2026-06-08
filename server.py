from scapy.all import IP, ICMP, Raw, send, sniff
import random

OUTPUT_FILE = "received_file.txt"
DROP_RATE = 10  # 1 out of 10 packets will be dropped

received_chunks = {}


def send_ack(client_ip, ack_message):
    packet = IP(dst=client_ip) / ICMP(type="echo-reply") / Raw(load=ack_message)
    send(packet, verbose=False)


def handle_packet(packet):
    if not packet.haslayer(ICMP) or not packet.haslayer(Raw):
        return

    # Echo Request only
    if packet[ICMP].type != 8:
        return

    client_ip = packet[IP].src
    message = packet[Raw].load.decode(errors="ignore")

    # Simulate packet loss
    if random.randint(1, DROP_RATE) == 1:
        print(f"[DROP] Packet ignored: {message}")
        return

    print(f"[RECEIVED] {message}")

    if message.startswith("START|"):
        received_chunks.clear()
        send_ack(client_ip, "ACK|START")
        print("[SERVER] File transfer started")

    elif message.startswith("DATA|"):
        parts = message.split("|", 2)

        if len(parts) < 3:
            return

        seq = int(parts[1])
        data = parts[2]

        received_chunks[seq] = data

        send_ack(client_ip, f"ACK|{seq}")
        print(f"[ACK] Sent ACK for packet {seq}")

    elif message == "END":

        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            for seq in sorted(received_chunks.keys()):
                file.write(received_chunks[seq])

        send_ack(client_ip, "ACK|END")

        print(f"[SERVER] File saved as {OUTPUT_FILE}")


print("[SERVER] FTPing server is running...")
print("[SERVER] Waiting for ICMP packets...")

sniff(
    filter="icmp",
    prn=handle_packet,
    promisc=False,
    iface="lo0"
)
