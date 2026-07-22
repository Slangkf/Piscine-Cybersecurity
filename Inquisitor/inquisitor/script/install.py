import subprocess
import venv
import os

# Create the virtual environment
if not os.path.isdir("venv"):
    venv.create("venv", with_pip=True)
print("Virtual environment of the inquisitor container ready ✅.")

pip = os.path.join("venv", "bin", "pip")

# Install Python dependencies
subprocess.run([pip, "install", "macaddress", "scapy"], check=True)
print("Dependencies of the inquisitor container installed ✅.")
