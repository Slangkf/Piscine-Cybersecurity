*This project was created in June 2026 as part of the 42 curriculum by tclouet.*

![](../shared/note.png)

![](../shared/feedbacks.png)

# Description

*This section presents the project, its goals, and a brief overview.*

The Spider exercise aims to create a program that recursively extracts all images from a website by providing a URL as a parameter. 

The program is written in Python, and its dependencies are managed through a virtual environment created with venv.

# Instructions

*This section contains information about installation and execution.*

*Before starting, please ensure that Python 3.13 or later is installed.*

1. ### **Set up the virtual environment:**

    From the `spider` directory, run the following commands:
	
    - Create a virtual environment: `python -m venv venv`. 
    - Activate the virtual environment: `source venv/bin/activate`.
    - Install the required dependencies: `pip install requests beautifulsoup4`.
    - Verify that the virtual environment is activated: `which python`.

#### Note:
    The `which python` command should return: `venv/bin/python`.

2. ### **Available commands:**

    - Option `-r`: recursively downloads all images from the specified URL.
    - Option `-r -l [N]`: sets the maximum recursion depth. If not specified, the default value is 5.
    - Option `-p [PATH]`: specifies the directory where downloaded files will be saved. If not specified, `./data/` will be used.

#### Note:
    To display the program help message, type: `python3 spider.py --help`

3. ### **Run the program:**

    `python3 spider.py [-r] [-l N] [-p PATH] URL`

4. ### **Deactivate the virtual environment:**

    - To leave the virtual environment, run: `deactivate`.

# Technical Notes

*This section provides technical information about the technologies used in the project.*

### **The main attributes of the `Response` object returned by `requests.get()`:**

- html.status_code → the HTTP status code (200, 404, etc.).
- html.text → the response content decoded into a Unicode string — this is the raw HTML.
- html.content → the raw content in bytes (undecoded) — useful for images.
- html.headers → the HTTP headers of the response.

### **The `src` attribute can be of three forms:**

- Absolute: https://example.com/images/photo.jpg → usable directly.
- Root-relative: /images/photo.jpg → must be combined with the base domain.
- Path-relative: ../images/photo.jpg → must be resolved relative to the current URL.

`urljoin` handles all three cases automatically. It takes two arguments:
- The base URL (the URL of the current page — args.url).
- The URL found in the src attribute.

### **`urlparse` returns a `ParseResult` object with several attributes:**

ex: `urlparse('https://example.com/images/photo.jpg?size=large')`
- scheme   : 'https'
- netloc   : 'example.com'
- path     : '/images/photo.jpg'
- query    : 'size=large'

### **List vs set:**

For a collection of unique values ​​where you're only checking for membership with `in`, a set is more appropriate:

`authorized_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}`

The difference:
- A list [] iterates through all elements one by one to check membership — O(n)
- A set {} uses a hash to check membership instantly — O(1)

### **The hash rule:**

- In Python, two equal values ​​always produce the same hash: hash('.jpg') == hash('.jpg') → True, always.
This is a guarantee of the language. It doesn't matter where the string `.jpg` comes from: if its content is identical, its hash is identical.

- How the hash is calculated:  
The hash of a string is calculated from its own content, using a mathematical algorithm.
Python takes the bytes of the string character by character and applies a series of mathematical operations to produce an integer: '.jpg' → algorithm → 12345678 (for example).

- Non-iterative search:  
When you search for `extension` in the set, Python calculates `hash(extension)`: obtains the integer 12345678. It uses the hash value to quickly locate the element in the set without iterating through all stored values.
