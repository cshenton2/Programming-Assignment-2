# Christopher Shenton
# Description: A simple TCP client that sends a SYN message to initiate a connection,
# sends a data message, sends an ACK message, and sends a FIN message to close the connection.

import socket
import struct
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

HEADER_FORMAT = '!2HI3BH'
HEADER_SIZE = 13

def create_message(src_port, dst_port, seq_num, ack=0, syn=0, fin=0, payload=""):
    if not (0 <= src_port <= 65535 and 0 <= dst_port <= 65535):
        raise ValueError("Invalid port values")
    if not all(flag in (0, 1) for flag in (ack, syn, fin)):
        raise ValueError("Flags must be 0 or 1")

    payload_bytes = payload.encode()
    payload_size = len(payload_bytes)
    header = struct.pack(HEADER_FORMAT, src_port, dst_port, seq_num, ack, syn, fin, payload_size)
    return header + payload_bytes

def send_and_receive(sock, message, label):
    try:
        sock.send(message)
        logger.info(f"Sent {label}")
        response = sock.recv(1024).decode()
        print(f"[{label} Response] {response}")
    except Exception as e:
        logger.error(f"Error during {label} exchange: {e}")

def main():
    SERVER_HOST = 'localhost'
    SERVER_PORT = 12345
    CLIENT_PORT = 54321  # Arbitrary client port
    seq = 1

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((SERVER_HOST, SERVER_PORT))
        logger.info(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")

        # SYN message
        msg_syn = create_message(CLIENT_PORT, SERVER_PORT, seq, syn=1)
        send_and_receive(client, msg_syn, "SYN")
        seq += 1

        # Data message
        payload = "Hello, Server!"
        msg_data = create_message(CLIENT_PORT, SERVER_PORT, seq, payload=payload)
        send_and_receive(client, msg_data, "DATA")
        seq += 1

        # ACK message
        msg_ack = create_message(CLIENT_PORT, SERVER_PORT, seq, ack=1)
        send_and_receive(client, msg_ack, "ACK")
        seq += 1

        # FIN message
        msg_fin = create_message(CLIENT_PORT, SERVER_PORT, seq, fin=1)
        send_and_receive(client, msg_fin, "FIN")

    except ConnectionRefusedError:
        logger.error("Connection refused by server")
    finally:
        client.close()
        logger.info("Client socket closed")

if __name__ == "__main__":
    main()
