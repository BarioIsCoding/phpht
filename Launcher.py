from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

class CustomBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phpht")  # Set the window title
        self.browser = QWebEngineView()  # Create a web engine view
        self.setCentralWidget(self.browser)
        self.browser.setUrl(QUrl("http://127.0.0.1:5000"))  # Set the URL here

if __name__ == "__main__":
    app = QApplication([])
    window = CustomBrowser()
    window.show()
    app.exec_()
