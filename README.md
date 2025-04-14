# Programming Assignment 2
### Author: Christopher Shenton

## Overview
This project implements a client-server model using TCP socket programming in Python. It simulates the TCP protocol by using a custom TCP-style header. The client constructs messages with a header and proper payload, and the server parses and processes them as expected.

---

## How to Build and Run
To build and run the project, run the server.py file then the client.py file using the following commands:

### Run the Server
```bash
make run-server
```

### Run the Client
```bash
make run-client
```
'make build' and 'make clean' are not necessary commands as this project was created in Python and server/client files do not need to be compiled.

## Required Libraries
All dependencies are already included in Python's standard library:
socket, struct, logging, and sys

## Message Header Format Explanation
Each message from the client has the following fixed-format header:

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

The server decodes and reacts to each message using these flags:

SYN = 1: connection initiation
ACK = 1: acknowledgment of previous message
FIN = 1: signals connection close
All flags 0: standard data message

