import os
import subprocess
import time

STATUS_BAT = r'C:\ToolBox\Robocopy\bin\Status_robocp_silent.bat'
START_BAT = r'C:\ToolBox\Robocopy\bin\Start_robocp.bat'
STATUS_FILE = r'C:\ToolBox\Robocopy\bin\status'

TIMEOUT_IN_SECONDS = 10

def check_transfer_status():
    status_process = subprocess.Popen(STATUS_BAT)
    
    start_time = time.time()
    while not os.path.isfile(STATUS_FILE):
        elapsed_time = time.time() - start_time
        
        if elapsed_time > TIMEOUT_IN_SECONDS:
            try:
                os.remove(STATUS_FILE)
            except:
                pass
                
            return -1

        time.sleep(0.1)
    
    with open(STATUS_FILE, 'r') as fp:
        lines = len(fp.readlines())
        
    os.remove(STATUS_FILE)
    
    return lines

def start_transfer():
    transfer_status = check_transfer_status()
    
    if transfer_status == 0:
        subprocess.Popen(START_BAT, creationflags=0x08000000)
    
    return transfer_status
