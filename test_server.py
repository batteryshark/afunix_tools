import AFUnix.Server
import binascii

SOCKET_ADDRESS = "./myserver.sock"
server = AFUnix.Server.AFUnixServer(SOCKET_ADDRESS)
if not server.listening:
    print("Server Create Fail")
else:
    while 1:
        print("Waiting for Client...")
        res, conn = server.accept()
        if not res:
            print("Server Accept Error")
            break
        print("Server Received Connection")
        print(conn)
        res, data = server.read(conn, 32)
        if not res:
            print("Server Read Fail!")
            break
        print(f"Server Read {len(data)} Bytes: ")
        print(binascii.hexlify(data))

        print("Echoing Back to Client...")
        res = server.write(conn, data)
        if not res:
            print("Server Write Fail!")
            break
        print(f"{len(data)} Bytes Written to Client!")
        server.close(conn)

