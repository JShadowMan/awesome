#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/types.h>


struct sockaddr_storage socket_get_addr(const char *name, int port) {
    union {
        struct sockaddr_storage ss;
        struct sockaddr_in s4;
        struct sockaddr_in6 s6;
    } sock_addr;
    memset(&sock_addr, 0, sizeof(sock_addr));

    struct hostent *he = gethostbyname(name);
    if (he == NULL) {
        fprintf(stderr, "cannot resolve %s", name);
        exit(-1);
    }

    if (he->h_addrtype == AF_INET) {
        sock_addr.s4.sin_family = AF_INET;
        memcpy(&sock_addr.s4.sin_addr, he->h_addr_list[0], (size_t)he->h_length);
    } else if (he->h_addrtype == AF_INET6){
        sock_addr.s6.sin6_family = AF_INET6;
        memcpy(&sock_addr.s6.sin6_addr, he->h_addr_list[0], (size_t)he->h_length);
    } else {
        fprintf(stderr, "undefined sock_addr type for %d", he->h_addrtype);
        exit(-1);
    }

    sock_addr.s4.sin_port = htons((unsigned short)port);
    return sock_addr.ss;
}
