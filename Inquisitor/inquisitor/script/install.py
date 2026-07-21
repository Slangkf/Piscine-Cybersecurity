import subprocess
import venv
import os

# Create the virtual environment
if not os.path.isdir("venv"):
    venv.create("venv", with_pip=True)
print("Virtual environment ready ✅.")

pip = os.path.join("venv", "bin", "pip")

# Install Python dependencies
subprocess.run([pip, "install", "ipaddress", "macaddress", "scapy", "libpcap"], check=True)
print("Dependencies installed ✅.\nActivate the venv with: source venv/bin/activate")
