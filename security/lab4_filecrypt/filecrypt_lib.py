import sys
import os.path
from Crypto.Hash import HMAC
from Crypto.Util import Counter

def check_file_exists(files):
    files_not_found = []
    for file_path in files:
        if not os.path.exists(file_path):
            files_not_found.append(file_path)

    if files_not_found:
        sys_exit(6, 'Files not found: {FILES}'.format(FILES=', '.join(files_not_found)))

def sys_exit(code, message):
    sys.stderr.write(message + '\n')
    sys.exit(code)

def get_hmac(key, data):
    return HMAC.new(key, data).hexdigest()

def get_ctr(nonce):
    return Counter.new(128, initial_value=long(nonce, 16))