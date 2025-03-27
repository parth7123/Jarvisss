import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy, QLineEdit
from PyQt5.QtGui import QIcon, QPainter, QColor, QTextCharFormat, QFont, QPixmap, QMovie, QPen, QBrush, QRadialGradient, QFontDatabase, QLinearGradient
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QRectF

# Environment setup
current_dir = os.path.abspath(r"C:\Users\parth\Desktop\Jarvis")
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
GraphicsDirPath = os.path.join(current_dir, "Frontend", "Graphics")
Assistantname = "Jarvis"

# Utility Functions
def AnswerModifier(Answer):
    return '\n'.join(line for line in Answer.split('\n') if line.strip())

def QueryModifier(Query):
    new_query = Query.lower().strip()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]
    if any(word + " " in new_query for word in question_words):
        return new_query.capitalize() + "?"
    return new_query.capitalize() + "."

def SetMicrophoneStatus(status):
    with open(os.path.join(TempDirPath, "Mic.data"), "w", encoding="utf-8") as file:
        file.write(status)

def GetMicrophoneStatus():
    with open(os.path.join(TempDirPath, "Mic.data"), "r", encoding="utf-8") as file:
        return file.read()

def SetAssistantStatus(status):
    with open(os.path.join(TempDirPath, "Status.data"), "w", encoding="utf-8") as file:
        file.write(status)

def GetAssistantStatus():
    with open(os.path.join(TempDirPath, "Status.data"), "r", encoding="utf-8") as file:
        return file.read()

def GraphicsDirectoryPath(filename):
    return os.path.join(GraphicsDirPath, filename)

def TempDirectoryPath(filename):
    return os.path.join(TempDirPath, filename)

def ShowTextToScreen(text):
    with open(TempDirectoryPath("Responses.data"), "w", encoding="utf-8") as file:
        file.write(text)

# Floating Star Background Widget
class StarBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stars = []
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateStars)
        self.timer.start(50)
        self.initializeStars()

    def initializeStars(self):
        self.stars = []
        for _ in range(100):
            x = random.randint(0, self.width())
            y = random.randint(0, self.height())
            speed_x = random.uniform(-0.5, 0.5)
            speed_y = random.uniform(-0.5, 0.5)
            size = random.uniform(1, 3)
            alpha = random.uniform(0.3, 1.0)
            self.stars.append({"x": x, "y": y, "speed_x": speed_x, "speed_y": speed_y, "size": size, "alpha": alpha})

    def updateStars(self):
        for star in self.stars:
            star["x"] += star["speed_x"]
            star["y"] += star["speed_y"]
            if star["x"] < 0 or star["x"] > self.width():
                star["speed_x"] = -star["speed_x"]
            if star["y"] < 0 or star["y"] > self.height():
                star["speed_y"] = -star["speed_y"]
            star["alpha"] = max(0.3, min(1.0, star["alpha"] + random.uniform(-0.05, 0.05)))
        self.update()

    def resizeEvent(self, event):
        self.initializeStars()
        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#1E1B3A"))
        gradient.setColorAt(1, QColor("#3A1B3A"))
        painter.fillRect(self.rect(), gradient)

        for star in self.stars:
            gradient = QRadialGradient(star["x"], star["y"], star["size"] * 3)
            gradient.setColorAt(0, QColor(255, 255, 255, int(255 * star["alpha"])))
            gradient.setColorAt(1, QColor(255, 255, 255, 0))
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QRectF(
                star["x"] - star["size"],
                star["y"] - star["size"],
                star["size"] * 2,
                star["size"] * 2
            ))

# Particle Animation Widget (Holographic Effect)
class ParticleAnimation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        self.setFixedHeight(400)
        self.setFixedWidth(200)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateParticles)
        self.timer.start(30)

    def initializeParticles(self):
        self.particles = []
        for _ in range(50):
            x = random.randint(0, self.width())
            y = random.randint(self.height(), self.height() + 50)
            speed = random.uniform(2, 5)
            size = random.uniform(1, 3)
            self.particles.append({"x": x, "y": y, "speed": speed, "size": size, "alpha": random.uniform(0.5, 1.0)})

    def updateParticles(self):
        for particle in self.particles:
            particle["y"] -= particle["speed"]
            particle["alpha"] = max(0, particle["alpha"] - 0.01)
            if particle["y"] < -particle["size"]:
                particle["y"] = self.height() + random.randint(0, 50)
                particle["x"] = random.randint(0, self.width())
                particle["speed"] = random.uniform(2, 5)
                particle["size"] = random.uniform(1, 3)
                particle["alpha"] = random.uniform(0.5, 1.0)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for particle in self.particles:
            gradient = QRadialGradient(particle["x"], particle["y"], particle["size"] * 3)
            color_center = QColor("#FFB6C1")
            color_center.setAlpha(int(255 * particle["alpha"]))
            gradient.setColorAt(0, color_center)
            color_edge = QColor("#FFB6C1")
            color_edge.setAlpha(0)
            gradient.setColorAt(1, color_edge)
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QRectF(
                particle["x"] - particle["size"],
                particle["y"] - particle["size"],
                particle["size"] * 2,
                particle["size"] * 2
            ))

# Chat Section
class ChatSection(QWidget):
    def __init__(self, on_input_callback=None):
        super().__init__()
        self.old_chat_message = ""
        self.on_input_callback = on_input_callback
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setFont(QFont("Exo", 12))
        self.chat_text_edit.setStyleSheet("""
            background: rgba(255, 255, 255, 20); 
            color: #E6E6FA; 
            border: 1px solid #FFB6C1; 
            border-radius: 10px; 
            padding: 10px;
            font-family: Exo;
        """)
        layout.addWidget(self.chat_text_edit)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter command...")
        self.input_field.setStyleSheet("""
            background: rgba(255, 255, 255, 20); 
            color: #E6E6FA; 
            border: 1px solid #FFB6C1; 
            border-radius: 5px; 
            padding: 8px;
            font-family: Exo;
            font-size: 12px;
        """)
        self.input_field.returnPressed.connect(self.processKeyboardInput)
        layout.addWidget(self.input_field)

        self.particle_anim = ParticleAnimation(self)
        self.particle_anim.initializeParticles()
        layout.addWidget(self.particle_anim, alignment=Qt.AlignCenter)

        self.status_label = QLabel("Awaiting command...")
        self.status_label.setStyleSheet("""
            color: #E6E6FA; 
            font-size: 14px; 
            font-family: Exo;
            background: transparent;
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.updateStatus)
        self.timer.start(100)

    def loadMessages(self):
        with open(TempDirectoryPath("Responses.data"), "r", encoding="utf-8") as file:
            message = file.read().strip()
        if message and message != self.old_chat_message:
            self.addMessage(message, "#E6E6FA")
            self.old_chat_message = message

    def updateStatus(self):
        self.status_label.setText(GetAssistantStatus())

    def processKeyboardInput(self):
        text = self.input_field.text().strip()
        if text:
            modified_query = QueryModifier(text)
            self.addMessage(f"You: {modified_query}", "#E6E6FA")
            if self.on_input_callback:
                self.on_input_callback("keyboard", modified_query)
            self.input_field.clear()

    def addMessage(self, message, color):
        self.current_message = message
        self.current_color = color
        self.current_text = ""
        self.char_index = 0
        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self.updateTyping)
        self.typing_timer.start(30)

    def updateTyping(self):
        if self.char_index < len(self.current_message):
            self.current_text += self.current_message[self.char_index]
            self.char_index += 1
            cursor = self.chat_text_edit.textCursor()
            format = QTextCharFormat()
            format.setForeground(QColor(self.current_color))
            self.chat_text_edit.setText("")
            cursor.insertText(self.current_text + "\n", format)
            self.chat_text_edit.ensureCursorVisible()
        else:
            self.typing_timer.stop()

    def displayResponse(self, response):
        ShowTextToScreen(response)

# Initial Screen
class InitialScreen(QWidget):
    def __init__(self, on_input_callback=None):
        super().__init__()
        self.on_input_callback = on_input_callback
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel(f"{Assistantname} AI")
        title_label.setStyleSheet("""
            color: #E6E6FA; 
            font-size: 36px; 
            font-family: Exo; 
            font-weight: bold;
            background: transparent;
        """)
        layout.addWidget(title_label)

        self.particle_anim = ParticleAnimation(self)
        self.particle_anim.initializeParticles()
        layout.addWidget(self.particle_anim)

        self.mic_label = QLabel()
        self.mic_label.setFixedSize(80, 80)
        self.toggled = True

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            color: #E6E6FA; 
            font-size: 16px; 
            font-family: Exo;
            background: transparent;
        """)
        layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        self.toggleMicIcon()
        self.mic_label.mousePressEvent = self.toggleMicIcon
        layout.addWidget(self.mic_label, alignment=Qt.AlignCenter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateStatus)
        self.timer.start(100)

    def toggleMicIcon(self, event=None):
        mic_on_path = GraphicsDirectoryPath("Mic_on.png")
        mic_off_path = GraphicsDirectoryPath("Mic_off.png")
        pixmap = QPixmap(mic_on_path if self.toggled else mic_off_path)
        if pixmap.isNull():
            self.status_label.setText("Mic icon not found")
            return
        self.mic_label.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio))
        SetMicrophoneStatus("False" if self.toggled else "True")
        self.toggled = not self.toggled
        anim = QPropertyAnimation(self.mic_label, b"geometry")
        anim.setDuration(300)
        anim.setStartValue(self.mic_label.geometry())
        anim.setEndValue(self.mic_label.geometry().adjusted(0, -20, 0, -20))
        anim.setEasingCurve(QEasingCurve.OutBounce)
        anim.start()
        if not self.toggled:
            self.status_label.setText("Listening...")
            # QTimer.singleShot(2000, lambda: self.processSpeechInput("Sample speech input"))

    def processSpeechInput(self, text):
        modified_query = QueryModifier(text)
        ShowTextToScreen(f"You (speech): {modified_query}")
        self.status_label.setText("Processing...")
        if self.on_input_callback:
            self.on_input_callback("speech", modified_query)

    def updateStatus(self):
        self.status_label.setText(GetAssistantStatus())

    def displayResponse(self, response):
        ShowTextToScreen(response)

# Custom Top Bar
class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.setFixedHeight(40)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        title = QLabel(f"{Assistantname} AI")
        title.setStyleSheet("""
            color: #E6E6FA; 
            font-size: 16px; 
            font-family: Exo; 
            font-weight: bold;
        """)
        layout.addWidget(title)

        layout.addStretch()

        for text, icon, index in [
            ("Home", "Home.png", 0),
            ("Chat", "Chats.png", 1)
        ]:
            btn = QPushButton(text)
            btn.setIcon(QIcon(GraphicsDirectoryPath(icon)))
            btn.setStyleSheet("""
                QPushButton { 
                    background: rgba(255, 255, 255, 20); 
                    color: #E6E6FA; 
                    padding: 5px 15px; 
                    border-radius: 5px; 
                    font-family: Exo;
                    font-size: 12px;
                }
                QPushButton:hover { 
                    background: #FFB6C1; 
                    color: #1E1B3A;
                }
            """)
            btn.clicked.connect(lambda _, i=index: self.stacked_widget.setCurrentIndex(i))
            layout.addWidget(btn)

        for icon, action in [
            ("Minimize2.png", self.minimizeWindow),
            ("Minimize.png", self.maximizeWindow),
            ("Close.png", self.closeWindow)
        ]:
            btn = QPushButton()
            btn.setIcon(QIcon(GraphicsDirectoryPath(icon)))
            btn.setStyleSheet("""
                background: rgba(255, 255, 255, 20); 
                padding: 5px; 
                border-radius: 5px;
            """)
            btn.clicked.connect(action)
            layout.addWidget(btn)

        self.draggable = True
        self.offset = None

        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(500)
        self.anim.setStartValue(QPoint(0, -40))
        self.anim.setEndValue(QPoint(0, 0))
        self.anim.setEasingCurve(QEasingCurve.OutQuad)
        self.anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#1E1B3A"))

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        parent = self.parent()
        parent.showNormal() if parent.isMaximized() else parent.showMaximized()

    def closeWindow(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset:
            self.parent().move(event.globalPos() - self.offset)

# Main Window
class MainWindow(QMainWindow):
    def __init__(self, on_input_callback=None):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 1200, 800)

        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont("C:/Users/parth/Desktop/Jarvis/Frontend/Fonts/Exo-Regular.ttf")
        if font_id != -1:
            font_families = font_db.applicationFontFamilies(font_id)
            if font_families:
                QFontDatabase().addApplicationFont(font_families[0])

        self.star_background = StarBackground(self)
        self.star_background.setGeometry(0, 0, self.width(), self.height())

        self.stacked_widget = QStackedWidget(self)
        self.initial_screen = InitialScreen(on_input_callback)
        self.chat_section = ChatSection(on_input_callback)
        self.stacked_widget.addWidget(self.initial_screen)
        self.stacked_widget.addWidget(self.chat_section)

        self.setCentralWidget(self.stacked_widget)
        self.setMenuWidget(CustomTopBar(self, self.stacked_widget))

    def resizeEvent(self, event):
        self.star_background.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def displayResponse(self, response):
        current_widget = self.stacked_widget.currentWidget()
        current_widget.displayResponse(response)

def start_gui(app=None, on_input_callback=None):
    if app is None:
        app = QApplication(sys.argv)
    window = MainWindow(on_input_callback)
    window.show()
    return app, window

if __name__ == "__main__":
    app, window = start_gui()
    sys.exit(app.exec_())