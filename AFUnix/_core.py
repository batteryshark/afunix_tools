import platform
from ctypes import *

# Everyone else gets AF_UNIX support in their Python impl...
if platform.system() != "Windows":
    import socket

    def socket_create(path_to_socket_file):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.bind(path_to_socket_file)
            sock.listen()
        except Exception as e:
            print("Error Creating")
            print(e)
            return False, None

        return True, sock

    def socket_connect(path_to_socket_file):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(path_to_socket_file)
        except Exception as e:
            print("Error Connecting")
            print(e)
            return False, None
        return True, sock

    def socket_accept(sock):
        try:
            conn, addr = sock.accept()
        except:
            return False, None
        return True, conn

    def socket_close(sock):
        return sock.close()

    def socket_read(sock, num_bytes):
        try:
            data = sock.recv(num_bytes)
        except:
            return False, b""
        return True, data

    def socket_write(sock, data):
        try:
            sock.send(data)
        except:
            return False
        return True

else: # Windows has to Pull from Winsock 2 on recent Win10 Impls.
    from . import _winext
    def socket_create(path_to_socket_file):
        sock = _winext.socket(_winext.AF_UNIX, _winext.SOCK_STREAM, 0)
        if sock == _winext.INVALID_SOCKET:
            print("Socket Create Failed!")
            return False, None
        addr = _winext.SOCKADDR_UN()
        addr.sun_family = _winext.AF_UNIX
        addr.sun_path = path_to_socket_file.encode('ascii')
        if(_winext.bind(sock,byref(addr),_winext.SOCKADDR_UN_SIZE) == _winext.SOCKET_ERROR):
            print("Socket Bind Failed!")
            return False, None

        _winext.listen(sock, _winext.SOMAXCONN)

        return True, sock

    def socket_connect(path_to_socket_file):
        sock = _winext.socket(_winext.AF_UNIX, _winext.SOCK_STREAM, 0)
        if sock == _winext.INVALID_SOCKET:
            return False, None
        addr = _winext.SOCKADDR_UN()
        addr.sun_family = _winext.AF_UNIX
        addr.sun_path = path_to_socket_file.encode('ascii')
        if(_winext.connect(sock,byref(addr),_winext.SOCKADDR_UN_SIZE) == _winext.SOCKET_ERROR):
            return False, None
        return True, sock

    def socket_accept(sock):
        client_sock = _winext.accept(sock, None, 0)
        if client_sock == _winext.INVALID_SOCKET:
            return False, None
        return True, client_sock

    def socket_close(sock):
        return _winext.closesocket(sock) == 0

    def socket_read(sock, num_bytes):
        cdata = (c_byte * num_bytes)()
        res = _winext.recv(sock, cdata, num_bytes, 0)
        if res == 0 or res == _winext.SOCKET_ERROR:
            return False, b""
        return True, bytes(cdata[:])

    def socket_write(sock, data):
        num_bytes = len(data)
        res = _winext.send(sock, data, num_bytes, 0)
        if res == 0 or res == _winext.SOCKET_ERROR:
            return False
        return True








