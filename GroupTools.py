import sys
import discord
import asyncio
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget
from threading import Thread
from PyQt5.QtCore import pyqtSignal, QObject, QTimer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

intents = discord.Intents.default()
client = discord.Client(intents=intents, selfbot=True)  # Adjusted as per your preference

# Variables for group DM ID and name change interval
name_change_interval = 4  # seconds between name changes, adjust to avoid rate limit
lock_name_change = False  # Control variable for locking name change

# Signal class for thread-safe operations
class Signal(QObject):
    name_change_signal = pyqtSignal(str)

@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user}')

async def change_group_name(group_id, name):
    group = client.get_channel(group_id)
    if group is None or not isinstance(group, discord.GroupChannel):
        logging.warning("Group DM not found or not a GroupChannel.")
        return

    try:
        await group.edit(name=name)
        logging.info(f"Changed group name to '{name}'")
    except Exception as e:
        logging.error(f"Failed to change group name: {e}")

async def change_group_name_periodically(signal, group_id):
    global lock_name_change
    while lock_name_change:
        signal.name_change_signal.emit("request_name")
        await asyncio.sleep(name_change_interval)
        
class MainWindow(QMainWindow):
    def __init__(self, loop, signal):
        super().__init__()
        self.loop = loop
        self.signal = signal
        self.setWindowTitle("Discord Group Name Changer")
        self.setGeometry(100, 100, 280, 150)  # Adjusted for additional input

        layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter Group Name")
        layout.addWidget(self.name_input)

        self.id_input = QLineEdit(self)  # Corrected variable name
        self.id_input.setPlaceholderText("Enter Group ID")
        layout.addWidget(self.id_input)

        self.change_button = QPushButton("Change Name", self)
        self.change_button.clicked.connect(self.change_name)
        layout.addWidget(self.change_button)

        self.lock_button = QPushButton("Lock Group Name", self)
        self.lock_button.setStyleSheet("background-color: green")
        self.lock_button.clicked.connect(self.toggle_lock)
        layout.addWidget(self.lock_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect signal for thread-safe name change
        self.signal.name_change_signal.connect(self.thread_safe_name_change)

    def change_name(self):
        group_name = self.name_input.text()
        group_id = int(self.id_input.text())  # Ensure you get the group ID as an integer
        asyncio.run_coroutine_threadsafe(change_group_name(group_id, group_name), self.loop)

    def toggle_lock(self):
        global lock_name_change
        lock_name_change = not lock_name_change
        group_id = int(self.id_input.text())  # Get group ID for locking mechanism
        if lock_name_change:
            self.lock_button.setText("Unlock Group Name")
            self.lock_button.setStyleSheet("background-color: red")
            asyncio.run_coroutine_threadsafe(change_group_name_periodically(self.signal, group_id), self.loop)
        else:
            self.lock_button.setText("Lock Group Name")
            self.lock_button.setStyleSheet("background-color: green")

    def thread_safe_name_change(self, request):
        if request == "request_name":
            group_name = self.name_input.text()
            group_id = int(self.id_input.text())  # Get the group ID for name change
            asyncio.run_coroutine_threadsafe(change_group_name(group_id, group_name), self.loop)

def start_discord_bot(loop, signal):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start(token, bot=False))  # Set bot to False for user account (selfbot)

def start_ui(loop, signal):
    app = QApplication(sys.argv)
    mainWindow = MainWindow(loop, signal)
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # Reading token from 'token.txt' file
    with open('token.txt', 'r') as file:
        token = file.read().strip()

    loop = asyncio.new_event_loop()
    signal = Signal()
    t = Thread(target=start_discord_bot, args=(loop, signal))
    t.start()

    start_ui(loop, signal)