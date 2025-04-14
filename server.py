# Christopher Shenton
# Description: A simple TCP server that listens for a client connection, receives a SYN message to initiate a connection,
# receives a data message, receives an ACK message, and receives a FIN message to close the connection.

import socket
import struct
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

HEADER_FORMAT = '!2HI3BH'
HEADER_SIZE = 13

def parse_header(data):
    """Parse the custom TCP header from received data"""
    if len(data) < HEADER_SIZE:
        raise ValueError(f"Received data too short: {len(data)} bytes, expected at least {HEADER_SIZE}")
    return struct.unpack(HEADER_FORMAT, data[:HEADER_SIZE])

def handle_client(client_socket, addr):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                logger.info(f"Client {addr} disconnected")
                break

            try:
                src_port, dst_port, seq, ack, syn, fin, payload_size = parse_header(data)
                payload = data[HEADER_SIZE:HEADER_SIZE + payload_size].decode() if payload_size else ""

                logger.info(f"Received Header from {addr}: SrcPort={src_port}, DstPort={dst_port}, Seq={seq}, "
                            f"ACK={ack}, SYN={syn}, FIN={fin}, PayloadSize={payload_size}")

                if syn:
                    response = "SYN received – connection initiated"
                elif ack:
                    response = "ACK received – message acknowledged"
                elif fin:
                    response = "FIN received – connection closing"
                else:
                    response = f"Data received – payload length: {payload_size}"

                client_socket.send(response.encode())
                logger.info(f"Sent to {addr}: {response}")

                if fin:
                    break

            except (ValueError, struct.error) as e:
                error_msg = f"Header parse error: {e}"
                logger.error(error_msg)
                client_socket.send(error_msg.encode())
            except UnicodeDecodeError:
                logger.error("Payload decoding error")
                client_socket.send("Error: Invalid payload encoding".encode())

    finally:
        client_socket.close()
        logger.info(f"Connection with {addr} closed")

def main():
    HOST = 'localhost'
    PORT = 12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        server.listen(1)
        logger.info(f"Server listening on {HOST}:{PORT}")

        while True:
            client_socket, addr = server.accept()
            logger.info(f"Connected by {addr}")
            handle_client(client_socket, addr)

    except Exception as e:
        logger.error(f"Server error: {e}")
    finally:
        server.close()
        logger.info("Server shut down")

if __name__ == "__main__":
    main()
