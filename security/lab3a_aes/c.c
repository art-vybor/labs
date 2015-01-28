#include <stdio.h>
#include <unordered_map>
#include <string.h>
#include "oracle.h"
#include <openssl/aes.h>
#include <stdlib.h>

using namespace std;

const char *s_ctext="00010203040506070001020304050607f1ecbc68bd8afb7c93e63fa73112d51a2068ca3b362effd71ec9b24f2a398203";
AES_KEY key;

void print_hex(unsigned char * data, int len) {
    for (int i = 0; i < len; ++i) {
        printf("%02X", data[i]);
    }
    printf("\n");
}

void from_hex_to_bin(const char *src, unsigned char *dst) {
    for (int i =0; i < strlen(src); i+=2) {
        char s[2]; s[0]=src[i]; s[1]=src[i+1];
        dst[i/2]=strtol(s, NULL, 16);
    }
}

unsigned char* find_plaintext(unsigned char* C_1, unsigned char* C_2) {
    unsigned char *P = (unsigned char *) malloc(16);
    unsigned char I[16], _C[32];

    strncpy((char *)(_C+16), (char *)C_2, 16);

    //loop bytes
    for (int i = 15; i>=0; --i) {
        //fill _C[k] for correc _P pad value. k from i+1 to 15. correct _p pad = 16-i;
        unsigned char _P_pad = 16-i;
        for (int k = i+1; k<16; k++) _C[k] = _P_pad ^ I[k];
        
        //loop by _c[i] value
        for (int j = 0; j <= 255; ++j) {
            _C[i] = j;
            //send to oracle
            if (checkPlainTextPad(_C, _C+16, 16, &key)) {
                //find P[i] and break;
                I[i] = j ^ _P_pad;
                P[i] = C_1[i] ^ I[i];
                break;
            }
        }
    }
    return P;
}

int main() {
    unsigned char ctext[48];
    from_hex_to_bin(s_ctext, ctext);
    print_hex(ctext,48);
    unsigned char c[3][16];

    for (int i = 0; i < 48; ++i) c[i/16][i%16] = ctext[i];

    printf("IV: "); print_hex(c[0],16);
    printf("C1: "); print_hex(c[1],16);
    printf("C2: "); print_hex(c[2],16);

    //prepare key
    AES_set_decrypt_key((const unsigned char *)"my key          ", 128, &key);

    //for each chiphertext block i
    for (int i = 1; i < 3; ++i) {
        unsigned char *p;
        p = find_plaintext(c[i-1], c[i]);
        print_hex(p, 16);
    }

    return 0;
}
