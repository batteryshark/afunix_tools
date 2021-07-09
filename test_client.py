import AFUnix.Client
import binascii

SOCKET_ADDRESS = "./myserver.sock"
TEST_DATA = b"1234123412341234234523452345234512341234123412342345234523452345"

client = AFUnix.Client.AFUnixClient(SOCKET_ADDRESS)
if not client.connected:
    print("Client Connect Error!")
else:
    res = client.write(TEST_DATA)
    if not res:
        print("Client Write Fail!")
    else:
        print(f"Client Wrote {len(TEST_DATA)} Bytes")
    num_bytes = 32
    res, data = client.read(num_bytes)
    if not res:
        print("Client Read Fail!")
    else:
        print(f"Client Read {len(data)} Bytes")
        print(binascii.hexlify(data))

    client.close()
