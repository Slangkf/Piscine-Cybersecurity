*This project was created in June 2026 as part of the 42 curriculum by tclouet.*

![](./utils/note.png)

![](./utils/feedback.png)

# Description

*This section presents the project, its goals, and a brief overview.*

The ft_otp exercise aims to create a program that generates a Time-based One-Time Password (TOTP) using the HMAC-based One-Time Password (HOTP) algorithm.

The program is written in Python, and its dependencies are managed through a virtual environment created with venv.

# Instructions

*This section contains information about installation and execution.*

*Before starting, please ensure that Python 3.13 or later is installed.*

1. ### **Set up the virtual environment:**

    From the `ft_otp` directory, run the following commands:
	
    - Create a virtual environment: `python -m venv venv`. 
    - Activate the virtual environment: `source venv/bin/activate`.
    - Install the required dependency: `pip install cryptography`.
    - Verify that the virtual environment is activated: `which python`.

#### Note:
    The `which python` command should return: `venv/bin/python`.

2. ### **Configure the FERNET_KEY variable:**

    Before running the program, generate a Fernet key and assign it to the `FERNET_KEY` variable in the source code.

    Generate a new key with Python:

    ```bash
    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    ```

    Copy the generated value and replace the default value of `FERNET_KEY`:

    `FERNET_KEY` = "your-generated-key"

    Keep this key secure. Any `ft_otp.key` file encrypted with this key can only be decrypted using the same Fernet key. If the key is lost, the encrypted data cannot be recovered.

#### Note:
    The output of `Fernet.encrypt()` is a URL-safe Base64 string.

3. ### **Run the program:**

    *Before running the program, you should have a 64 hexadecimal key in a `.txt` file.*

    - `python3 ft_otp.py -g <path_to_your_file>.txt`: the program stores the hexadecimal key in an encrypted file named ft_otp.key, created in the current directory.
    - `python3 ft_otp.py -k ft_otp.key`: the program generates a new temporary password based on the key provided as an argument and prints it on the standard output.

#### Note:
    To display the program help message, type: `python3 ft_otp.py --help`

4. ### **Compare the generated password with oathtool:**

    To verify that `ft_otp.py` generates correct OTPs, you can compare its output against `oathtool`:

    Make sure your virtual environment is activated, then install oathtool:

    `pip install oathtool`

    Comparison command:

    `cat <path_to_your_file>.txt | xxd -r -p | base32 | oathtool --totp`

    - `cat <path_to_your_file>.txt` outputs the plaintext hex secret key.
    - `xxd -r -p` decodes that hex string back into raw bytes.
    - `base32` re-encodes those same raw bytes into Base32, the format expected by this package.
    - `oathtool --totp -` reads the Base32 key from standard input and generates the current TOTP.

    The result should match the output of:

    `python3 ft_otp.py -k ft_otp.key`

    (Run both commands within the same 30-second window, since the TOTP value changes every 30 seconds.)

#### Note:
    This `oathtool` is the PyPI package (a third-party Python wrapper), not the official GNU `oath-toolkit` binary — used here since it installs without root access. Unlike the official tool, it always decodes the key as Base32, so the hex secret must be converted first, or it will silently produce a wrong OTP.

5. ### **Deactivate the virtual environment:**

    - To leave the virtual environment, run: `deactivate`.

# Technical Notes

**Hexadecimal**
A way to represent binary data as text, using 16 symbols (`0-9`, `a-f`). Used here to store the secret key as plain text before it gets encrypted.

**HMAC (Hash-based Message Authentication Code)**
A way to combine a secret key with a message to produce a unique,
fixed-size output. The same key and message always give the same
result, but changing either one completely changes the output. Here,
it's used with SHA-1 to turn the secret key and a counter into the
one-time password.

**Base64**
A way to represent binary data as text, using 64 characters
(`A-Z`, `a-z`, `0-9`, `+`, `/`). Used here to store the Fernet encryption key and the encrypted secret as plain text.

**Base32**
Similar to Base64, but with only 32 characters (`A-Z`, `2-7`), making it simpler and case-insensitive. It's the standard format for OTP secrets in most authenticator apps, and the format required by the `oathtool` package used in this project.

# Resources

[RFC6238](https://datatracker.ietf.org/doc/html/rfc6238)  
[Implement your own TOTP generator](https://dev.to/vimiomori/implementing-your-own-time-based-otp-generator-1n35)
