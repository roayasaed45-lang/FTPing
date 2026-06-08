from scapy.all import IP, ICMP, Raw, send, sniff
import time

SERVER_IP = "127.0.0.1"
INPUT_FILE = "test_file.txt"
CHUNK_SIZE = 32
TIMEOUT = 2
IFACE = "lo0"


def send_and_wait_for_ack(message, expected_ack):
    while True:
        print(f"[CLIENT] Sending: {message}")

        packet = IP(dst=SERVER_IP) / ICMP(type="echo-request") / Raw(load=message)
        send(packet, verbose=False)

        def is_expected_ack(pkt):
            if pkt.haslayer(ICMP) and pkt.haslayer(Raw):
                raw_data = pkt[Raw].load.decode(errors="ignore")
                return raw_data == expected_ack
            return False

        responses = sniff(
            filter="icmp",
            timeout=TIMEOUT,
            count=1,
            lfilter=is_expected_ack,
            promisc=False,
            iface=IFACE
        )

        if responses:
            print(f"[CLIENT] Received: {expected_ack}")
            return

        print("[CLIENT] No valid ACK, resending...")
        time.sleep(1)


send_and_wait_for_ack("START|test_file.txt", "ACK|START")

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    content = file.read()

chunks = [content[i:i + CHUNK_SIZE] for i in range(0, len(content), CHUNK_SIZE)]

for index, chunk in enumerate(chunks, start=1):
    message = f"DATA|{index}|{chunk}"
    expected_ack = f"ACK|{index}"
    send_and_wait_for_ack(message, expected_ack)

send_and_wait_for_ack("END", "ACK|END")

print("[CLIENT] File transfer completed successfully.")
