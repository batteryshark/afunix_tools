# Bullshit Winsock2 Bindings for AF_UNIX because Corona
from ctypes import *
from ctypes.wintypes import  *

import atexit

# Constants
AF_UNIX = 1
SOCK_STREAM = 1
INVALID_SOCKET = ~0
SOMAXCONN = 0x7FFFFFFF
SOCKET_ERROR = -1
WSADESCRIPTION_LEN = 256
WSASYS_STATUS_LEN = 128
UNIX_PATH_MAX = 108
SOCKET = c_uint


# Structures
class SOCKADDR_UN(Structure):
    _fields_ = [("sun_family", c_ushort),
                ("sun_path", c_char * UNIX_PATH_MAX)]

SOCKADDR_UN_SIZE = sizeof(SOCKADDR_UN)

class WSADATA(Structure):
    _fields_ = [
        ("wVersion",        WORD),
        ("wHighVersion",    WORD),
        ("szDescription",   c_char * (WSADESCRIPTION_LEN+1)),
        ("szSystemStatus",  c_char * (WSASYS_STATUS_LEN+1)),
        ("iMaxSockets",     c_ushort),
        ("iMaxUdpDg",       c_ushort),
        ("lpVendorInfo",    c_char_p),
    ]

# Functions
def MAKEWORD(bLow, bHigh):
    return (bHigh << 8) + bLow

WSACleanup = windll.Ws2_32.WSACleanup
WSACleanup.argtypes = []
WSACleanup.restype = c_int

WSAStartup = windll.Ws2_32.WSAStartup
WSAStartup.argtypes = (WORD, POINTER(WSADATA))
WSAStartup.restype = c_int

accept = windll.Ws2_32.accept
accept.argtypes = [SOCKET, POINTER(SOCKADDR_UN), c_int]
accept.restype = SOCKET

bind = windll.Ws2_32.bind
bind.argtypes = (SOCKET, POINTER(SOCKADDR_UN), c_int)
bind.restype = c_int

listen = windll.Ws2_32.listen
listen.argtypes = (SOCKET, c_int)
listen.restype = BOOL

socket = windll.Ws2_32.socket
socket.argtypes = [c_int, c_int, c_int]
socket.restype = SOCKET
WSASocket = windll.Ws2_32.WSASocketA

send = windll.Ws2_32.send
send.argtypes = [SOCKET, c_void_p, c_int, c_int]
send.restype = c_int

recv = windll.Ws2_32.recv
recv.argtypes = [SOCKET, POINTER(c_byte), c_int, c_int]
recv.restype = c_int

closesocket = windll.Ws2_32.closesocket
closesocket.argtypes = [SOCKET]
closesocket.restype = c_int

connect = windll.Ws2_32.connect
connect.argtypes = [SOCKET, POINTER(SOCKADDR_UN), c_int]
connect.restype = c_int

# Startup Code
wsa_data = WSADATA()
WSAStartup(MAKEWORD(2,2),byref(wsa_data))

# Teardown Code
@atexit.register
def unload():
    WSACleanup()
