import sys
import argparse #  to parse command-line arguments
from cryptography.fernet import Fernet # to encrypt hexadecimal secret key
import time
import hmac # to calculate the HMAC-SHA1 hash required by the HOTP algorithm

FERNET_KEY=""

# Extracting a 31-bit value from the 20-byte HMAC-SHA1 digest
def dynamic_truncation(hmac_result):
    try:
        offset = hmac_result[19] & 0xf
        bytes_sequence = hmac_result[offset:offset+4]
        result = bytearray()
        result.append(bytes_sequence[0] & 0x7F)
        for bits in bytes_sequence[1:]:
            result.append(bits & 0xFF)
        return result
    except Exception as e:
        print(f'ft_otp: error: {e}')
        sys.exit(1)

# Generates a 6-digit HOTP value from a hex-encoded secret and a counter
def generate_hotp(secret, counter):
    try:
        key = bytes.fromhex(secret)
        counter_in_bytes = counter.to_bytes(8, byteorder='big')
        hmac_result = hmac.new(key, counter_in_bytes, "sha1").digest()
        last_31_bits = dynamic_truncation(hmac_result)
        value = int(last_31_bits.hex(), 16)
        otp = value % 10 ** 6
        return otp
    except Exception as e:
        print(f'ft_otp: error: {e}')
        sys.exit(1)

# Reads and decrypts the secret key stored in the given encrypted key file
def get_secret_key(infile):
    try:
        f = Fernet(FERNET_KEY)
        with open(infile, "rb") as file:
            encrypted_data = file.read().strip()
            decrypted_data = f.decrypt(encrypted_data).decode()
            return decrypted_data   
    except Exception as e:
        print(f'ft_otp: error: {e}')
        sys.exit(1)

# Generates a time-based OTP (TOTP) using the secret stored in infile
def generate_totp(infile):
    decoded_secret = get_secret_key(infile)
    return generate_hotp(decoded_secret, int(time.time()) // 30)

# Validates that the given string is a properly formatted hexadecimal key
def is_valid_content(content):
    try:
        if len(content) % 2 != 0 or len(content) < 64:
            raise ValueError
        int(content, 16)
        return True
    except ValueError:
        print('ft_otp: error: invalid key format.')
        return False

# Reads a plaintext hex key from infile, validates it, encrypts it with Fernet, and writes it to ft_otp.key
def generate_secret_key(infile):
    try:
        f = Fernet(FERNET_KEY)
        with open(infile, 'r') as file:
            content = file.read().strip()
            if not is_valid_content(content):
                return
            encrypted_data = f.encrypt(content.encode())
        with open("ft_otp.key", "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)
        print("The ft_otp.key file has been created.")
    except Exception as e:
        print(f'ft_otp: error: {e}')
        sys.exit(1)

# Defines and parses the command-line interface:
# -g to generate a key file, -k to generate an OTP from an existing key file
def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate a one-time password (OTP) using a HMAC key.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', type=str, help='the path to the file where is stored the key')
    group.add_argument('-k', type=str, help='the path to the ft_otp.key file')
    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.g:
        generate_secret_key(args.g)
    elif args.k:
        otp = generate_totp(args.k)
        print(f"{otp:06d}")

if __name__ == "__main__":
    main()