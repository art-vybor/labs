import marshal
import os
import binascii
from Crypto import Random
from Crypto.Hash import HMAC

from filecrypt_lib import sys_exit

class user_manager:
    users_data_file = 'filecrypt_users_data'
    sault_size = 16

    def __init__(self):
        self.users = marshal.load(open(self.users_data_file, 'rb')) if os.path.exists(self.users_data_file) else {}

    def save(self):
        marshal.dump(self.users, open(self.users_data_file, 'wb'))

    def is_password_valide(self, password):
        upper = False
        lower = False        
        digit = False
        len_ge_8 = False

        if len(password) >= 8: len_ge_8 = True

        for letter in password:
            if letter.isupper(): upper = True
            if letter.islower(): lower = True
            if letter.isdigit(): digit = True

        return upper and lower and digit and len_ge_8

    def authorize(self, username, password):
        if not self.exists(username):
            sys_exit(2, 'Bad credentials')

        if self.users[username]['password_hash'] != self.get_password_hash(username, password):
            sys_exit(2, 'Bad credentials')

        self.username = username
        self.password = password
            

    def create(self, username, password):
        if self.exists(username): 
            sys_exit(4, 'User already exists')

        if not self.is_password_valide(password):
            sys_exit(5, 'Too short or weak password')

        self.users[username] = {}

        self.users[username]['sault'] = binascii.b2a_hex(os.urandom(self.sault_size))
        self.users[username]['password_hash'] = self.get_password_hash(username, password)

    def remove(self):
        del self.users[self.username]

    def exists(self, username):
        return username in self.users

    def get_password_hash(self, username, password):
        return HMAC.new(self.users[username]['sault'], password).hexdigest()

    def get_key(self, file_path):
        return HMAC.new(self.users[self.username]['sault'], self.username + self.password).hexdigest()

    def zip_files_with_keys(self, files):
        return zip(files, map(self.get_key, files))

