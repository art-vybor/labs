#include <stdio.h>
#include <string.h>
#include <openssl/des.h>
#include <stdlib.h>

const char *k1="01010101C4646EA0";
const char *k2="010101015A72C81A";
const char *s_text="6368616D50696F6E";
const char *s_ctext="C17DD7C47474E4E6";

typedef C_Block * DES_TXT;

void print_hex(unsigned char * data, int len) {
    for (int i = 0; i < len; i++) {
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

int main() {
    unsigned char text[8], ctext[8], temp[8], temp1[8];
    from_hex_to_bin(s_text, text);
    from_hex_to_bin(s_ctext, ctext);
    
    DES_cblock key; DES_key_schedule keysched;
    from_hex_to_bin(k2, key);

    DES_set_key((DES_TXT)key, &keysched); 
    DES_ecb_encrypt((DES_TXT)text, (DES_TXT)temp, &keysched, DES_ENCRYPT);

    from_hex_to_bin(k1, key);

    DES_set_key((DES_TXT)key, &keysched); 
    DES_ecb_encrypt((DES_TXT)temp, (DES_TXT)temp1, &keysched, DES_ENCRYPT);

    printf("chiphertext: "); print_hex(ctext, 8);
    printf("to check: "); print_hex(temp1, 8);

    return 0;
}