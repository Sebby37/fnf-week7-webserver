# Module imports, done to reduce compiled file size
from os import chdir, path, getcwd
from socketserver import TCPServer
from http.server import SimpleHTTPRequestHandler
from webbrowser import get, register, BackgroundBrowser
from datetime import datetime
from traceback import format_exc
from sys import exit as sys_exit

# Done for error logging
try:
    # Getting the original directory that this file is placed in
    orig_dir = getcwd()
    
    ''' Config file reading and creation '''
    # Creating the config file if it doesn't exist
    if not path.exists("config.ini"):
        with open("config.ini", "w+") as file:
            file.write("# Edit this config file if you need to change where your browser is and what url you want the webserver to use.\n")
            file.write("# If the program doesn't run, delete this file and rerun it. If it doesn't work after that, make a github issue on the repo.\n")
            file.write("[Options]\n")
            file.write("browser=C:\\Program Files\\Firefox Developer Edition\\firefox.exe\n")
            file.write("url=127.0.0.1")
            file.close()
            del file

    # Reading from the config file
    with open("config.ini", "r") as file:
        config = file.readlines()
        file.close()
        del file

    # Getting the browser dir from the config file
    browser_dir = config[3].strip()
    browser_dir = browser_dir.split("=")
    browser_dir = browser_dir[1]
    if not path.exists(browser_dir):
        raise FileNotFoundError("Chosen browser does not exist, edit the chosen browser in config.ini")

    # Getting the url from the config file
    url = config[4].strip()
    url = url.split("=")
    url = url[1]

    # Pyinstaller stuff (https://stackoverflow.com/a/13790741/)
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            from sys import _MEIPASS
            base_path = _MEIPASS
        except Exception:
            base_path = path.abspath(".")

        return path.join(base_path, relative_path)

    # Setting the directory to the fnf directory
    chdir(resource_path("fnf7"))
    
    # Setting up the webserver (because browsers don't let you load images from a file:// directory
    Handler = SimpleHTTPRequestHandler
    with TCPServer((url, 80), Handler) as httpd:
        
        # Opening the page in firefox (because it doesn't work in my chromium browser
        register("user-browser", None, BackgroundBrowser(browser_dir))
        get("user-browser").open(f"http://{url}:80/index.html", new=2)
        
        # Starting the webserver
        httpd.serve_forever()

    # Successful exit
    sys_exit(0)
except:
    # Logging errors to a traceback file
    chdir(orig_dir)
    print("Error occured, check the traceback text file")
    current_time = datetime.now()
    current_time = current_time.strftime("%a, %d %b %Y %H;%M;%S")
    with open(f"Traceback {current_time}.txt", "w+") as traceback_log:
        traceback_log.write(format_exc())
        traceback_log.close()
    
    # Unsuccessful exit
    sys_exit(1)
