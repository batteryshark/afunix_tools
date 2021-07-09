#undef UNICODE

#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#include <afunix.h>
#include <stdlib.h>
#include <stdio.h>
#pragma comment(lib, "Ws2_32.lib")

#define SERVER_SOCKET "/vx/tmp/12345678/VXLOG.sock"

int __cdecl main(void)
{
    SOCKET ClientSocket = INVALID_SOCKET;
    SOCKET ListenSocket = INVALID_SOCKET;
    int Result = 0;
    char SendBuffer[] = "af_unix from Windows to WSL!";
    char RecvBuffer[4096] = { 0x00 };
    int SendResult = 0;
    int RecvResult = 0;
    SOCKADDR_UN ServerSocket = { 0 };
    WSADATA WsaData = { 0 };

    // Initialize Winsock
    Result = WSAStartup(MAKEWORD(2, 2), &WsaData);
    if (Result != 0) {
        printf("WSAStartup failed with error: %d\n", Result);
        goto Exit;
    }

    // Create a AF_UNIX stream server socket.
    ListenSocket = socket(AF_UNIX, SOCK_STREAM, 0);
    if (ListenSocket == INVALID_SOCKET) {
        printf("socket failed with error: %d\n", WSAGetLastError());
        goto Exit;
    }

    ServerSocket.sun_family = AF_UNIX;
    strncpy_s(ServerSocket.sun_path, sizeof ServerSocket.sun_path, SERVER_SOCKET, (sizeof SERVER_SOCKET) - 1);

    // Bind the socket to the path.
    Result = bind(ListenSocket, (struct sockaddr*)&ServerSocket, sizeof(ServerSocket));
    if (Result == SOCKET_ERROR) {
        printf("bind failed with error: %d\n", WSAGetLastError());
        goto Exit;
    }

    // Listen to start accepting connections.
    Result = listen(ListenSocket, SOMAXCONN);
    if (Result == SOCKET_ERROR) {
        printf("listen failed with error: %d\n", WSAGetLastError());
        goto Exit;
    }

    printf("Accepting connections on: '%s'\n", SERVER_SOCKET);
    // Accept a connection.
    ClientSocket = accept(ListenSocket, NULL, NULL);
    if (ClientSocket == INVALID_SOCKET) {
        printf("accept failed with error: %d\n", WSAGetLastError());
        goto Exit;
    }
    printf("Accepted a connection.\n");

    // Send some data.
    /*
    SendResult = send(ClientSocket, SendBuffer, (int)strlen(SendBuffer), 0);
    if (SendResult == SOCKET_ERROR) {
        printf("send failed with error: %d\n", WSAGetLastError());
        goto Exit;
    }
    printf("Relayed %zu bytes: '%s'\n", strlen(SendBuffer), SendBuffer);
    */

    RecvResult = recv(ClientSocket, RecvBuffer, (int)sizeof(RecvBuffer), 0);
    if (RecvResult == SOCKET_ERROR) {
        printf("recv failed with error: %d\n", WSAGetLastError());
        goto Exit;
    }
    printf("Relayed %zu bytes: '%s'\n", strlen(RecvBuffer), RecvBuffer);

    // shutdown the connection.
    printf("Shutting down\n");
    Result = shutdown(ClientSocket, 0);
    if (Result == SOCKET_ERROR) {
        printf("shutdown failed with error: %d\n", WSAGetLastError());
        goto Exit;
    }
    VK_F1
        VK_F2
Exit:

    // cleanup
    if (ListenSocket != INVALID_SOCKET) {
        closesocket(ListenSocket);
    }

    if (ClientSocket != INVALID_SOCKET) {
        closesocket(ClientSocket);
    }

    // Analogous to `unlink`
    DeleteFileA(SERVER_SOCKET);
    WSACleanup();
    return 0;
}