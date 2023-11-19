from flask import Flask, send_from_directory
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'Phpht.html')  # Make sure this is the correct file name

@app.route('/run_banbypass')
def run_banbypass():
    subprocess.run(['python', 'BanBypass.py'])
    return 'BanBypass executed'

@app.route('/run_nighttweaks')
def run_nighttweaks():
    subprocess.run(['python', 'NightTweaks.py'])
    return 'NightTweaks executed'

@app.route('/run_grouptools')
def run_grouptools():
    subprocess.run(['python', 'GroupTools.py'])
    return 'GroupTools executed'

@app.route('/run_sticky')
def run_sticky():
    subprocess.run(['python', 'Sticky.py'])
    return 'Sticky executed'

if __name__ == '__main__':
    app.run(debug=True)
