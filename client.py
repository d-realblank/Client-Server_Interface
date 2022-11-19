"""
David Onwionoko
40167358
Assignment 2
"""

if __name__ == "__main__":
    from Client.database_client import Client

    # Set client address
    HOST: str = "localhost"
    PORT: int = 9999
    client: Client = Client(HOST, PORT)

    print("Welcome to the Client interface\n")

    #Loop until user quits
    while client.active:
        client.query()