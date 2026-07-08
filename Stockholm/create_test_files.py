from pathlib import Path

# List of file extensions used to generate test files.
# These extensions match the file types handled by the main program.
authorized_extensions = {
    '.der', '.pfx', '.key', '.crt', '.csr', '.p12', '.pem', '.odt', '.ott', '.sxw',
    '.stw', '.uot', '.3ds', '.max', '.3dm', '.ods', '.ots', '.sxc', '.stc', '.dif',
    '.slk', '.wb2', '.odp', '.otp', '.sxd', '.std', '.uop', '.odg', '.otg', '.sxm',
    '.mml', '.lay', '.lay6', '.asc', '.sqlite3', '.sqlitedb', '.sql', '.accdb',
    '.mdb', '.db', '.dbf', '.odb', '.frm', '.myd', '.myi', '.ibd', '.mdf',
    '.ldf', '.sln', '.suo', '.cs', '.c', '.cpp', '.pas', '.h', '.asm', '.js',
    '.cmd', '.bat', '.ps1', '.vbs', '.vb', '.pl', '.dip', '.dch', '.sch',
    '.brd', '.jsp', '.php', '.asp', '.rb', '.java', '.jar', '.class', '.sh',
    '.mp3', '.wav', '.swf', '.fla', '.wmv', '.mpg', '.vob', '.mpeg', '.asf',
    '.avi', '.mov', '.mp4', '.3gp', '.mkv', '.3g2', '.flv', '.wma', '.mid',
    '.m3u', '.m4u', '.djvu', '.svg', '.ai', '.psd', '.nef', '.tiff', '.tif',
    '.cgm', '.raw', '.gif', '.png', '.bmp', '.jpg', '.jpeg', '.vcd', '.iso',
    '.backup', '.zip', '.rar', '.7z', '.gz', '.tgz', '.tar', '.bak', '.tbk',
    '.bz2', '.PAQ', '.ARC', '.aes', '.gpg', '.vmx', '.vmdk', '.vdi', '.sldm',
    '.sldx', '.sti', '.sxi', '.602', '.hwp', '.snt', '.onetoc2', '.dwg',
    '.pdf', '.wk1', '.wks', '.123', '.rtf', '.csv', '.txt', '.vsdx', '.vsd',
    '.edb', '.eml', '.msg', '.ost', '.pst', '.potm', '.potx', '.ppam',
    '.ppsx', '.ppsm', '.pps', '.pot', '.pptm', '.pptx', '.ppt', '.xltm',
    '.xltx', '.xlc', '.xlm', '.xlt', '.xlw', '.xlsb', '.xlsm', '.xlsx',
    '.xls', '.dotx', '.dotm', '.dot', '.docm', '.docb', '.docx'
}

# Creates sample files with authorized extensions in the target directory.
# Used to test the file processing functionality of the program.
def create_test_files():
    directory = Path('/home/infection')
    for index, extension in enumerate(authorized_extensions):
        filename = directory / f"test_file_{index}{extension}"
        with open(filename, "w") as f:
            f.write(
                f"Test file number: {index}\n"
                f"Extension: {extension}\n"
            )
        print(f"Create: {filename}")

# Execute the test file generation when the script is run directly.
if __name__ == "__main__":
    create_test_files()
