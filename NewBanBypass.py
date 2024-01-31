import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QFont, QColor, QPainter, QGuiApplication

class NotificationWindow(QWidget):
    def __init__(self, message, color):
        super().__init__()
        self.initUI(message, color)

    def initUI(self, message, color):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: #282b30; border-radius: 10px;")

        # Font setup
        font = QFont("Arial", 10)

        # Message label
        self.label = QLabel(message, self)
        self.label.setFont(font)
        self.label.setStyleSheet(f"color: {color}; margin-top: 20px; margin-left: 10px; margin-right: 10px;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Progress bar setup
        self.progress_width = 300
        self.color = QColor(color)
        self.time_left = 5  # Total time in seconds

        # Window size and position
        self.resize(self.progress_width, 80)
        self.moveNotificationToCorner()

        # Timer for progress bar
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgress)
        self.timer.start(500)  # Slower timer for smoother progress bar

    def moveNotificationToCorner(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()  # Use availableGeometry() instead of geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.move(screen_width - self.width() - 10, screen_height - self.height() - 50)

    def updateProgress(self):
        self.time_left -= 0.5
        self.update()  # Trigger a repaint

        if self.time_left <= 0:
            self.timer.stop()
            self.close()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self) 
        painter.setRenderHint(QPainter.Antialiasing)

        # Drawing progress bar at the top
        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)
        current_width = (self.time_left / 5) * self.progress_width
        painter.drawRect(QRect(0, 0, current_width, 5))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    notif = NotificationWindow("This is a success notification!", "#57F287")
    notif.show()
    sys.exit(app.exec_())
