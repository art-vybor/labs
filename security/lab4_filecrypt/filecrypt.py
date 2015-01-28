import argparse

from user_manager import user_manager
from encrypt_manager import encrypt_manager
from filecrypt_lib import sys_exit, check_file_exists


def parse_args():
    parser = argparse.ArgumentParser(description='Filecrypt command line interface.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e',    help='encrypt files', action="store_true", default=False, dest='encrypt_files')
    group.add_argument('-d',    help='decrypt files', action="store_true", default=False, dest='decrypt_files')
    group.add_argument('-a',    help='add user',      action="store_true", default=False, dest='add_user')
    group.add_argument('-r',    help='remove user',   action="store_true", default=False, dest='remove_user')

    parser.add_argument('-u',   help='username',      metavar='username', dest='username', required=True)
    parser.add_argument('-p',   help='password with more than 8 chars, at least 1 char of each type: [A-Z], [a-z], [0-9]', metavar='password', dest='password', required=True)
    parser.add_argument('files', help='files for encrypt or decrypt', nargs='*', metavar='file')
    return parser.parse_args()

def main():
    args = parse_args()
    username = args.username
    password = args.password
    files = args.files

    if args.encrypt_files:
        um = user_manager()
        um.authorize(username, password)
        check_file_exists(files)

        em = encrypt_manager()
        em.encrypt(um.zip_files_with_keys(files))
        em.save()

        um.save()
        print 'Encrypted files: {FILES}'.format(FILES=', '.join(files))
    elif args.decrypt_files:
        um = user_manager()
        um.authorize(username, password)
        check_file_exists(files)
        files_with_keys = um.zip_files_with_keys(files)

        em = encrypt_manager()
        em.check_tampering(files_with_keys)
        em.decrypt(files_with_keys)
        em.save()

        um.save()
        print 'Decrypted files: {FILES}'.format(FILES=', '.join(files))

    elif args.add_user:
        um = user_manager()

        um.create(username, password)
        um.save()
        print 'Added user {USERNAME}'.format(USERNAME=username)        
        
    elif args.remove_user:
        um = user_manager()
        um.authorize(username, password)

        um.remove()
        um.save()
        print 'Removed user {USERNAME}'.format(USERNAME=username)

if __name__ == "__main__":
    main()