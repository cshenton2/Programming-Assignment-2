# Christopher Shenton
# Makefile for Programming Assignment 2

# Define variables
PYTHON := python3
SERVER := server.py
CLIENT := client.py

build:
	@echo "Nothing to build for Python"

run-server:
	@echo "Starting server..."
	@$(PYTHON) $(SERVER)

run-client:
	@echo "Starting client..."
	@$(PYTHON) $(CLIENT)

clean:
	@echo "Nothing to clean for Python"
