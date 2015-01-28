
#include <cstring>
#include <openssl/aes.h>
#include <string>

typedef unsigned char uchar;
bool checkPlainTextPad(const uchar *iv, const uchar *in, size_t len, const AES_KEY *aesKey);
std::string string_to_hex(const unsigned char *buf, size_t len);
std::string hex_to_string(const std::string& input);
void decryptSome(uchar *out, const uchar *iv, const uchar *in, int nBlocks, const AES_KEY *aesKey);
