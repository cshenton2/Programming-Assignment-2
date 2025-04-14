# Programming Assignment 2 Design Explanation

## Overview

This project implements a client-server model using TCP socket programming in Python. It simulates the TCP protocol by using a custom TCP-style header. The client constructs messages with a header and proper payload, and the server parses and processes them as expected.

## Custom Header Format and Structure

The custom header is a fixed-length binary structure which uses 13 bytes. It is designed using Python’s built-in 'struct' module following the format below:

### Header Layout

| Field         | Size     | Description                          |
|---------------|----------|--------------------------------------|
| Source Port   | 2 bytes  | Arbitrary client-side port number    |
| Dest Port     | 2 bytes  | Server's listening port              |
| Sequence No   | 4 bytes  | Message sequence number              |
| ACK Flag      | 1 byte   | 0 or 1 (acknowledgment)              |
| SYN Flag      | 1 byte   | 0 or 1 (synchronize/start handshake) |
| FIN Flag      | 1 byte   | 0 or 1 (message finishes/terminates) |
| Payload Size  | 2 bytes  | Length of payload that follows the header |


Total Header Size: 13 bytes

### Struct Format String

```python
HEADER_FORMAT = '!2HI3BH'
```
! = network (big-endian) byte order

2H = Source port (2 bytes), Destination port (2 bytes)

I = Sequence number (4 bytes)

3B = ACK, SYN, FIN flags (1 byte each)

H = Payload size (2 bytes)

This format allows for consistent parsing of messages and aligns with TCP concepts like connection setup (SYN), acknowledgment (ACK), and connection termination (FIN).

## Server Logic and Parsing
The server listens on a fixed port for one client at a time.

Header Parsing
The parse_header() function verifies the message and extracts header fields.

```
src_port, dst_port, seq, ack, syn, fin, payload_size = parse_header(data)
```

Response Logic
The server determines its response based on the values of the SYN, ACK, and FIN flags in the header:

SYN == 1:
Response → "SYN received – connection initiated"

ACK == 1:
Response → "ACK received – message acknowledged"

FIN == 1:
Response → "FIN received – connection closing"

Else (all flags 0):
Response → "Data received – payload length: X"

## Error Handling and Design Decisions

For error handling, the server first checks for improper messages:

Ensures received data is at least 13 bytes long, validates flags are either 0 or 1, then confirms the payload size matches the declared value

The server wraps payload decoding in a try-except block to catch decoding errors if the payload cannot be interpreted as a UTF-8 string.

### Logging for Debugging
The server.py and client.py files both use Python's built in logging module to track connection setup, header content, server decisions and responses, and error messages