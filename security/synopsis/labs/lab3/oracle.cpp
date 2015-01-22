// link with libcrypto.so, i.e. add -lcrypto

#include <openssl/aes.h>
#include <iostream>
#include <string>
#include <iomanip>
#include <vector>
#include <sstream>
#include <assert.h>

typedef unsigned char uchar;

std::string string_to_hex(const unsigned char *buf, size_t len)
{
    static const char* const lut = "0123456789abcdef";

    std::string output;
    output.reserve(2 * len);
    size_t j = 0;
    for (size_t i = 0; i < len; ++i)
    {
        const unsigned char c = buf[i];
        output.push_back(lut[c >> 4]);
        output.push_back(lut[c & 15]);
    }
    return output;
}

std::string hex_to_string(const std::string& input)
{
    size_t len = input.length();
    assert(len % 2 == 0);

    std::string output;
    output.reserve(len/2);
    for (size_t i = 0; i < len; i+=2)
    {
        std::string s = input.substr(i, 2);
        std::stringstream str(s);
        unsigned int v;
        str >> std::hex >> v;
        output.push_back((uchar)v);
    }
    return output;
}

void mxor(uchar* out, const uchar* a, const uchar* b, const size_t len)
{
  for( int i = 0; i < len; ++i)
    out[i] = a[i] ^ b[i];
}

void decryptBlock(uchar* out, const uchar* iv, const unsigned char *in, const AES_KEY *aesKey)
{
  AES_ecb_encrypt(in, out, aesKey, AES_DECRYPT);
  mxor(out, iv, out, 16);
}

void decryptSome(uchar *out, const uchar *iv, const uchar *in, int nBlocks, const AES_KEY *aesKey)
{
  decryptBlock(out, iv, in, aesKey);
  for(int i = 1; i < nBlocks; ++i)
    decryptBlock(out + 16*i, in + 16*(i-1), in + 16*i, aesKey);
}

bool checkPad(const uchar *in, size_t bufSize)
{
  size_t pad = in[bufSize - 1];
  if(pad > bufSize)
    return false;
  if(pad == 0)
  {
    if(16 > bufSize)
      return false;
    for(int i = bufSize - 16; i < bufSize; ++i)
      if(in[i] != pad)
        return false;
    return true;
  }
  for(int i = bufSize - pad; i < bufSize; ++i)
    if(in[i] != pad)
      return false;
  return true;
}

bool checkPlainTextPad(const uchar *iv, const uchar *in, size_t len, const AES_KEY *aesKey)
{
  uchar *out = new uchar[len];
  decryptSome(out, iv, in, len / 16, aesKey);
  bool res = checkPad(out, len);
  delete[] out;
  return res;
}

main(int argc, char **argv)
{
  std::string input;
  std::cin >> input;
  std::string cts = hex_to_string(input);

  uchar *iv = (uchar*)cts.data();
  uchar *ct = (uchar*)cts.data() + 16;
  size_t ctlen = cts.length();
  if(ctlen % 16 != 0 || ctlen < 32)
  {
    std::cerr << "input length must be 16*n bytes, and at least 32 bytes" << std::endl;
    return 1;
  }

  uchar key[] = "my key          ";
  AES_KEY decKey;
  AES_set_decrypt_key(key, 128, &decKey);
  bool goodPad = checkPlainTextPad(iv, ct, ctlen-16, &decKey);
  std::cout << (goodPad ? "true" : "false") << std::endl;
 
  return 0;
} 
