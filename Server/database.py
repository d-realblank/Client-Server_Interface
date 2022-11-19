

from typing import List, Dict

class Database:
    """Database storage class structure."""

    def __init__(self, file: str) -> None:
        """Initialize the database
        :param file: The database file
        """

        # Initialize the database
        self.fName: str = file
        self.database: Dict = {}

        try:
            # Open the file
            with open(file) as f:
                # Read the file
                lines = f.readlines()
                for line in lines:
                    customer = Database.process_line(line)
                    # Add if valid customer
                    if customer != None:
                        self.add_customer(customer, False)
                
                # Update the file
                self.update_file()
        except:
            # If invalid, create a new file
            print("Invalid database file, creating new file")
            with open(file, "w") as f:
                pass

    @staticmethod
    def process_line(line: str) -> List:
        """Process a line from the database file
        :param line: The line to process
        :return: The customer data
        """

        # Split the line
        data = line.strip().split("|")

        # Check if the line length is valid
        if len(data) != 4:
            return None
        
        # Trim whitespace
        data = [x.strip() for x in data]

        # Check if the data is valid
        if len(data[0]) == 0:
            return None

        try:
            # Parse age into number
            data[1] = int(data[1])
        except:
            # If failed, use 0 as age
            data[1] = 0

        # Return the data
        return data

    @staticmethod
    def format_customer(name: str, data: List) -> str:
        """Format a customer into a string
        :param customer: The customer to format
        :return: The database string
        """

        # Format the customer
        return "{}|{}|{}|{}".format(name, data[0], data[1], data[2])

    def has_customer(self, name: str) -> bool:
        """Check if the database has a customer
        :param name: The customer name
        :return: True if the customer exists, False otherwise
        """

        # Check if the customer exists
        return name in self.database

    def get_customer(self, name: str) -> str:
        """Get a customer from the database
        :param name: The customer name
        :return: The customer database string
        """

        if self.has_customer(name):
            # Return the customer
            return Database.format_customer(name, self.database[name])
        else:
            # Return an error message
            return None

    def add_customer(self, data: List, update: bool = True) -> bool:
        """Add a customer to the database
        :param data: The customer data
        :param update: Whether to update the file
        :return: True if the customer was added, False otherwise
        """

        # Check if the customer exists
        if not self.has_customer(data[0]):

            # Add the customer
            self.database[data[0]] = data[1:]
            if update:
                # Update the file
                self.update_file()
            return True

        return False

    def delete_customer(self, name: str, update: bool = True) -> bool:
        """Delete a customer from the database
        :param name: The customer name
        :param update: Whether to update the file
        :return: True if the customer was deleted, False otherwise
        """

        # Check if the customer exists
        if self.has_customer(name):

            # Delete the customer
            del self.database[name]
            if update:
                # Update the file
                self.update_file()
            return True

        return False

    def update_age(self, name: str, age: int, update: bool = True) -> bool:
        """Update a customer's age
        :param name: The customer name
        :param age: The customer age
        :param update: Whether to update the file
        :return: True if the customer was updated, False otherwise
        """

        # Check if the customer exists
        if self.has_customer(name):

            # Update the customer
            self.database[name][0] = age
            if update:
                # Update the file
                self.update_file()
            return True

        return False

    def update_address(self, name: str, address: str, update: bool = True) -> bool:
        """Update a customer's address
        :param name: The customer name
        :param address: The customer address
        :param update: Whether to update the file
        :return: True if the customer was updated, False otherwise
        """

        # Check if the customer exists
        if self.has_customer(name):

            # Update the customer
            self.database[name][1] = address
            if update:
                # Update the file
                self.update_file()
            return True

        return False

    def update_phone(self, name: str, phone: str, update: bool = True) -> bool:
        """Update a customer's phone number
        :param name: The customer name
        :param phone: The customer phone number
        :param update: Whether to update the file
        :return: True if the customer was updated, False otherwise
        """

        # Check if the customer exists
        if self.has_customer(name):

            # Update the customer
            self.database[name][2] = phone
            if update:
                # Update the file
                self.update_file()
            return True

        return False

    def report(self) -> str:
        """Generate a report of the database
        :return: The report
        """

        # Generate the report
        report = ""
        keys = sorted(self.database.keys())

        for key in keys:
            report += Database.format_customer(key, self.database[key]) + "\n"

        return report

    def update_file(self) -> None:
        """Update the database file"""

        # Update the file
        with open(self.fName, "w") as f:
            f.write(self.report())