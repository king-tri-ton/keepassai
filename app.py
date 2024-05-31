import sys
import sqlite3
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QListWidget
from cryptography.fernet import Fernet
from openai import OpenAI
from config import *

def load_key():
    """Loads a key from the `secret.key` file or creates a new one if the file does not exist."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
    return key

# Loading the encryption key
key = load_key()
cipher_suite = Fernet(key)

def encrypt_password(password):
    return cipher_suite.encrypt(password.encode())

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()

def generate_password(prompt):
    openai = OpenAI(api_key=AI_TOKEN)
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=64
    )
    choice = response.choices[0]
    message = choice.message
    return message.content.strip()

def analyze_password(password):
    openai = OpenAI(api_key=AI_TOKEN)
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Analyze the security of the following password: {password}"}
        ],
        max_tokens=64
    )
    choice = response.choices[0]
    message = choice.message
    return message.content.strip()

def init_db():
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, service TEXT UNIQUE, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

class PasswordManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Password Manager')

        layout = QVBoxLayout()

        self.serviceLabel = QLabel('Service:')
        self.serviceInput = QLineEdit()
        layout.addWidget(self.serviceLabel)
        layout.addWidget(self.serviceInput)

        self.usernameLabel = QLabel('Username:')
        self.usernameInput = QLineEdit()
        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameInput)

        self.passwordLabel = QLabel('Password:')
        self.passwordInput = QLineEdit()
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordInput)

        self.generateButton = QPushButton('Generate Password')
        self.generateButton.clicked.connect(self.generate_password)
        layout.addWidget(self.generateButton)

        self.saveButton = QPushButton('Save Password')
        self.saveButton.clicked.connect(self.save_password)
        layout.addWidget(self.saveButton)

        self.analyzeButton = QPushButton('Analyze Password')
        self.analyzeButton.clicked.connect(self.analyze_password)
        layout.addWidget(self.analyzeButton)

        self.analysisOutput = QTextEdit()
        self.analysisOutput.setReadOnly(True)
        layout.addWidget(self.analysisOutput)

        self.accountsList = QListWidget()
        self.accountsList.itemClicked.connect(self.load_account_details)
        layout.addWidget(self.accountsList)

        self.loadAccountsButton = QPushButton('Load Accounts')
        self.loadAccountsButton.clicked.connect(self.load_accounts)
        layout.addWidget(self.loadAccountsButton)

        self.setLayout(layout)
        self.load_accounts()  # Loading accounts at startup

    def generate_password(self):
        prompt = "Generate a secure password."
        password = generate_password(prompt)
        self.passwordInput.setText(password)

    def save_password(self):
        service = self.serviceInput.text().strip()
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text().strip()

        if not service or not username or not password:
            QMessageBox.warning(self, 'Input Error', 'All fields must be filled.')
            return

        encrypted_password = encrypt_password(password)

        conn = sqlite3.connect('password_manager.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)', (service, username, encrypted_password))
            conn.commit()
            QMessageBox.information(self, 'Success', 'Password saved successfully!')
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Duplicate Error', 'Service already exists. Please use a different service name or update the existing one.')
        finally:
            conn.close()

        self.load_accounts()

    def analyze_password(self):
        password = self.passwordInput.text().strip()
        if not password:
            QMessageBox.warning(self, 'Input Error', 'Password field must be filled.')
            return

        analysis = analyze_password(password)
        self.analysisOutput.setText(analysis)

    def load_accounts(self):
        self.accountsList.clear()
        conn = sqlite3.connect('password_manager.db')
        c = conn.cursor()
        c.execute('SELECT service FROM passwords')
        services = c.fetchall()
        conn.close()

        for service in services:
            self.accountsList.addItem(service[0])

    def load_account_details(self, item):
        service = item.text()
        print(f"Selected service: {service}")  # Debug message
        conn = sqlite3.connect('password_manager.db')
        c = conn.cursor()
        c.execute('SELECT username, password FROM passwords WHERE service = ?', (service,))
        account = c.fetchone()
        conn.close()

        if account:
            username, encrypted_password = account
            print(f"Username: {username}, Encrypted Password: {encrypted_password}")  # Debug message
            try:
                password = decrypt_password(encrypted_password)
                print(f"Decrypted Password: {password}")  # Debug message
                self.serviceInput.setText(service)
                self.usernameInput.setText(username)
                self.passwordInput.setText(password)
            except Exception as e:
                print(f"Decryption error: {e}")  # Debug message
                QMessageBox.warning(self, 'Decryption Error', f'Failed to decrypt password: {str(e)}')

if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    manager = PasswordManager()
    manager.show()
    sys.exit(app.exec_())
