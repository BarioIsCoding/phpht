import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineCore import QWebEngineProfile

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView(self)
        self.setCentralWidget(self.browser)
        self.browser.loadFinished.connect(self.on_load_finished)
        self.profile = QWebEngineProfile("No-Store", self.browser)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        self.browser.setPage(QWebEngineView(self.profile).page())
        self.browser.load("https://discord.com/login")

def main():
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
