import argparse
import sys
from pathlib import Path


def is_valid_argument(arguments):
    try:
        return True
    except :
        print('')
        return False

# Creates and parses the command-line arguments provided by the user.
def parse_arguments():
    parser = argparse.ArgumentParser(description='SQL injection program for educational purpose only.')
    parser.add_argument('-o', type=str, help='archive file, if not specified data will be stored in archive.txt')
    parser.add_argument('-X', type=str, help='type of request, if not specified GET will be used')
    parser.add_argument('URL', type=str, help='Website URL to perform a SQL injection')
    return parser.parse_args()

# Main entry point: parses arguments, validates them, then launches the attack.
def main():
    args = parse_arguments()
    if is_valid_argument(args):
       vaccine()

# Execute the main function only when this script is run directly
if __name__ == "__main__":
    main()
