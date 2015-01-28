import marshal
import os
import binascii
from Crypto.Cipher import AES

from filecrypt_lib import sys_exit, get_ctr, get_hmac

class encrypt_manager:
    encrypt_data_file = 'filecrypt_encrypt_data'
    nonce_size = 16

    def __init__(self):
        self.files = marshal.load(open(self.encrypt_data_file, 'rb')) if os.path.exists(self.encrypt_data_file) else {}

    def save(self):
        marshal.dump(self.files, open(self.encrypt_data_file, 'wb'))

    def encrypt(self, files_with_keys):
        for file_path, key in files_with_keys:
            data = open(file_path, 'rb').read()
            nonce = binascii.b2a_hex(os.urandom(self.nonce_size))

            cipher = AES.new(key, AES.MODE_CTR, counter=get_ctr(nonce)).encrypt(data)

            self.files[get_hmac(key, cipher)] = {'nonce': nonce}
            open(file_path, 'wb').write(cipher)

    def decrypt(self, files_with_keys):
        for file_path, key in files_with_keys:
            cipher = open(file_path, 'rb').read()
            hmac = get_hmac(key, cipher)
            nonce = self.files[hmac]['nonce']

            data = AES.new(key, AES.MODE_CTR, counter=get_ctr(nonce)).decrypt(cipher)           

            del self.files[hmac]
            open(file_path, 'wb').write(data)

    def check_tampering(self, files_with_keys):
        tampering_files = []

        for file_path, key in files_with_keys:
            data = open(file_path, 'rb').read()

            if get_hmac(key, data) not in self.files:
                tampering_files.append(file_path)

        if tampering_files:
            sys_exit(7, 'Tampering detected: {FILES}'.format(FILES=', '.join(tampering_files)))

