from django.utils.crypto import get_random_string
import os


def generate_secret_key(length=50):
    """
    Return a 50 character random string
    usable as a `SECRET_KEY` setting value.
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    if not isinstance(length, int):
        raise TypeError(
            f'invalid literal for int() with base 10: {length}')
    return get_random_string(length, chars)


def main():
    if not os.path.isdir('config'):
        os.makedirs('config')
        print("Creating config folder")
    if not os.path.exists('config/secret_key.txt'):
        secret_key = get_random_string(50)
        with open('config/secret_key.txt', 'wtexit') as secret_key_file:
            secret_key_file.write(secret_key)
            secret_key_file.close()
            print("Secret key file created")
    else:
        print("Secret key file already exists")


if __name__ == '__main__':
    main()
