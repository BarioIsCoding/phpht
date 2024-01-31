from flask import Flask, send_from_directory
import subprocess
import os
import threading    
from plyer import notification

def close():
    os.system("taskkill /fi \"Phpht\" /f")

def runfile():
    close()
    subprocess.run(['python', 'Launcher.py'])

def notify(addon_name, addon_startup_notification):
    notification.notify(
        title = addon_name,
        message = addon_startup_notification,
        app_icon = None,
        timeout = 10,
    )
    close()

app = Flask(__name__)

x = threading.Thread(target=runfile)
x.start()

@app.route('/')
def index():
    return send_from_directory('.', 'Phpht.html')

@app.route('/run_pingbypass')
def run_banbypass():
    notify("PingBypass Executed", "Pings have been bypassed. The user BetterMint can be pinged in discord.gg/basic by writing  instead of the actual ping.")
    subprocess.run(['python', 'PingBypass.py'])
    return 'PingBypass executed'

@app.route('/run_nighttweaks')
def run_nighttweaks():
    notify("NightTweaks Executed", "NightTweaks has been started. Use /help for help.")
    subprocess.run(['python', 'NightTweaks.py'])
    return 'NightTweaks executed'

@app.route('/run_grouptools')
def run_grouptools():
    notify("GroupTools Executed", "You can now change or lock the group name of whichever group you have access to. Do NOT lock before entering Group ID to prevent a crash.")
    subprocess.run(['python', 'GroupTools.py'])

@app.route('/run_sticky')
def run_sticky():
    notify("Sticky Executed", "Sticky has been started and is ready to run. Use /ssticky to set the sticky message.")
    subprocess.run(['python', 'Sticky.py'])

if __name__ == '__main__':
    app.run()
