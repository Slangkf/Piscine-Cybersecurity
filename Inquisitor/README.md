*This project was created in July 2026 as part of the 42 curriculum by tclouet.*

![](./utils/note.png)

![](./utils/feedbacks.png)

# Description

*This section presents the project, its goals, and a brief overview.*

The Inquisitor program aims to perform full-duplex ARP poisoning, allowing it to intercept traffic between an FTP client and an FTP server. It should also be able to analyze intercepted traffic and display the names of files uploaded from the FTP client to the FTP server.

The program is written in Python, and its dependencies are managed using a virtual environment created with `venv`.

#### Note:
    This project is intended for educational purposes only. Use it exclusively in controlled environments where you have authorization to perform network analysis.

# Architecture

The project uses three Docker containers connected through an isolated network:

- Client: generates files and uploads them through FTP.

- Server: runs an FTP server and stores uploaded files.

- Inquisitor: performs ARP poisoning between the client and server, intercepts packets, and analyzes FTP traffic.


# Instructions

*This section contains information about installation and execution.*

*Before starting, ensure that Python 3.11 or later and Docker Engine are installed.*

1. ### **Build and start the project:**

    At the root of the project, execute the following commands:

    - Build all the Docker images: `make build`.
    - Start all the Docker containers: `make up`.

    The terminal will display the command to activate the venv in the "inquisitor" container, as well as the IP and MAC addresses of each container.
    
    In separate terminals:

    - Navigate inside one of these containers: `docker exec -it <client/inquisitor/server> bash`.    

#### Note:
    To display all the available commands, run: `make help`

2. ### **Set up the client container:**

    Inside the client container:
	
    - To connect the FTP client to the server: `tnftp server 21`
    - Use `anonymous` as the username.

    You can choose your own password. Once this is done, you are connected to the FTP server.

3. ### **Set up the inquisitor container:**

    Inside the inquisitor container:
	
    - Activate the virtual environment: `source venv/bin/activate`.

    To intercept the network traffic through ARP poisoning:

    - Launch the Inquisitor program: `python3 inquisitor.py <IP_client> <MAC_client> <IP_server> <MAC_server>`

    The program must display the name of the uploaded file.

#### Note:
    The `which python` command should return: `/app/venv/bin/python`.

4. ### **Check the server container:**

    Inside the server container:
	
    - Check that files are correctly uploaded: `ls`.
    - Check the content of a file: `cat <file_name>`

5. ### **Stop and clean up the project:**

    - To deactivate the virtual environment, run: `deactivate`.

    - To leave a Docker container, type: `exit`.

    - To clean the project: `make destroy`

#### Note:
    Running `make destroy` will prompt you for confirmation before removing the project resources.

# Tests

*For these tests, the client IPv4/MAC address pair is: `10.89.1.3 2a:de:ae:2d:af:83` and the server IPv4/MAC address pair is: `10.89.1.2 16:c6:de:1f:b5:f3`*

**From the inquisitor container shell:**

- Run the program without arguments: `python3 inquisitor.py`: should output a usage error listing the required arguments.

- Run the program with invalid arguments: `python3 inquisitor.py string 6:c6:de:1f:b5:f3 10.89.1.2 string2`: should output an error message.

- Run the program with an IPv6 format instead of an IPv4: `python3 inquisitor.py 2001:db8:85a3::8a2e:370:7334 6:c6:de:1f:b5:f1 10.89.1.2 6:c6:de:1f:b5:f3`: should output an error message.

- Run the program with a wrong MAC address format: `python3 inquisitor.py 10.89.1.3 2a:de::2d:af:83 10.89.1.2 16:c6:de:1f:b5:f3`: should output an error message.

- Run the program with a wrong IPv4/MAC pair: `python3 inquisitor.py 10.89.1.3 16:c6:de:1f:b5:f3 10.89.1.2 2a:de:ae:2d:af:83`: should output an error message.

- Run the program with the inquisitor container IPv4/MAC pair: `python3 inquisitor.py 10.89.1.4 16:a6:e1:85:62:28 10.89.1.2 2a:de:ae:2d:af:83`: should output an error message.

- Run the program with the same IPv4/MAC pair for client and server: `python3 inquisitor.py 10.89.1.3 2a:de:ae:2d:af:83 10.89.1.3 2a:de:ae:2d:af:83`: the program should run but not display any file name, since traffic between two truly distinct machines never passes through the inquisitor in this case. The file transfer between the client and the server must still complete normally.

- Run the program with the client/server IPv4/MAC pairs inverted: `python3 inquisitor.py 10.89.1.2 16:c6:de:1f:b5:f3 10.89.1.3 2a:de:ae:2d:af:83`: the program and the file tranfer should run normaly.

- Run the program with the correct arguments: `python3 inquisitor.py 10.89.1.3 2a:de:ae:2d:af:83 10.89.1.2 16:c6:de:1f:b5:f3`: the program should run and wait for a file transfer to display the file name.

- Send a SIGINT to stop the inquisitor program: `CTRL+C`: the program should stop and restore the ARP tables. The file transfer between the FTP client and the FTP server should keep working normally afterward.

**From the client container shell:**

- Check the ARP table before starting the attack: `arp -a`: should show the real MAC addresses for the server and the inquisitor.

- Check the ARP table while the attack is running: `arp -a`: the server's entry should now show the inquisitor's MAC address instead of its real one.

**From within an FTP session on the client (inside the `/uploads` directory):**

- Send a file to the server: `put /home/test_environment/test_file_<number.extension> <file_name_of_your_choice>`: the inquisitor program should display the file name and the transfer should complete.

- Get a file from the server: `get <file_name> /app/<file_name>`: the inquisitor program should display the file name and the transfer should complete.

**From the server container shell:**

- Check the ARP table before starting the attack: `arp -a`: should show the real MAC addresses for the client and the inquisitor.

- Check the ARP table while the attack is running: `arp -a`: the client's entry should now show the inquisitor's MAC address instead of its real one.

# Technical Notes

**ARP**  
The Address Resolution Protocol (ARP) is a protocol used to map an IPv4 address to the MAC address of a device on a local area network (LAN). This allows devices to communicate at the data link layer while using IP addresses at the network layer.

This mapping procedure is important because IP and MAC addresses differ in length, requiring translation for systems to recognize one another. The most widely used IP version today is IP version 4 (IPv4). An IP address is 32 bits long, whereas MAC addresses are 48 bits long. ARP maps an IPv4 address to the corresponding MAC address of a device on the local network.

**ARP spoofing**  
ARP spoofing can be used to perform a man-in-the-middle (MITM) attack by redirecting traffic between two hosts through the attacker.

**OSI**  
The OSI (Open Systems Interconnection) model is a conceptual reference model that standardizes how network communications are structured and understood. It divides the communication process into seven layers, each with specific functions and responsibilities. Although modern networks primarily use the TCP/IP protocol suite, the OSI model is widely used to understand network operations, troubleshoot communication issues, and analyze the security risks and vulnerabilities associated with each layer.

**Router**  
A router is a networking device that connects different networks and forwards data packets between them. In a local area network (LAN), the router typically acts as the default gateway, receiving traffic destined for external networks (such as the Internet) and routing incoming and outgoing traffic to the appropriate destination.

**FTP protocol**  
The File Transfer Protocol (FTP) is a standard network protocol used to transfer files between a client and a server over a TCP/IP network. It allows users to upload, download, rename, delete, and manage files on a remote server. FTP typically uses TCP port 21 for control commands and TCP port 20 for data transfer in active mode.

# Resources
 
- [Docker Compose documentation](https://docs.docker.com/reference/cli/docker/compose/)
- [TNFTP documentation](https://manpages.ubuntu.com/manpages/jammy/man1/tnftp.1.html)
- [VSFTPD Configuration](https://doc.ubuntu-fr.org/vsftpd)
- [Create a network scanner](https://www.youtube.com/watch?v=TX-MSSIjL8E)
