# Christopher Shenton
# Description: A simple TCP client that sends a SYN message to initiate a connection,
# sends a data message, sends an ACK message, and sends a FIN message to close the connection.

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

def create_message(src_port, dst_port, seq_num, ack=0, syn=0, fin=0, payload=""):
    """Create a message with custom TCP header and payload"""
    try:
        if not (0 <= src_port <= 65535 and 0 <= dst_port <= 65535):
            raise ValueError("Port numbers must be between 0 and 65535")
        if not all(flag in (0, 1) for flag in (ack, syn, fin)):
            raise ValueError("Flags must be 0 or 1")
        
        payload_size = len(payload)
        if payload_size > 65535:  # 2 bytes max value
            raise ValueError("Payload size exceeds maximum allowed value")
            
        header = struct.pack(HEADER_FORMAT, src_port, dst_port, seq_num, 
                           ack, syn, fin, payload_size)
        return header + payload.encode()
    except (struct.error, ValueError) as e:
        logger.error(f"Failed to create message: {e}")
        raise
    except UnicodeEncodeError as e:
        logger.error(f"Payload encoding error: {e}")
        raise

def send_and_receive(client, message, message_type):
    """Send message and receive response with error handling"""
    try:
        client.send(message)
        logger.info(f"Sent {message_type} message")
        
        response = client.recv(1024)
        if not response:
            raise ConnectionError("Server disconnected unexpectedly")
            
        decoded_response = response.decode()
        logger.info(f"Server response to {message_type}: {decoded_response}")
        return decoded_response
    except socket.error as e:
        logger.error(f"Socket error during {message_type} transmission: {e}")
        raise
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode server response for {message_type}: {e}")
        raise

def main():
    # Server configuration
    SERVER_HOST = 'localhost'
    SERVER_PORT = 12345
    CLIENT_PORT = 44444
    
    # Create TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to server
        client.connect((SERVER_HOST, SERVER_PORT))
        logger.info(f"Connected to {SERVER_HOST}:{SERVER_PORT}")
        
        # Send SYN message
        syn_msg = create_message(CLIENT_PORT, SERVER_PORT, 1, syn=1)
        print(f"Server response: {send_and_receive(client, syn_msg, 'SYN')}")
        
        # Send data message
        payload = "Hello, Server!"
        data_msg = create_message(CLIENT_PORT, SERVER_PORT, 2, payload=payload)
        print(f"Server response: {send_and_receive(client, data_msg, 'Data')}")
        
        # Send ACK message
        ack_msg = create_message(CLIENT_PORT, SERVER_PORT, 3, ack=1)
        print(f"Server response: {send_and_receive(client, ack_msg, 'ACK')}")
        
        # Send FIN message
        fin_msg = create_message(CLIENT_PORT, SERVER_PORT, 4, fin=1)
        print(f"Server response: {send_and_receive(client, fin_msg, 'FIN')}")
        
    except ConnectionRefusedError:
        logger.error(f"Connection refused by {SERVER_HOST}:{SERVER_PORT}")
    except socket.timeout:
        logger.error("Connection timed out")
    except (ValueError, struct.error) as e:
        logger.error(f"Header creation error: {e}")
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        try:
            client.close()
            logger.info("Connection closed")
        except Exception as e:
            logger.error(f"Error closing socket: {e}")

if __name__ == "__main__":
    main()