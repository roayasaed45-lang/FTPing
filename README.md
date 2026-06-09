# FTPing – File Transfer over ICMP using Scapy

## Project Overview

FTPing is a custom protocol that combines the concepts of **FTP (File Transfer Protocol)** and **Ping (ICMP)**.

The goal of the project is to transfer a file from a client to a server using only ICMP Echo Request and Echo Reply packets. The implementation was developed in Python using the Scapy library.

---

## Features

* File transfer over ICMP packets only
* Custom ACK mechanism
* Reliable delivery despite packet loss
* Packet retransmission on timeout
* File reconstruction on the server side
* Simulation of packet loss (10% random packet drops)

---

## Protocol Design

### Start Transfer

The client starts the communication by sending:

```text
START|filename
```

The server responds with:

```text
ACK|START
```

---

### Data Transfer

The file is divided into small chunks.

Each chunk is sent as:

```text
DATA|sequence_number|data
```

Example:

```text
DATA|1|Hello
DATA|2|World
```

The server responds with:

```text
ACK|1
ACK|2
```

---

### End Transfer

When all chunks have been sent, the client sends:

```text
END
```

The server saves the reconstructed file and responds with:

```text
ACK|END
```

---

## Reliability Mechanism

ICMP does not provide reliable delivery.

To overcome this limitation:

1. Every packet requires an ACK.
2. The client waits for the correct ACK.
3. If no ACK is received within the timeout period, the packet is retransmitted.
4. The server randomly drops approximately 10% of packets to simulate a real network environment.

---

## Project Structure

```text
FTPing/
│
├── client.py
├── server.py
├── test_file.txt
├── received_file.txt
├── requirements.txt
└── README.md
```

---

## Requirements

Python 3.x

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Start the Server

```bash
sudo python server.py
```

### Start the Client

```bash
sudo python client.py
```

---

## Example Output

### Client

```text
[CLIENT] Sending: DATA|1|...
[CLIENT] Received: ACK|1

[CLIENT] Sending: END
[CLIENT] Received: ACK|END
```

### Server

```text
[RECEIVED] DATA|1|...
[ACK] Sent ACK for packet 1

[DROP] Packet ignored: END

[RECEIVED] END
[SERVER] File saved as received_file.txt
```

---

## Technologies Used

* Python
* Scapy
* ICMP Protocol
* Networking Concepts
* Reliable Data Transfer

---

## Author

Roaya Saed

Management Information Systems (MIS)

Final Networking Project
