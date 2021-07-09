from . import _core

class AFUnixClient():
    def __init__(self, path_to_socket_file):
        self.socket_path = path_to_socket_file
        self.connected, self.sock = _core.socket_connect(self.socket_path)

    def read(self, num_bytes):
        return _core.socket_read(self.sock, num_bytes)

    def write(self, data):
        return _core.socket_write(self.sock, data)

    def close(self):
        return _core.socket_close(self.sock)

    def __del__(self):
        if self.connected:
            self.close()
            self.connected = False
