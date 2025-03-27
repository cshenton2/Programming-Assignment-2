# Christopher Shenton
# Description: A simple TCP client that sends a SYN message to initiate a connection,
# sends a data message, sends an ACK message, and sends a FIN message to close the connection.


import socket
import struct

# Custom TCP header format: 2H (ports) + I (seq) + 3B (flags) + H (payload size)
HEADER_FORMAT = '!2HI3BH'
HEADER_SIZE = 13

def create_message(src_port, dst_port, seq_num, ack=0, syn=0, fin=0, payload=""):
    """Create a message with custom TCP header and payload"""
    payload_size = len(payload)
    header = struct.pack(HEADER_FORMAT, src_port, dst_port, seq_num, 
                        ack, syn, fin, payload_size)
    return header + payload.encode()

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
        print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")
        
        # Send SYN message to initiate connection
        syn_msg = create_message(CLIENT_PORT, SERVER_PORT, 1, syn=1)
        client.send(syn_msg)
        print(f"Server response: {client.recv(1024).decode()}")
        
        # Send data message
        payload = "Hello, Server!"
        data_msg = create_message(CLIENT_PORT, SERVER_PORT, 2, payload=payload)
        client.send(data_msg)
        print(f"Server response: {client.recv(1024).decode()}")
        
        # Send ACK message
        ack_msg = create_message(CLIENT_PORT, SERVER_PORT, 3, ack=1)
        client.send(ack_msg)
        print(f"Server response: {client.recv(1024).decode()}")
        
        # Send FIN message to close connection
        fin_msg = create_message(CLIENT_PORT, SERVER_PORT, 4, fin=1)
        client.send(fin_msg)
        print(f"Server response: {client.recv(1024).decode()}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection closed")

if __name__ == "__main__":
    main()