

import os
from typing import Tuple
from .database import Database
from socket import socket
from socketserver import BaseRequestHandler, TCPServer, BaseServer, StreamRequestHandler

class DatabaseServer(TCPServer):
    """Database server object."""

    @property
    def getpid(self) -> int:
        """Get the process ID of the server.
        :return: The process ID
        """

        return os.getpid()

    def __init__(self, file: str, server_address: Tuple, handler: BaseRequestHandler, bind_and_activate: bool = True) -> None:
        """Initialize the server
        :param file: The database file
        :param server_address: The server address
        :param handler: The request handler
        :param bind_and_activate: Whether to bind and activate the server
        """

        self.pid: int = os.getpid()
        self.file: str = file
        self.database: Database = Database(file)
        TCPServer.__init__(self, server_address, handler, bind_and_activate)

class DatabaseHandler(StreamRequestHandler):
    """Database request handler."""

    def __init__(self, request: socket, client_address: Tuple, server: BaseServer) -> None:
        """Initialize the handler
        :param request: The request socket
        :param client_address: The client address
        :param server: The server
        """
    
        self.server: BaseServer = server
        self.database: Database = server.database
        StreamRequestHandler.__init__(self, request, client_address, server)

    def readline(self) -> str:
        """Read a line from the client
        :return: The line
        """

        # Read the line
        line: str = self.rfile.readline().decode()

        # Strip the line
        return line.strip()

    def writeline(self, response: str) -> None:
        """Write a line to the client
        :param response: The text to write to the server response
        """

        # Write the line
        self.wfile.write((response + "\n").encode())

    def handle(self) -> None:
        """Handles requests"""

        # Read the request
        request_type = self.readline()

        # Action according to the request type
        if request_type == "find_customer":
            self.find_customer()
        elif request_type == "add_customer":
            self.add_customer()
        elif request_type == "delete_customer":
            self.delete_customer()
        elif request_type == "update_age":
            self.update_age()
        elif request_type == "update_address":
            self.update_address()
        elif request_type == "update_phone":
            self.update_phone()
        elif request_type == "print_report":
            self.print_report()
        elif request_type == "get_pid":
            self.get_pid()
        else:
            # Print an error message (should never happen)
            self.writeline("Invalid request")
        
    def find_customer(self) -> None:
        """Finds a customer"""

        # Read the name
        name: str = self.readline()

        # Find the customer
        customer = self.database.get_customer(name)

        # Handle null customer
        if customer is None:
            self.writeline("Customer not found")
        else:
            self.writeline(customer)
        
    def add_customer(self) -> None:
        """Adds a customer"""

        # Read the line
        line = self.readline()
        # Parse the line into a customer
        customer = Database.process_line(line)

        if customer != None:  
            # Add the customer
            if self.database.add_customer(customer):
                # Write the response
                self.writeline("Customer added")
            else:
                # Write the response
                self.writeline("Customer already exists")
        else:
            # Write the response
            self.writeline("Invalid customer")
    
    def delete_customer(self) -> None:
        """Deletes a customer"""

        # Read the name
        name: str = self.readline()

        # Delete the customer
        if self.database.delete_customer(name):
            # Write the response
            self.writeline("Customer deleted")
        else:
            # Write the response
            self.writeline("Customer not found")

    def update_age(self) -> None:
        """Updates the age of a customer"""

        # Read the name
        name: str = self.readline()

        try:
            # Read the age
            age: int = int(self.readline())

            # Update the age
            if self.database.update_age(name, age):
                # Write the response
                self.writeline("Age updated")
            else:
                # Write the response
                self.writeline("Customer not found")
        except:
            # Write the response
            self.writeline("Invalid age")

    def update_address(self) -> None:
        """Updates the address of a customer"""

        # Read the name
        name: str = self.readline()

        # Read the address
        address: str = self.readline()

        # Update the address
        if self.database.update_address(name, address):
            # Write the response
            self.writeline("Address updated")
        else:
            # Write the response
            self.writeline("Customer not found")

    def update_phone(self) -> None:
        """Updates the phone number of a customer"""

        # Read the name
        name: str = self.readline()

        # Read the phone number
        phone: str = self.readline()

        # Update the phone number
        if self.database.update_phone(name, phone):
            # Write the response
            self.writeline("Phone number updated")
        else:
            # Write the response
            self.writeline("Customer not found")

    def print_report(self) -> None:
        """Prints the report"""

        # Print the report
        self.writeline("\n"+ self.database.print_report())

    def get_pid(self) -> None:
        """Gets the process ID of the server"""

        # Write the response
        self.writeline(str(self.server.pid))