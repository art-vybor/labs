#include <stdio.h>
#include <string.h>
#include <openssl/rc4.h>
#include <stdlib.h>

char *s_key="6F626579616E6430303030";
char *s_text="636F6F7065726174656F72646965616761696E";
char encrypted[16];

void print_hex(char* data, int len) {
    for (int i = 0; i < len; i++) {
        printf("%02X", (unsigned char)data[i]);
    }
    printf("\n");
}

void to_hex(char *src, char *dst) {
    for (int i =0; i < strlen(src); i+=2) {
        char s[2]; s[0]=src[i]; s[1]=src[i+1];
        dst[i/2]=strtol(s, NULL, 16);
    }
}

int main() {
    char key[16], text[16];
    to_hex(s_key,key);
    to_hex(s_text,text);

    for (int i=strlen(key); i<16;++i)
        key[i]=0;

    int len = strlen(s_text)/2;
    print_hex(key,16);
    print_hex(text,len);

    RC4_KEY rc4_key;
    RC4_set_key(&rc4_key, 16, key);
    RC4(&rc4_key, len, text, encrypted);
    print_hex(encrypted, len);

    RC4_set_key(&rc4_key, 16, key);
    RC4(&rc4_key, len, encrypted, text);
    print_hex(text, len);

    return 0;
}