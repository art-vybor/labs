#include <stdio.h>
#include <unordered_map>
#include <string.h>
#include <openssl/des.h>
#include <stdlib.h>

using namespace std;

typedef C_Block * DES_TXT;

const char *s_text="6368616D50696F6E";
const char *s_ctext="C17DD7C47474E4E6";

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

long chipher_to_long(unsigned char* chipher) {
    long i1 = (chipher[0] & 0xFF) | ((chipher[1] & 0xFF) << 8) | ((chipher[2] & 0xFF) << 16) | ((chipher[3] & 0xFF) << 24);
    long i2 = (chipher[4] & 0xFF) | ((chipher[5] & 0xFF) << 8) | ((chipher[6] & 0xFF) << 16) | ((chipher[7] & 0xFF) << 24);
    i1 = i1 & 0xFFFFFFFF; i2 = i2 & 0xFFFFFFFF;
    return i1 | (i2 << 32);
}

void update_key(DES_cblock key, int k) {
    key[4] = (k & 0b01111111) << 1; key[5] = ((k >> 7) & 0b01111111) << 1;
    key[6] = ((k >> 14) & 0b01111111) << 1; key[7] = ((k >> 21) & 0b01111111) << 1;
}

int main() {
    unsigned char text[8], ctext[8];
    from_hex_to_bin(s_text,text);
    from_hex_to_bin(s_ctext,ctext);

    unordered_map<long, int> key_chipher_map;

    DES_cblock key; DES_key_schedule keysched;

    key[0] = 0x01; key[1] = 0x01; key[2] = 0x01; key[3] = 0x01;
    key[4] = 0x01; key[5] = 0x01; key[6] = 0x01; key[7] = 0x01;
    
    //loop by all possible keys: encrypt text with it and put to key_chipher_map
    int top_k = 0b00001111111111111111111111111111;
    unsigned char temp[8];
    for (int k=0; k <= top_k; ++k) {
        if (k%5000000==0) printf("encrypt stage %.2f%%\n", k*1.0/top_k*100);
        //update key
        update_key(key, k);

        //encrypt
        DES_set_key((DES_TXT)key, &keysched); 
        DES_ecb_encrypt((DES_TXT)text, (DES_TXT)temp, &keysched, DES_ENCRYPT);

        //put to map
        long chipher_long = chipher_to_long(temp);
        key_chipher_map.insert(make_pair(chipher_long, k));
    }
    
    //loop by all possible keys: decrypt ctext with it and try to find key in key_chipher_map
    unordered_map<long,int>::iterator it;
    for (int k=0; k <= top_k; ++k) {
        if (k%1000000==0) printf("decrypt stage  %.2f%%\n", k*1.0/top_k*100);
        //update key
        update_key(key, k);

        //decrypt
        DES_set_key((DES_TXT)key, &keysched); 
        DES_ecb_encrypt((DES_TXT)ctext, (DES_TXT)temp, &keysched, DES_DECRYPT);
        
        //try to find in map
        long chipher_long = chipher_to_long(temp);

        it = key_chipher_map.find(chipher_long);
        if (it != key_chipher_map.end()) {
            printf("key found:\n");
            print_hex(key, 8);
            update_key(key, it->second);
            print_hex(key, 8);
        }
    }   

    return 0;
}