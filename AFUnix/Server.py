from . import _core
import os

class AFUnixServer():
    def __init__(self, path_to_socket_file):
        self.socket_path = path_to_socket_file
        self.listening, self.sock = _core.socket_create(self.socket_path)

    def __del__(self):
        if self.sock:
            self.close()
        self.listening = False
        if not self.listening:
            if os.path.exists(self.socket_path):
                os.unlink(self.socket_path)

    def accept(self):
        return _core.socket_accept(self.sock)

    def close(self, target_sock=None):
        if not target_sock:
            target_sock = self.sock
        return _core.socket_close(target_sock)

    def read(self, target_sock, num_bytes):
        return _core.socket_read(target_sock, num_bytes)

    def write(self, target_sock, data):
        return _core.socket_write(target_sock, data)