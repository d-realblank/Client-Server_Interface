

import os
import signal
import socket
from typing import Tuple

from click import prompt

class Client:
    """Client class for the database server."""

    # Database query prompt
    prompt: str = """\
=== Menu ===
1. Find customer
2. Add customer
3. Delete customer
4. Update customer age
5. Update customer address
6. Update customer phone
7. Print report
8. Exit
        
Select: """
    # Database response buffer size
    buffer: int = 1024

    def __init__(self, host: str, port: int) -> None:
        """Initialize the client
        :param host: The host address of the server
        """

        # Initialize the socket
        self.active: bool = True
        self.address: Tuple = host
        self.sock: socket.socket = None

    @staticmethod
    def ask_query() -> int:
        """Asks the user for a query
        :return: The query number (1 to 8)
        """

        #Loop
        while True:

            # Ask for the query
            query: str = prompt(Client.prompt, type=int)

            # Check if the query is valid
            if query in range(1, 9):
                return query

            # Print an error message
            print("Invalid query")

    @staticmethod
    def ask_yn(prompt: str) -> bool:
        """Asks the user for a yes/no answer
        :param prompt: The prompt to display
        :return: True if the answer is yes, False otherwise
        """

        # Loop
        while True:
                
            # Ask for the answer
            answer: str = prompt(prompt, type=str)

            # Check if the answer is valid
            if answer.lower() in ("y", "yes"):
                return True
            elif answer.lower() in ("n", "no"):
                return False

            # Print an error message
            print("Invalid answer")

    @staticmethod
    def ask_string(prompt: str) -> str:
        """Asks the user for a string
        :param prompt: The prompt to display
        :return: The string
        """

        # Loop
        while True:

            # Ask for the string
            string: str = prompt(prompt, type=str)

            # Check if the string is valid
            if string and len(string) > 0:
                return string

            # Print an error message
            print("Invalid string")

    @staticmethod
    def ask_int(prompt: str) -> int:
        """Asks the user for an integer
        :param prompt: The prompt to display
        :return: The integer
        """

        # Loop
        while True:

            # Ask for the integer
            val = input(prompt).strip()

            # Parse as integer
            try:
                integer = int(val)
                return integer
            except:
                # Print an error message
                print("Invalid integer")

    @staticmethod
    def println(string: str) -> None:
        """Prints a message to console with newline character
        :param string: The message to print
        """

        print(string + "\n")

    def connect(self) -> bool:
        """Connects to the server. Client shut down if connection fails.
        :return: True if the connection was successful, False otherwise
        """

        # Create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        try:
            self.sock.connect(self.address)
            return True
        except:
            # Print an error message
            Client.println("Connection failed")
            self.active = False
            return False

    def send_query(self, query: str) -> None:
        """Sends a query to the server
        :param query: The query number (1 to 8)
        """

        # Send the query
        self.sock.sendall((query + "\n").encode())

    def get_server_response(self) -> str:
        """Gets the server response
        :return: The server response
        """

        # Receive the response
        return self.sock.recv(Client.buffer).decode()

    def receive_response(self) -> str:
        """Receives the server response
        :return: The server response
        """

        # Receive the response
        response: str = self.get_server_response()

        # Return the response
        return "Server: " + response

    def query(self) -> None:
        """Queries the server"""

        # Connect to the server
        if self.connect():

            # Ask for the query
            query: int = Client.ask_query()

            #Action according to the query
            if query == 1:
                self.find_customer()
            elif query == 2:
                self.add_customer()
            elif query == 3:
                self.delete_customer()
            elif query == 4:
                self.update_age()
            elif query == 5:
                self.update_address()
            elif query == 6:
                self.update_phone()
            elif query == 7:
                self.print_report()
            elif query == 8:
                self.exit()
            else:
                # Print an error message (should never happen)
                print("Invalid query")

            # Close the connection
            self.sock.close()

    def find_customer(self) -> None:
        """Queries the server for a customer"""

        # Get client name
        name = Client.ask_string("Enter customer name: ")

        # Send the query
        self.send_query("\n".join(["find_customer", name]))
        Client.println(self.receive_response())

    def add_customer(self) -> None:
        """Adds a customer to the database"""

        # Get client name
        name = Client.ask_string("Enter customer name: ")

        # Get client age
        age = Client.ask_int("Enter customer age: ")

        # Get client address
        address = Client.ask_string("Enter customer address: ")

        # Get client phone
        phone = Client.ask_string("Enter customer phone: ")

        # Send the query
        self.send_query("\n".join(["add_customer", "{}|{}|{}|{}".format(name, age, address, phone)]))
        Client.println(self.receive_response())

    def delete_customer(self) -> None:
        """Deletes a customer from the database"""

        # Get client name
        name = Client.ask_string("Enter customer name: ")

        # Send the query
        self.send_query("\n".join(["delete_customer", name]))
        Client.println(self.receive_response())

    def update_age(self) -> None:
        """Updates a customer's age"""

        # Get client name
        name = Client.ask_string("Enter customer name: ")

        # Get client age
        age = Client.ask_int("Enter customer age: ")

        # Send the query
        self.send_query("\n".join(["update_age", name, str(age)]))
        Client.println(self.receive_response())

    def update_address(self) -> None:
        """Updates a customer's address"""

        # Get client name
        name = Client.ask_string("Enter customer name: ")

        # Get client address
        address = Client.ask_string("Enter customer address: ")

        # Send the query
        self.send_query("\n".join(["update_address", name, address]))
        Client.println(self.receive_response())

    def update_phone(self) -> None:
        """Updates a customer's phone"""

        # Get client name
        name = Client.ask_string("Enter customer name: ")

        # Get client phone
        phone = Client.ask_string("Enter customer phone: ")

        # Send the query
        self.send_query("\n".join(["update_phone", name, phone]))
        Client.println(self.receive_response())

    def print_report(self) -> None:
        """Print full report of the database"""

        # Send the query
        self.send_query("print_report")
        Client.println("\n=== Data Records ===\n" + self.get_server_response())

    def exit(self) -> None:
        """Closes client"""

        # Send the query
        self.active = False
        terminate = self.ask_yn("Are you sure you want to exit? ")

        # Terminate if the user wants to
        if terminate:
            # Send the query, get PID
            self.send_query("get_pid")
            pid = self.get_server_response()

            # kill the server
            try:
                # On Windows
                if os.name == "nt":
                    os.system("taskkill /F /PID " + pid)
                else:
                    os.kill(int(pid), signal.SIGTERM)
            except:
                # Print an error message
                Client.println("Could not kill server, manual termination required. PID: " + pid)
