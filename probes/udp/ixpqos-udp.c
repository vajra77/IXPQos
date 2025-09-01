#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define MAXLINE 2048

void rnd_fill_buffer(char *buffer, int count) {

}

int udp_ping(char *dst_addr, int count, float delay) {

    int sockfd;
    char buffer[MAXLINE];
    struct sockaddr_in tgt_addr;

    int i;
    for(i = 0; i<= count; i++) {

        int dst_port = 7000 + 7*i;
        rnd_fill_buffer(buffer, MAXLINE);

        if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
            perror("socket creation failed");
            return -1;
        }

        memset(&tgt_addr, 0, sizeof(tgt_addr));

        // Filling server information
        tgt_addr.sin_family = AF_INET;
        tgt_addr.sin_port = htons(dst_port);
        inet_pton(AF_INET, dst_addr, &(tgt_addr.sin_addr));

        int n;
        unsigned int len;

        sendto(sockfd, (const char *)buffer, MAXLINE,
            0, (const struct sockaddr *) &tgt_addr,
                sizeof(tgt_addr));

        n = recvfrom(sockfd, (char *)buffer, MAXLINE,
                    MSG_WAITALL, (struct sockaddr *) &tgt_addr,
                    &len);
        buffer[n] = '\0';

        close(sockfd);
    }
    return 0;
}

