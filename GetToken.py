import sys
import os
import re
import asyncio
import discord
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLabel, QPushButton


def find_tokens(path):
    path += '\\Local Storage\\leveldb'
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue
        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens


async def get_username_from_token(token):
    client = discord.Client()

async def get_username_from_token(token):
    client = discord.Client()

    async def get_username():
        try:
            await client.start(token, bot=False)
            username = str(client.user)
            await client.logout()
            return username
        except discord.errors.LoginFailure:
            return None  # Return None if login fails

    try:
        return await asyncio.wait_for(get_username(), timeout=10)
    except asyncio.TimeoutError:
        return None  # Return None if the operation times out
    finally:
        await client.close()




def get_tokens_with_usernames():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    loop = asyncio.get_event_loop()
    all_tokens_with_usernames = []

    for platform, path in paths.items():
        if os.path.exists(path):
            tokens = find_tokens(path)
            for token in tokens:
                username = loop.run_until_complete(get_username_from_token(token))
                if username:
                    all_tokens_with_usernames.append((username, token))
    return all_tokens_with_usernames


class TokenSelector(QWidget):
    def __init__(self, tokens_with_usernames):
        super().__init__()

        self.setWindowTitle("Discord Token Selector")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.token_combo = QComboBox()
        self.token_combo.addItem("Select a user")

        for username, _ in tokens_with_usernames:
            self.token_combo.addItem(username)

        layout.addWidget(self.token_combo)

        self.selected_token_label = QLabel()
        layout.addWidget(self.selected_token_label)

        self.select_button = QPushButton("Select User")
        self.select_button.clicked.connect(lambda: self.select_token(tokens_with_usernames))
        layout.addWidget(self.select_button)

        self.setLayout(layout)

    def select_token(self, tokens_with_usernames):
        selected_index = self.token_combo.currentIndex()
        if selected_index > 0:
            _, selected_token = tokens_with_usernames[selected_index - 1]
            self.selected_token_label.setText(f"Selected Token: {selected_token}")
            with open('token.txt', 'w') as f:
                f.write(selected_token)
            self.close()


def main():
    app = QApplication(sys.argv)
    tokens_with_usernames = get_tokens_with_usernames()
    window = TokenSelector(tokens_with_usernames)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
