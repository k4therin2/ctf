/*
  This sends some random UDP traffic to mtb.wtf, then sends a CTF flag, then
  more random UDP traffic. Port 58008 btw. The flag is obfuscated so that you
  cannot run strings on it (we already have a strings flag).

  Compile for Linux and Windows (run on Linux machine):
  $ gcc -o DontRunMe DontRunMe.c
  $ i686-w64-mingw32-gcc -o DontRunMe.exe DontRunMe.c -lws2_32

  Compile for Mac (run on Mac-hine... heh.):
  $ clang -o DontRunMe DontRunMe.c

  The flag is FLAG{c_is_the_best_and_you_should_all_learn_it}
 */

#ifdef _WIN32
#include <winsock2.h>
#define NL "\r\n"
#else// hopefully it's linux
#include <netdb.h>
#include <sys/socket.h>
#define NL "\n"
#endif

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MSG_PROB 20

char flag[] = "\x34\x2d\x2f\x23\x14\x0e\x70\x02\x16\x26\x07\x43\x04\x2d\x07\x46\x1e\x1b\x2d\x04\x4b\x17\x3a\x1a\x1a\x07\x3a\x28\x0a\x1a\x01\x40\x0b\x37\x4f\x1b\x09\x33\x00\x17\x00\x1c\x0a\x30\x04\x5b\x16";
char *key = "random/keys+are#more%secure[but,oh.well";
char *target_hostname = "mtb.wtf";
unsigned short port = 58008;
unsigned char rndbuf[256];

/*
  XOR the bytes of buf with bytes of the key. Sort of an "encryption" technique
  but very silly. This is done in obf.c as well, but with a smaller key and
  more, well, obfuscated.
 */
void xor(char *buf, size_t bufsize, char *key, size_t keylen)
{
  for (size_t i = 0; i < bufsize; i++) {
    buf[i] ^= key[i % keylen];
  }
}

/*
  Print out a string as a hex escaped char array.
 */
void print_charray(char *buf, size_t bufsize)
{
  printf("\"");
  for (size_t i = 0; i < bufsize; i++) {
    printf("\\x%02x", buf[i]);
  }
  printf("\"" NL);
}

/*
  Fills rndbuf with random data.
 */
void randomize() {
  for (int i = 0; i < sizeof(rndbuf); i++) {
    rndbuf[i] = rand();
  }
}

/*
  Sends UDP packets of random data. Each time, it has a 1/MSG_PROB chance of
  terminating.
 */
void sendmanyrandom(int sock, struct sockaddr *in, size_t len) {
  while (rand() % MSG_PROB != 0) {
    randomize();
    int res = sendto(sock, rndbuf, strlen(flag) + 1, 0, in, len);
    if (-1 == res) {
      #ifdef _WIN32
      fprintf(stderr, "windows sux(sendto) %d" NL, WSAGetLastError());
      #else
      perror("sendto");
      #endif
      exit(-1);
    }
  }
}

int main(int argc, char **argv) {
  // Utility for getting encrypted data. Would be funny if somebody discovered
  // this code.
  if (argc == 2) {
    size_t len = strlen(argv[1]);
    char *data = malloc(len);
    memcpy(data, argv[1], len);
    xor(data, len, key, strlen(key));
    print_charray(data, len);
    free(data);
  }

#ifdef _WIN32
  // Windows requires you to initialize their socket library. Rather annoying.
  WSADATA wsadata;
  int err = WSAStartup(MAKEWORD(1, 0), &wsadata);
  if (err != 0) {
    printf("WSAStartup failed with error: %d" NL, err);
    return 1;
  }
#endif
  srand(time(NULL));

  // DNS lookup for mtb.wtf
  struct hostent *hostent = gethostbyname(target_hostname);
  if (hostent == NULL) {
#ifdef _WIN32
    fprintf(stderr, "windows sux(gethostbyname) %d" NL, WSAGetLastError());
#else
    herror("gethostbyname");
#endif
    return -1;
  }

  // Create UDP sending socket
  int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
  if (sock == -1) {
#ifdef _WIN32
    fprintf(stderr, "windows sux(socket) %d" NL, WSAGetLastError());
#else
    perror("socket");
#endif
    return sock;
  }

  // Construct a socket address (host/port) for UDP mtb.wtf:58008
  struct sockaddr_in in;
  in.sin_family = AF_INET;
  in.sin_port = htons(port);
  memcpy(&in.sin_addr, hostent->h_addr_list[0], hostent->h_length); // finger cross


  // Send random data.
  sendmanyrandom(sock, (struct sockaddr*)&in, sizeof(in));
  // Then send the actual flag.
  xor(flag, sizeof(flag) - 1, key, strlen(key));
  int res = sendto(sock, flag, strlen(flag) + 1, 0, (struct sockaddr*)&in,
                   sizeof(in));
  // Error check.
  if (-1 == res) {
#ifdef _WIN32
    fprintf(stderr, "windows sux(sendto) %d" NL, WSAGetLastError());
#else
    perror("sendto");
#endif
    return -1;
  }
  // Send more random data.
  sendmanyrandom(sock, (struct sockaddr*)&in, sizeof(in));

  // Finally, print out a silly cryptic message and wait for enter keypress.
  printf("If a flag goes through a wire, does it make any noise?" NL);
  printf("<enter to quit, you may want to run me again>" NL);
  fgetc(stdin);
}
