import sys
import argparse #  to parse command-line arguments
from cryptography.fernet import Fernet # to encrypt hexadecimal secret key
import time
import hmac # to calculate the HMAC-SHA1 hash required by the HOTP algorithm

FERNET_KEY=""

# Implements the dynamic truncation step defined in RFC 4226.
# The last 4 bits of the HMAC digest determines an offset from
# which 4 bytes are extracted to form a 31-bit positive integer.
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

# Reads the encrypted key file, decrypts it using Fernet,
# and returns the original hexadecimal secret key.
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

# Generates a TOTP code by computing the current time-step
# (30-second window) and passing it to the HOTP algorithm.
def generate_totp(infile):
    decoded_secret = get_secret_key(infile)
    return generate_hotp(decoded_secret, int(time.time()) // 30)

# Verifies that the provided secret is a valid hexadecimal string
# and contains at least 64 hexadecimal characters.
def is_valid_content(content):
    try:
        if len(content) % 2 != 0 or len(content) < 64:
            raise ValueError
        int(content, 16)
        return True
    except ValueError:
        print('ft_otp: error: invalid key format.')
        return False

# Reads a plaintext hexadecimal secret from a file, validates it,
# encrypts it using Fernet, and stores the encrypted key in
# the ft_otp.key file.
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

# Configures and parses command-line arguments.
# -g : generate an encrypted ft_otp.key file from a plaintext key.
# -k : generate a TOTP code from an existing encrypted key file.
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