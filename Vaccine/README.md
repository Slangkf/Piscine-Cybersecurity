*This project was created in July 2026 as part of the 42 curriculum by tclouet.*

![](./utils/note.png)

![](./utils/feedbacks.png)

# Description

*This section presents the project, its goals, and a brief overview.*

The Vaccine program aims to perform SQL injections by providing a URL as a parameter.

The program is written in Python, and its dependencies are managed using a virtual environment created with `venv`.

#### Note:
    This project is intended for educational purposes only. Use it exclusively in controlled environments where you have authorization to perform network analysis.

# Instructions

*This section contains information about installation and execution.*

*Before starting, ensure that Python 3.11 or later and Docker Engine are installed.*

1. ### **Build and start the project:**

    At the root of the project, execute the following commands:

    - Build the Docker image: `make build`.
    - Start the Docker container: `make up`.

    The terminal will display the command to activate the venv in the "vaccine" container.
    
    In separate terminal:

    - Navigate inside one of these containers: `docker exec -it vaccine bash`.    

#### Note:
    To display all the available commands, run: `make help`

2. ### **Set up the container and start the program:**

    Inside the container:
	
    - To activate the virtual environment: `source venv/bin/activate`
    
    - To start the program: `python3 vaccine.py`


3. ### **Stop and clean up the project:**

    - To deactivate the virtual environment, run: `deactivate`.

    - To leave a Docker container, type: `exit`.

    - To clean the project: `make destroy`

#### Note:
    Running `make destroy` will prompt you for confirmation before removing the project resources.

# Tests


# Technical Notes

**SQL injection:**
SQL injection is a technique used to inject elements specifically SQL (Structured Query Language) code into web form fields or page links for transmission to a web server. By doing so, attackers bypass security controls and manage to view or modify data stored in a database, such as passwords or banking details. SQL injection thus enables access to all data—whether personal (e.g., user or employee identities and contact details) or non-personal (e.g., product listings, prices)—contained within an SQL database.

# Resources
 
- []()

