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
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Custom TCP header format: 2H (ports) + I (seq) + 3B (flags) + H (payload size)
HEADER_FORMAT = '!2HI3BH'
HEADER_SIZE = 13

def parse_header(data):
    """Parse the custom TCP header from received data"""
    try:
        if len(data) < HEADER_SIZE:
            raise ValueError(f"Received data too short: {len(data)} bytes, expected at least {HEADER_SIZE}")
        return struct.unpack(HEADER_FORMAT, data[:HEADER_SIZE])
    except struct.error as e:
        logger.error(f"Failed to unpack header: {e}")
        raise
    except ValueError as e:
        logger.error(f"Invalid header length: {e}")
        raise

def handle_client(client_socket, addr):
    """Handle incoming client connection"""
    try:
        while True:
            # Receive message
            try:
                data = client_socket.recv(1024)
                if not data:
                    logger.info(f"Client {addr} disconnected")
                    break
            except socket.error as e:
                logger.error(f"Receive error from {addr}: {e}")
                break
                
            # Parse header and payload
            try:
                src_port, dst_port, seq_num, ack, syn, fin, payload_size = parse_header(data)
                if payload_size > len(data) - HEADER_SIZE:
                    raise ValueError(f"Payload size {payload_size} exceeds received data length")
                
                payload = data[HEADER_SIZE:HEADER_SIZE + payload_size].decode() if payload_size > 0 else ""
                
                # Validate header values
                if not (0 <= src_port <= 65535 and 0 <= dst_port <= 65535):
                    logger.warning(f"Invalid port numbers from {addr}: src={src_port}, dst={dst_port}")
                if not all(flag in (0, 1) for flag in (ack, syn, fin)):
                    logger.warning(f"Invalid flag values from {addr}: ack={ack}, syn={syn}, fin={fin}")
                
                # Log received header
                logger.info(f"Received from {addr} - Src: {src_port}, Dst: {dst_port}, Seq: {seq_num}, "
                           f"ACK: {ack}, SYN: {syn}, FIN: {fin}, Payload Size: {payload_size}")
                
                # Determine response based on flags
                if syn:
                    response = "SYN received – connection initiated"
                elif ack:
                    response = "ACK received – message acknowledged"
                elif fin:
                    response = "FIN received – connection closing"
                else:
                    response = f"Data received – payload length: {payload_size}"
                
                # Send response
                client_socket.send(response.encode())
                logger.info(f"Sent to {addr}: {response}")
                
                # Exit if FIN received
                if fin:
                    break
                    
            except UnicodeDecodeError as e:
                logger.error(f"Payload decode error from {addr}: {e}")
                client_socket.send("Error: Invalid payload encoding".encode())
            except ValueError as e:
                logger.error(f"Header validation error from {addr}: {e}")
                client_socket.send(f"Error: {str(e)}".encode())
                
    except Exception as e:
        logger.error(f"Unexpected error handling client {addr}: {e}")
    finally:
        try:
            client_socket.close()
            logger.info(f"Connection with {addr} closed")
        except Exception as e:
            logger.error(f"Error closing client socket {addr}: {e}")

def main():
    # Server configuration
    HOST = 'localhost'
    PORT = 12345
    
    # Create TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        server.listen(1)
        logger.info(f"Server listening on {HOST}:{PORT}")
        
        while True:
            try:
                client_socket, addr = server.accept()
                logger.info(f"Connected by {addr}")
                handle_client(client_socket, addr)
                
            except socket.error as e:
                logger.error(f"Accept error: {e}")
                break
                
    except socket.error as e:
        logger.error(f"Server socket error: {e}")
    except Exception as e:
        logger.error(f"Unexpected server error: {e}")
    finally:
        try:
            server.close()
            logger.info("Server closed")
        except Exception as e:
            logger.error(f"Error closing server socket: {e}")

if __name__ == "__main__":
    main()