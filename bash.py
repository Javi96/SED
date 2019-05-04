


import subprocess
import time
import os
import stat

os.chmod("red.sh", stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

while True:
    os.system("./red.sh")
    print("holaa")
    time.sleep(3)
    
