# main.py
import time
from fastapi import FastAPI
from bootstrap import start_system
from services.oled_display import show_text
from datetime import datetime
import subprocess
app = FastAPI()

start_system()



def get_ip_wlan0():
    try:
        output = subprocess.check_output("ip -4 addr show wlan0", shell=True).decode()
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("inet "):
                return "ssh pi@"+line.split()[1].split('/')[0]
        return "No IP"
    except:
        return "No Wi-Fi"

show_text(get_ip_wlan0())
@app.get("/")
def read_root():
    return {"Hello": "World"}
