

if __name__ == "__main__":
    
    import sys
    from Server.database_server import DatabaseServer, DatabaseHandler

    # Set the server address
    HOST: str = "localhost"
    PORT: int = 9999

    if len(sys.argv) > 1:
        FILE = int(sys.argv[1])
    else:
        FILE = "data.txt"

    with DatabaseServer(HOST, PORT, DatabaseHandler, FILE) as server:
        print("Server started")
        print("Database file: {}".format(FILE))
        print("Server address: {}:{}".format(HOST, PORT))
        print("Server PID: {}".format(server.getpid))
        server.serve_forever()