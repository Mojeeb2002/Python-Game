import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                            QComboBox, QMessageBox, QFrame, QInputDialog)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette, QColor
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, select
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# Database setup
engine = create_engine(DATABASE_URL, echo=False)
metadata = MetaData()

scores = Table(
    'scores',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=False),
    Column('score', Integer, nullable=False),
    Column('created_at', DateTime, default=datetime.now)
)

metadata.create_all(engine)

def set_dark_theme(app):
    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)

class NumberGuesserGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.secret_number = 0
        self.tries = 0
        self.max_tries = 0
        self.range_limit = 0
        self.current_score = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Number Guesser')
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 2px solid #3d3d3d;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 2px solid #3d3d3d;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 2px solid #3d3d3d;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
            QMessageBox {
                background-color: #2d2d2d;
            }
            QMessageBox QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 2px solid #3d3d3d;
                border-radius: 5px;
                padding: 8px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #3d3d3d;
            }
            QInputDialog {
                background-color: #2d2d2d;
            }
            QInputDialog QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QInputDialog QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 2px solid #3d3d3d;
                border-radius: 5px;
                padding: 8px;
            }
            QInputDialog QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 2px solid #3d3d3d;
                border-radius: 5px;
                padding: 8px;
                min-width: 80px;
            }
            QInputDialog QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel('Number Guesser')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 24px; font-weight: bold; color: #ffffff;')
        layout.addWidget(title)

        # Level selection
        level_frame = QFrame()
        level_frame.setStyleSheet('background-color: #2d2d2d; border-radius: 10px; padding: 20px;')
        level_layout = QVBoxLayout(level_frame)

        level_label = QLabel('Select Difficulty Level:')
        self.level_combo = QComboBox()
        self.level_combo.addItems(['Easy (Unlimited Tries)', 'Medium (10 Tries)', 'Hard (5 Tries)', 'Custom'])
        
        level_layout.addWidget(level_label)
        level_layout.addWidget(self.level_combo)
        layout.addWidget(level_frame)

        # Game area
        self.game_frame = QFrame()
        self.game_frame.setStyleSheet('background-color: #2d2d2d; border-radius: 10px; padding: 20px;')
        game_layout = QVBoxLayout(self.game_frame)

        self.status_label = QLabel('Select a level to start playing')
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.guess_input = QLineEdit()
        self.guess_input.setPlaceholderText('Enter your guess')
        self.guess_input.setEnabled(False)
        self.guess_input.returnPressed.connect(self.check_guess)
        
        self.submit_button = QPushButton('Submit Guess')
        self.submit_button.setEnabled(False)
        self.submit_button.clicked.connect(self.check_guess)

        game_layout.addWidget(self.status_label)
        game_layout.addWidget(self.guess_input)
        game_layout.addWidget(self.submit_button)
        layout.addWidget(self.game_frame)

        # Start button
        self.start_button = QPushButton('Start Game')
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button)

        # Set window size and position
        self.setMinimumSize(500, 600)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_game(self):
        level = self.level_combo.currentIndex()
        if level == 0:  # Easy
            self.range_limit = 100
            self.max_tries = float('inf')
        elif level == 1:  # Medium
            self.range_limit = 100
            self.max_tries = 10
        elif level == 2:  # Hard
            self.range_limit = 100
            self.max_tries = 5
        else:  # Custom
            custom_range, ok = QInputDialog.getInt(self, 'Custom Range', 'Enter upper limit:', 100, 1, 1000)
            if not ok:
                return
            custom_tries, ok = QInputDialog.getInt(self, 'Custom Tries', 'Enter number of tries:', 10, 1, 100)
            if not ok:
                return
            self.range_limit = custom_range
            self.max_tries = custom_tries

        self.secret_number = random.randint(1, self.range_limit)
        self.tries = 0
        self.guess_input.setEnabled(True)
        self.submit_button.setEnabled(True)
        self.start_button.setEnabled(False)
        self.status_label.setText(f'Guess a number between 1 and {self.range_limit}')

    def check_guess(self):
        try:
            guess = int(self.guess_input.text())
            self.tries += 1
            remaining_tries = self.max_tries - self.tries if self.max_tries != float('inf') else '∞'

            if guess == self.secret_number:
                self.current_score = self.calculate_score()
                self.show_game_over(True)
            elif guess < self.secret_number:
                self.status_label.setText(f'Too low! Tries left: {remaining_tries}')
            else:
                self.status_label.setText(f'Too high! Tries left: {remaining_tries}')

            if self.tries >= self.max_tries and self.max_tries != float('inf'):
                self.show_game_over(False)

            self.guess_input.clear()
        except ValueError:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter a valid number')

    def calculate_score(self):
        score = 1000 - (self.tries * 100)
        return max(0, score)

    def show_game_over(self, won):
        if won:
            message = f'Congratulations! You guessed the number in {self.tries} tries!\nYour score: {self.current_score}'
        else:
            message = f'Game Over! The number was {self.secret_number}'

        QMessageBox.information(self, 'Game Over', message)
        
        # Only prompt for username if the game was won
        if won:
            self.save_score()
        
        self.reset_game()

    def save_score(self):
        username, ok = QInputDialog.getText(self, 'Save Score', 'Enter your username:')
        if ok and username:
            with engine.connect() as conn:
                conn.execute(scores.insert().values(username=username, score=self.current_score))
                conn.commit()

    def reset_game(self):
        self.guess_input.setEnabled(False)
        self.submit_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.status_label.setText('Select a level to start playing')
        self.guess_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    set_dark_theme(app)
    game = NumberGuesserGame()
    game.show()
    sys.exit(app.exec_())
