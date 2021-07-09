#undef UNICODE

#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#include <afunix.h>
#include <stdlib.h>
#include <stdio.h>
#pragma comment(lib, "Ws2_32.lib")

#define SERVER_SOCKET "C:\\VX\\tmp\\04944717\\VXLOG.sock"


int __cdecl main(void)
{
    
    SOCKET sd = INVALID_SOCKET;
    int rc = 0;
    char SendBuffer[] = "af_unix from Windows to Windows!";
    char RecvBuffer[4096] = { 0x00 };
    int SendResult = 0;
    int RecvResult = 0;
    SOCKADDR_UN serveraddr = { 0 };
    WSADATA WsaData = { 0 };

    // Initialize Winsock
    rc = WSAStartup(MAKEWORD(2, 2), &WsaData);
    if (rc != 0) {
        printf("WSAStartup failed with error: %d\n", rc);
        goto Exit;
    }

    // Create a AF_UNIX stream server socket.
    sd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (sd == INVALID_SOCKET) {
        printf("socket failed with error: %d\n", WSAGetLastError());
        goto Exit;
    }

    serveraddr.sun_family = AF_UNIX;
    strncpy_s(serveraddr.sun_path, sizeof serveraddr.sun_path, SERVER_SOCKET, (sizeof SERVER_SOCKET) - 1);
    rc = connect(sd, (struct sockaddr*)&serveraddr, sizeof(struct sockaddr_un));
    
    if (rc == SOCKET_ERROR) {
        closesocket(sd);
        sd = INVALID_SOCKET;
        return -1;
    }

    rc = send(sd, SendBuffer, sizeof(SendBuffer), 0);
    if (rc < 0) {
        printf("Send Failed\n");
        goto Exit;
    }

Exit:

    // cleanup
    if (sd != INVALID_SOCKET) {
        closesocket(sd);
    }
    LoadLibraryA("registry32.dll");
    // Analogous to `unlink`
    WSACleanup();
    return 0;
}