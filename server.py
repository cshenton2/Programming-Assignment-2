# Christopher Shenton
# Description: A simple TCP server that listens for a client connection, receives a SYN message to initiate a connection,
# receives a data message, receives an ACK message, and receives a FIN message to close the connection.

import socket
import struct

# Custom TCP header format: 2H (ports) + I (seq) + 3B (flags) + H (payload size)
HEADER_FORMAT = '!2HI3BH'
HEADER_SIZE = 13

def parse_header(data):
    """Parse the custom TCP header from received data"""
    return struct.unpack(HEADER_FORMAT, data[:HEADER_SIZE])

def handle_client(client_socket):
    """Handle incoming client connection"""
    try:
        while True:
            # Receive message
            data = client_socket.recv(1024)
            if not data:
                break
                
            # Parse header
            src_port, dst_port, seq_num, ack, syn, fin, payload_size = parse_header(data)
            payload = data[HEADER_SIZE:].decode() if payload_size > 0 else ""
            
            # Log received header
            print(f"Received - Src: {src_port}, Dst: {dst_port}, Seq: {seq_num}, "
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
            
            # Send response and log it
            client_socket.send(response.encode())
            print(f"Sent response: {response}")
            
            # Exit if FIN received
            if fin:
                break
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Client connection closed")

def main():
    # Server configuration
    HOST = 'localhost'
    PORT = 12345
    
    # Create TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    
    print(f"Server listening on {HOST}:{PORT}")
    
    try:
        # Accept single client connection
        client_socket, addr = server.accept()
        print(f"Connected by {addr}")
        handle_client(client_socket)
        
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server.close()
        print("Server closed")

if __name__ == "__main__":
    main()