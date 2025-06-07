import sys
import os
import sys
import os
import time
import soundfile as sf
import sys
import os
import time
import soundfile as sf
import numpy as np
import cv2
import stepic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                           QTabWidget, QFileDialog, QMessageBox, QGroupBox,
                           QFrame, QSplitter, QTextEdit, QDialog, QComboBox,
                           QProgressBar, QScrollArea)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor, QPalette, QCursor, QImage
from cryptography.fernet import Fernet
from PIL import Image, UnidentifiedImageError
import stepic  # For image steganography

# Function to convert PIL Image to QPixmap
def pil2pixmap(pil_image):
    # Convert the PIL image to RGB mode if it's not already
    if pil_image.mode != "RGB" and pil_image.mode != "RGBA":
        pil_image = pil_image.convert("RGB")
    
    # Get image dimensions
    width, height = pil_image.size
    
    # Convert to QImage format based on image mode
    if pil_image.mode == "RGB":
        # Convert PIL image to QImage (RGB format)
        data = pil_image.tobytes("raw", "RGB")
        qimage = QImage(data, width, height, width * 3, QImage.Format_RGB888)
    else:  # RGBA
        data = pil_image.tobytes("raw", "RGBA")
        qimage = QImage(data, width, height, width * 4, QImage.Format_RGBA8888)
    
    # Convert QImage to QPixmap
    return QPixmap.fromImage(qimage)

import stepic
import soundfile as sf
import numpy as np
import cv2
import time
#import qss_resources  # Will create this resource file later

class SteganographyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Global variables
        self.key_file_path = ""
        self.image_file_path = ""
        self.audio_file_path = ""
        self.video_file_path = ""
        
        # Set the global stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0e17;
                color: #e0e0e0;
            }
            
            #titleFrame {
                background-color: #1a1f2c;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 5px;
            }
            
            #titleLabel {
                color: #00e5ff;
                font-size: 36px;
                font-weight: bold;
                font-family: 'Orbitron', sans-serif;
                letter-spacing: 2px;
            }
            
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            
            QPushButton:hover {
                background-color: #0d8bf2;
                border: 2px solid #2196f3;
            }
            
            QPushButton:pressed {
                background-color: #0b7ad1;
            }
            
            #actionButton {
                background-color: #00bcd4;
                font-size: 16px;
                font-weight: bold;
            }
            
            #actionButton:hover {
                background-color: #00acc1;
                border: 2px solid #00bcd4;
            }
            
            #actionButton:pressed {
                background-color: #0097a7;
            }
            
            QLineEdit {
                background-color: #1d2334;
                border: 1px solid #2d3446;
                border-radius: 4px;
                padding: 8px;
                color: #e0e0e0;
                selection-background-color: #2196f3;
            }
            
            QGroupBox {
                border: 1px solid #2d3446;
                border-radius: 4px;
                margin-top: 1em;
                padding-top: 10px;
                font-weight: bold;
                color: #e0e0e0;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            
            QProgressBar {
                border: 1px solid #2d3446;
                border-radius: 4px;
                background-color: #1d2334;
                text-align: center;
                color: white;
            }
            
            QProgressBar::chunk {
                background-color: #00e5ff;
                width: 10px;
                margin: 0px;
            }
            
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
            }
            
            #statusBar {
                background-color: #1a1f2c;
                color: #7a8292;
            }
        """)
        
        self.init_ui()
        
    def init_ui(self):
        # Main window setup
        self.setWindowTitle("NexusCipher - Futuristic Steganography Tool")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 700)
        
        # Apply futuristic theme
        self.setup_theme()
        
        # Main widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title area
        title_frame = QFrame()
        title_frame.setObjectName("titleFrame")
        title_layout = QHBoxLayout(title_frame)
        
        title_label = QLabel("NEXUS CIPHER")
        title_label.setObjectName("titleLabel")
        title_layout.addWidget(title_label)
        
        main_layout.addWidget(title_frame)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("mainTabs")
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.setup_key_tab()
        self.setup_text_tabs()
        self.setup_image_tabs()
        self.setup_audio_tabs()
        self.setup_video_tabs()
        
        # Status bar
        self.statusBar().showMessage("Ready")
        self.statusBar().setObjectName("statusBar")
        
    def setup_theme(self):
        """Set up the futuristic theme for the application"""
        # Set the application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0e17;
                color: #e0e0e0;
            }
            
            #titleFrame {
                background-color: #1a1f2c;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 5px;
            }
            
            #titleLabel {
                color: #00e5ff;
                font-size: 36px;
                font-weight: bold;
                font-family: 'Orbitron', sans-serif;
                letter-spacing: 2px;
            }
            
            QTabWidget::pane {
                border: 1px solid #2d3446;
                background-color: #151b2a;
                border-radius: 6px;
            }
            
            QTabBar::tab {
                background-color: #1a1f2c;
                color: #7a8292;
                padding: 10px 20px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background-color: #151b2a;
                color: #00e5ff;
                border-bottom: 2px solid #00e5ff;
            }
            
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
            }
            
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            
            QPushButton:hover {
                background-color: #0d8bf2;
                border: 2px solid #2196f3;
            }
            
            QPushButton:pressed {
                background-color: #0b7ad1;
            }
            
            #actionButton {
                background-color: #00bcd4;
                font-size: 16px;
                font-weight: bold;
            }
            
            #actionButton:hover {
                background-color: #00acc1;
                border: 2px solid #00bcd4;
            }
            
            #actionButton:pressed {
                background-color: #0097a7;
            }
            
            QLineEdit {
                background-color: #1d2334;
                border: 1px solid #2d3446;
                border-radius: 4px;
                padding: 8px;
                color: #e0e0e0;
                selection-background-color: #2196f3;
            }
            
            QGroupBox {
                border: 1px solid #2d3446;
                border-radius: 4px;
                margin-top: 1em;
                padding-top: 10px;
                font-weight: bold;
                color: #e0e0e0;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            
            QProgressBar {
                border: 1px solid #2d3446;
                border-radius: 4px;
                background-color: #1d2334;
                text-align: center;
                color: white;
            }
            
            QProgressBar::chunk {
                background-color: #00e5ff;
                width: 10px;
                margin: 0px;
            }
            
            #statusBar {
                background-color: #1a1f2c;
                color: #7a8292;
            }
        """) 

    def setup_key_tab(self):
        """Create the key management tab"""
        key_tab = QWidget()
        key_layout = QVBoxLayout(key_tab)
        key_layout.setAlignment(Qt.AlignCenter)
        key_layout.setSpacing(20)
        
        # Logo or image
        key_icon = QLabel()
        key_icon.setPixmap(QPixmap("key_icon.png") if os.path.exists("key_icon.png") else self.create_key_icon())
        key_icon.setAlignment(Qt.AlignCenter)
        key_layout.addWidget(key_icon)
        
        # Title
        title_label = QLabel("Key Management")
        title_label.setObjectName("sectionTitle")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; color: #00e5ff; margin: 10px;")
        key_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("Generate and manage encryption keys for secure steganography.")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        key_layout.addWidget(desc_label)
        
        # Key actions group
        key_group = QGroupBox("Key Operations")
        key_group.setObjectName("keyGroup")
        key_group_layout = QVBoxLayout(key_group)
        key_group_layout.setSpacing(15)
        
        # Create key button with glow effect
        create_key_btn = QPushButton("Generate New Key")
        create_key_btn.setObjectName("primaryButton")
        create_key_btn.setMinimumHeight(50)
        create_key_btn.clicked.connect(self.create_key)
        key_group_layout.addWidget(create_key_btn)
        
        # Key selection
        select_key_layout = QHBoxLayout()
        self.key_path_display = QLineEdit()
        self.key_path_display.setReadOnly(True)
        self.key_path_display.setPlaceholderText("No key selected")
        
        select_key_btn = QPushButton("Select Key File")
        select_key_btn.clicked.connect(self.select_key)
        
        select_key_layout.addWidget(self.key_path_display, 7)
        select_key_layout.addWidget(select_key_btn, 3)
        key_group_layout.addLayout(select_key_layout)
        
        # Status indicator for key
        self.key_status = QLabel("No key loaded")
        self.key_status.setAlignment(Qt.AlignCenter)
        self.key_status.setStyleSheet("color: #ff5252;")
        key_group_layout.addWidget(self.key_status)
        
        key_layout.addWidget(key_group)
        
        # Add spacer
        key_layout.addStretch()
        
        # Add tab
        self.tab_widget.addTab(key_tab, "Key Management")
    
    def create_key_icon(self):
        """Create a key icon if none exists"""
        # Creating a blank pixmap for the key icon
        pixmap = QPixmap(128, 128)
        pixmap.fill(Qt.transparent)
        return pixmap
    
    def create_key(self):
        """Create a new encryption key"""
        try:
            key = Fernet.generate_key()
            
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save Key File", "", "Key Files (*.key)"
            )
            
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(key)
                
                self.key_file_path = save_path
                self.key_path_display.setText(save_path)
                self.key_status.setText("Key loaded successfully")
                self.key_status.setStyleSheet("color: #4caf50;")
                
                # Show success animation
                self.show_success_message(f"Key saved to {save_path}")
                self.statusBar().showMessage(f"Key generated and saved to {save_path}")
        except Exception as e:
            self.show_error_message(f"Error creating key: {str(e)}")
    
    def select_key(self):
        """Select an existing encryption key"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Key File", "", "Key Files (*.key)"
            )
            
            if file_path:
                self.key_file_path = file_path
                self.key_path_display.setText(file_path)
                self.key_status.setText("Key loaded successfully")
                self.key_status.setStyleSheet("color: #4caf50;")
                self.statusBar().showMessage(f"Key loaded from {file_path}")
        except Exception as e:
            self.show_error_message(f"Error selecting key: {str(e)}")
    
    def show_success_message(self, message):
        """Show a success message popup"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #151b2a;
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }
        """)
        msg_box.exec_()
    
    def show_error_message(self, message):
        """Show an error message popup"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #151b2a;
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }
        """)
        msg_box.exec_()

    def setup_text_tabs(self):
        """Create tabs for text encryption and decryption"""
        # Text Encryption Tab
        text_encrypt_tab = QWidget()
        text_encrypt_layout = QVBoxLayout(text_encrypt_tab)
        text_encrypt_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Text Encryption")
        title_label.setObjectName("sectionTitle")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; color: #00e5ff; margin: 10px;")
        text_encrypt_layout.addWidget(title_label)
        
        # Main content in a cyberpunk card
        content_frame = QFrame()
        content_frame.setObjectName("contentCard")
        content_frame.setStyleSheet("""
            #contentCard {
                background-color: #1a2035;
                border-radius: 8px;
                border: 1px solid #2d3446;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        # Text input area
        input_group = QGroupBox("Enter Text to Encrypt")
        input_group_layout = QVBoxLayout(input_group)
        
        self.text_encrypt_input = QTextEdit()
        self.text_encrypt_input.setPlaceholderText("Enter your message here...")
        self.text_encrypt_input.setMinimumHeight(100)
        input_group_layout.addWidget(self.text_encrypt_input)
        
        content_layout.addWidget(input_group)
        
        # Key selection
        key_layout = QHBoxLayout()
        key_label = QLabel("Encryption Key:")
        
        self.encrypt_key_display = QLineEdit()
        self.encrypt_key_display.setReadOnly(True)
        self.encrypt_key_display.setPlaceholderText("No key selected")
        
        select_key_btn = QPushButton("Select Key")
        select_key_btn.clicked.connect(lambda: self.select_key_for_field(self.encrypt_key_display))
        
        key_layout.addWidget(key_label)
        key_layout.addWidget(self.encrypt_key_display, 7)
        key_layout.addWidget(select_key_btn, 3)
        
        content_layout.addLayout(key_layout)
        
        # Output area
        output_group = QGroupBox("Encrypted Output")
        output_group_layout = QVBoxLayout(output_group)
        
        self.text_encrypt_output = QTextEdit()
        self.text_encrypt_output.setReadOnly(True)
        self.text_encrypt_output.setPlaceholderText("Encrypted text will appear here...")
        self.text_encrypt_output.setMinimumHeight(100)
        output_group_layout.addWidget(self.text_encrypt_output)
        
        # Copy button
        copy_btn = QPushButton("Copy to Clipboard")
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(self.text_encrypt_output.toPlainText()))
        output_group_layout.addWidget(copy_btn)
        
        content_layout.addWidget(output_group)
        
        # Action button with glow effect
        encrypt_btn = QPushButton("Encrypt Text")
        self.setup_button_style(encrypt_btn, is_action_button=True)
        encrypt_btn.clicked.connect(self.encrypt_text)
        content_layout.addWidget(encrypt_btn)
        
        text_encrypt_layout.addWidget(content_frame)
        
        # Add spacer
        text_encrypt_layout.addStretch()
        
        # Text Decryption Tab
        text_decrypt_tab = QWidget()
        text_decrypt_layout = QVBoxLayout(text_decrypt_tab)
        text_decrypt_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Text Decryption")
        title_label.setObjectName("sectionTitle")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; color: #00e5ff; margin: 10px;")
        text_decrypt_layout.addWidget(title_label)
        
        # Main content in a cyberpunk card
        decrypt_content_frame = QFrame()
        decrypt_content_frame.setObjectName("contentCard")
        decrypt_content_frame.setStyleSheet("""
            #contentCard {
                background-color: #1a2035;
                border-radius: 8px;
                border: 1px solid #2d3446;
            }
        """)
        decrypt_content_layout = QVBoxLayout(decrypt_content_frame)
        decrypt_content_layout.setContentsMargins(20, 20, 20, 20)
        decrypt_content_layout.setSpacing(15)
        
        # Text input area
        decrypt_input_group = QGroupBox("Enter Encrypted Text")
        decrypt_input_group_layout = QVBoxLayout(decrypt_input_group)
        
        self.text_decrypt_input = QTextEdit()
        self.text_decrypt_input.setPlaceholderText("Paste encrypted text here...")
        self.text_decrypt_input.setMinimumHeight(100)
        decrypt_input_group_layout.addWidget(self.text_decrypt_input)
        
        decrypt_content_layout.addWidget(decrypt_input_group)
        
        # Key selection
        decrypt_key_layout = QHBoxLayout()
        decrypt_key_label = QLabel("Decryption Key:")
        
        self.decrypt_key_display = QLineEdit()
        self.decrypt_key_display.setReadOnly(True)
        self.decrypt_key_display.setPlaceholderText("No key selected")
        
        decrypt_select_key_btn = QPushButton("Select Key")
        decrypt_select_key_btn.clicked.connect(lambda: self.select_key_for_field(self.decrypt_key_display))
        
        decrypt_key_layout.addWidget(decrypt_key_label)
        decrypt_key_layout.addWidget(self.decrypt_key_display, 7)
        decrypt_key_layout.addWidget(decrypt_select_key_btn, 3)
        
        decrypt_content_layout.addLayout(decrypt_key_layout)
        
        # Output area
        decrypt_output_group = QGroupBox("Decrypted Output")
        decrypt_output_group_layout = QVBoxLayout(decrypt_output_group)
        
        self.text_decrypt_output = QTextEdit()
        self.text_decrypt_output.setReadOnly(True)
        self.text_decrypt_output.setPlaceholderText("Decrypted text will appear here...")
        self.text_decrypt_output.setMinimumHeight(100)
        decrypt_output_group_layout.addWidget(self.text_decrypt_output)
        
        decrypt_content_layout.addWidget(decrypt_output_group)
        
        # Action button with glow effect
        decrypt_btn = QPushButton("Decrypt Text")
        self.setup_button_style(decrypt_btn, is_action_button=True)
        decrypt_btn.clicked.connect(self.decrypt_text)
        decrypt_content_layout.addWidget(decrypt_btn)
        
        text_decrypt_layout.addWidget(decrypt_content_frame)
        
        # Add spacer
        text_decrypt_layout.addStretch()
        
        # Add tabs
        self.tab_widget.addTab(text_encrypt_tab, "Text Encryption")
        self.tab_widget.addTab(text_decrypt_tab, "Text Decryption")
    
    def select_key_for_field(self, field):
        """Select key and update the specified field"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Key File", "", "Key Files (*.key)"
            )
            
            if file_path:
                self.key_file_path = file_path
                field.setText(file_path)
                self.statusBar().showMessage(f"Key loaded from {file_path}")
        except Exception as e:
            self.show_error_message(f"Error selecting key: {str(e)}")
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.statusBar().showMessage("Copied to clipboard")
    
    def encrypt_text(self):
        """Encrypt the text"""
        try:
            text = self.text_encrypt_input.toPlainText()
            key_path = self.encrypt_key_display.text()
            
            if not text:
                self.show_error_message("Please enter text to encrypt")
                return
                
            if not key_path:
                self.show_error_message("Please select a key file")
                return
            
            with open(key_path, "rb") as file:
                key = file.read()
            
            fernet = Fernet(key)
            encrypted_text = fernet.encrypt(text.encode())
            
            self.text_encrypt_output.setText(encrypted_text.decode())
            self.statusBar().showMessage("Text encrypted successfully")
            
        except Exception as e:
            self.show_error_message(f"Error encrypting text: {str(e)}")
    
    def decrypt_text(self):
        """Decrypt the text"""
        try:
            encrypted_text = self.text_decrypt_input.toPlainText()
            key_path = self.decrypt_key_display.text()
            
            if not encrypted_text:
                self.show_error_message("Please enter encrypted text")
                return
                
            if not key_path:
                self.show_error_message("Please select a key file")
                return
            
            with open(key_path, "rb") as file:
                key = file.read()
            
            fernet = Fernet(key)
            decrypted_text = fernet.decrypt(encrypted_text.encode()).decode()
            
            self.text_decrypt_output.setText(decrypted_text)
            self.statusBar().showMessage("Text decrypted successfully")
            
        except Exception as e:
            self.show_error_message(f"Error decrypting text: {str(e)}")

    def setup_image_tabs(self):
        """Create tabs for image steganography"""
        # Image Encryption Tab
        image_encrypt_tab = QWidget()
        image_encrypt_layout = QVBoxLayout(image_encrypt_tab)
        image_encrypt_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Image Steganography - Hide")
        title_label.setObjectName("sectionTitle")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; color: #00e5ff; margin: 10px;")
        image_encrypt_layout.addWidget(title_label)
        
        # Image selection and preview
        image_selection_frame = QFrame()
        image_selection_frame.setObjectName("contentCard")
        image_selection_frame.setStyleSheet("""
            #contentCard {
                background-color: #1a2035;
                border-radius: 8px;
                border: 1px solid #2d3446;
            }
        """)
        
        image_selection_layout = QHBoxLayout(image_selection_frame)
        
        # Left panel - Image selection
        left_panel = QVBoxLayout()
        
        # Image selection
        image_group = QGroupBox("Carrier Image")
        image_group_layout = QVBoxLayout(image_group)
        
        select_image_btn = QPushButton("Select Image")
        select_image_btn.clicked.connect(lambda: self.select_image(self.image_encrypt_preview))
        image_group_layout.addWidget(select_image_btn)
        
        # Image info
        self.image_info_label = QLabel("No image selected")
        image_group_layout.addWidget(self.image_info_label)
        
        left_panel.addWidget(image_group)
        
        # Key selection
        key_group = QGroupBox("Encryption Key")
        key_group_layout = QVBoxLayout(key_group)
        
        self.image_encrypt_key_display = QLineEdit()
        self.image_encrypt_key_display.setReadOnly(True)
        self.image_encrypt_key_display.setPlaceholderText("No key selected")
        
        select_key_btn = QPushButton("Select Key")
        select_key_btn.clicked.connect(lambda: self.select_key_for_field(self.image_encrypt_key_display))
        
        key_group_layout.addWidget(self.image_encrypt_key_display)
        key_group_layout.addWidget(select_key_btn)
        
        left_panel.addWidget(key_group)
        
        # Text to hide
        text_group = QGroupBox("Text to Hide")
        text_group_layout = QVBoxLayout(text_group)
        
        self.image_encrypt_text = QTextEdit()
        self.image_encrypt_text.setPlaceholderText("Enter secret message to hide in the image...")
        text_group_layout.addWidget(self.image_encrypt_text)
        
        left_panel.addWidget(text_group)
        
        image_selection_layout.addLayout(left_panel, 1)
        
        # Right panel - Image preview
        right_panel = QVBoxLayout()
        
        preview_group = QGroupBox("Image Preview")
        preview_group_layout = QVBoxLayout(preview_group)
        
        self.image_encrypt_preview = QLabel("Select an image to preview")
        self.image_encrypt_preview.setAlignment(Qt.AlignCenter)
        self.image_encrypt_preview.setMinimumSize(300, 300)
        self.image_encrypt_preview.setMaximumSize(400, 400)
        self.image_encrypt_preview.setStyleSheet("border: 1px dashed #2d3446;")
        preview_group_layout.addWidget(self.image_encrypt_preview)
        
        right_panel.addWidget(preview_group)
        
        # Process status
        self.image_encrypt_status = QProgressBar()
        self.image_encrypt_status.setRange(0, 100)
        self.image_encrypt_status.setValue(0)
        self.image_encrypt_status.setTextVisible(False)
        right_panel.addWidget(self.image_encrypt_status)
        
        # Action button
        hide_btn = QPushButton("Hide Message in Image")
        self.setup_button_style(hide_btn, is_action_button=True)
        hide_btn.clicked.connect(self.hide_in_image)
        right_panel.addWidget(hide_btn)
        
        image_selection_layout.addLayout(right_panel, 1)
        
        image_encrypt_layout.addWidget(image_selection_frame)
        
        # Add spacer
        image_encrypt_layout.addStretch()
        
        # Image Decryption Tab
        image_decrypt_tab = QWidget()
        image_decrypt_layout = QVBoxLayout(image_decrypt_tab)
        image_decrypt_layout.setSpacing(20)
        
        # Title
        decrypt_title_label = QLabel("Image Steganography - Reveal")
        decrypt_title_label.setObjectName("sectionTitle")
        decrypt_title_label.setAlignment(Qt.AlignCenter)
        decrypt_title_label.setStyleSheet("font-size: 24px; color: #00e5ff; margin: 10px;")
        image_decrypt_layout.addWidget(decrypt_title_label)
        
        # Image selection and preview
        image_decrypt_frame = QFrame()
        image_decrypt_frame.setObjectName("contentCard")
        image_decrypt_frame.setStyleSheet("""
            #contentCard {
                background-color: #1a2035;
                border-radius: 8px;
                border: 1px solid #2d3446;
            }
        """)
        
        image_decrypt_layout_frame = QHBoxLayout(image_decrypt_frame)
        
        # Left panel - Image selection
        decrypt_left_panel = QVBoxLayout()
        
        # Image selection
        decrypt_image_group = QGroupBox("Encrypted Image")
        decrypt_image_group_layout = QVBoxLayout(decrypt_image_group)
        
        decrypt_select_image_btn = QPushButton("Select Image")
        decrypt_select_image_btn.clicked.connect(lambda: self.select_image(self.image_decrypt_preview))
        decrypt_image_group_layout.addWidget(decrypt_select_image_btn)
        
        # Image info
        self.decrypt_image_info_label = QLabel("No image selected")
        decrypt_image_group_layout.addWidget(self.decrypt_image_info_label)
        
        decrypt_left_panel.addWidget(decrypt_image_group)
        
        # Key selection
        decrypt_key_group = QGroupBox("Decryption Key")
        decrypt_key_group_layout = QVBoxLayout(decrypt_key_group)
        
        self.image_decrypt_key_display = QLineEdit()
        self.image_decrypt_key_display.setReadOnly(True)
        self.image_decrypt_key_display.setPlaceholderText("No key selected")
        
        decrypt_select_key_btn = QPushButton("Select Key")
        decrypt_select_key_btn.clicked.connect(lambda: self.select_key_for_field(self.image_decrypt_key_display))
        
        decrypt_key_group_layout.addWidget(self.image_decrypt_key_display)
        decrypt_key_group_layout.addWidget(decrypt_select_key_btn)
        
        decrypt_left_panel.addWidget(decrypt_key_group)
        
        image_decrypt_layout_frame.addLayout(decrypt_left_panel, 1)
        
        # Right panel - Image preview and decrypted text
        decrypt_right_panel = QVBoxLayout()
        
        # Image preview
        decrypt_preview_group = QGroupBox("Image Preview")
        decrypt_preview_group_layout = QVBoxLayout(decrypt_preview_group)
        
        self.image_decrypt_preview = QLabel("Select an image to preview")
        self.image_decrypt_preview.setAlignment(Qt.AlignCenter)
        self.image_decrypt_preview.setMinimumSize(300, 300)
        self.image_decrypt_preview.setMaximumSize(400, 400)
        self.image_decrypt_preview.setStyleSheet("border: 1px dashed #2d3446;")
        decrypt_preview_group_layout.addWidget(self.image_decrypt_preview)
        
        decrypt_right_panel.addWidget(decrypt_preview_group)
        
        # Decrypted text
        decrypt_text_group = QGroupBox("Revealed Message")
        decrypt_text_group_layout = QVBoxLayout(decrypt_text_group)
        
        self.image_decrypt_text = QTextEdit()
        self.image_decrypt_text.setReadOnly(True)
        self.image_decrypt_text.setPlaceholderText("Revealed message will appear here...")
        decrypt_text_group_layout.addWidget(self.image_decrypt_text)
        
        decrypt_right_panel.addWidget(decrypt_text_group)
        
        # Process status
        self.image_decrypt_status = QProgressBar()
        self.image_decrypt_status.setRange(0, 100)
        self.image_decrypt_status.setValue(0)
        self.image_decrypt_status.setTextVisible(False)
        decrypt_right_panel.addWidget(self.image_decrypt_status)
        
        # Action button
        reveal_btn = QPushButton("Reveal Hidden Message")
        self.setup_button_style(reveal_btn, is_action_button=True)
        reveal_btn.clicked.connect(self.unhide_from_image)
        decrypt_right_panel.addWidget(reveal_btn)
        
        image_decrypt_layout_frame.addLayout(decrypt_right_panel, 1)
        
        image_decrypt_layout.addWidget(image_decrypt_frame)
        
        # Add spacer
        image_decrypt_layout.addStretch()
        
        # Add tabs
        self.tab_widget.addTab(image_encrypt_tab, "Hide in Image")
        self.tab_widget.addTab(image_decrypt_tab, "Extract from Image")
    
    def select_image(self, preview_label):
        """Select an image file and update the preview"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
            )
            
            if file_path:
                self.image_file_path = file_path
                
                # Update image info label based on which tab is active
                if preview_label == self.image_encrypt_preview:
                    self.image_info_label.setText(f"Selected: {os.path.basename(file_path)}")
                else:
                    self.decrypt_image_info_label.setText(f"Selected: {os.path.basename(file_path)}")
                
                # Load and display image preview
                image = Image.open(file_path)
                image.thumbnail((350, 350))
                
                # Convert PIL image to QPixmap for display
                pixmap = pil2pixmap(image)
                
                preview_label.setPixmap(pixmap)
                preview_label.setAlignment(Qt.AlignCenter)
                
                self.statusBar().showMessage(f"Image loaded: {file_path}")
                
        except UnidentifiedImageError:
            self.show_error_message("Invalid image file")
        except Exception as e:
            self.show_error_message(f"Error selecting image: {str(e)}")
    
    def hide_in_image(self):
        """Hide an encrypted message in an image"""
        try:
            if not self.image_encrypt_text.toPlainText():
                self.show_error_message("Please enter text to hide")
                return
                
            if not self.image_file_path:
                self.show_error_message("Please select an image")
                return
                
            if not self.image_encrypt_key_display.text():
                self.show_error_message("Please select a key file")
                return
            
            # Show progress
            self.image_encrypt_status.setValue(25)
            QApplication.processEvents()
            
            # Read encryption key
            with open(self.image_encrypt_key_display.text(), "rb") as file:
                key = file.read()
            
            fernet = Fernet(key)
            encrypted_message = fernet.encrypt(self.image_encrypt_text.toPlainText().encode())
            
            # Update progress
            self.image_encrypt_status.setValue(50)
            QApplication.processEvents()
            
            # Load image and embed message
            img = Image.open(self.image_file_path)
            encoded_image = stepic.encode(img, encrypted_message)
            
            # Update progress
            self.image_encrypt_status.setValue(75)
            QApplication.processEvents()
            
            # Save the encoded image
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save Encoded Image", "", "PNG files (*.png)"
            )
            
            if save_path:
                encoded_image.save(save_path)
                
                # Update progress
                self.image_encrypt_status.setValue(100)
                QApplication.processEvents()
                
                self.show_success_message(f"Message hidden in {os.path.basename(save_path)}")
                self.statusBar().showMessage(f"Message hidden in image and saved to {save_path}")
                
                # Reset progress after a delay
                QApplication.processEvents()
                time.sleep(1)
                self.image_encrypt_status.setValue(0)
            else:
                self.image_encrypt_status.setValue(0)
                
        except Exception as e:
            self.image_encrypt_status.setValue(0)
            self.show_error_message(f"Error hiding message in image: {str(e)}")
    
    def unhide_from_image(self):
        """Reveal and decrypt a hidden message from an image"""
        try:
            if not self.image_file_path:
                self.show_error_message("Please select an image")
                return
                
            if not self.image_decrypt_key_display.text():
                self.show_error_message("Please select a key file")
                return
            
            # Show progress
            self.image_decrypt_status.setValue(25)
            QApplication.processEvents()
            
            # Load image and extract message
            image = Image.open(self.image_file_path)
            encrypted_text = stepic.decode(image)
            
            # Update progress
            self.image_decrypt_status.setValue(50)
            QApplication.processEvents()
            
            # Read decryption key
            with open(self.image_decrypt_key_display.text(), "rb") as file:
                key = file.read()
            
            # Update progress
            self.image_decrypt_status.setValue(75)
            QApplication.processEvents()
            
            # Decrypt the message
            fernet = Fernet(key)
            decrypted_text = fernet.decrypt(encrypted_text).decode()
            
            # Display the decrypted message
            self.image_decrypt_text.setText(decrypted_text)
            
            # Update progress
            self.image_decrypt_status.setValue(100)
            QApplication.processEvents()
            
            self.statusBar().showMessage("Message extracted and decrypted successfully")
            
            # Reset progress after a delay
            QApplication.processEvents()
            time.sleep(1)
            self.image_decrypt_status.setValue(0)
            
        except Exception as e:
            self.image_decrypt_status.setValue(0)
            self.show_error_message(f"Error extracting message from image: {str(e)}")

    def setup_audio_tabs(self):
        """Create tabs for audio steganography"""
        # Audio Encryption Tab
        audio_encrypt_tab = QWidget()
        audio_encrypt_layout = QVBoxLayout(audio_encrypt_tab)
        audio_encrypt_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Audio Steganography - Hide")
        title_label.setObjectName("sectionTitle")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; color: #00e5ff; margin: 10px;")
        audio_encrypt_layout.addWidget(title_label)
        
        # Main content frame
        audio_content_frame = QFrame()
        audio_content_frame.setObjectName("contentCard")
        audio_content_frame.setStyleSheet("""
            #contentCard {
                background-color: #1a2035;
                border-radius: 8px;
                border: 1px solid #2d3446;
            }
        """)
        audio_content_layout = QVBoxLayout(audio_content_frame)
        audio_content_layout.setContentsMargins(20, 20, 20, 20)
        audio_content_layout.setSpacing(15)
        
        # Audio selection 
        audio_select_group = QGroupBox("Select Audio File")
        audio_select_layout = QHBoxLayout(audio_select_group)
        
        self.audio_encrypt_path = QLineEdit()
        self.audio_encrypt_path.setReadOnly(True)
        self.audio_encrypt_path.setPlaceholderText("No audio file selected")
        
        select_audio_btn = QPushButton("Browse")
        select_audio_btn.clicked.connect(lambda: self.select_audio(self.audio_encrypt_path))
        
        audio_info_layout = QVBoxLayout()
        audio_info_layout.addWidget(self.audio_encrypt_path)
        
        self.audio_encrypt_info = QLabel("No audio file selected")
        audio_info_layout.addWidget(self.audio_encrypt_info)
        
        audio_select_layout.addLayout(audio_info_layout, 7)
        audio_select_layout.addWidget(select_audio_btn, 3)
        
        audio_content_layout.addWidget(audio_select_group)
        
        # Text to hide
        audio_text_group = QGroupBox("Message to Hide")
        audio_text_layout = QVBoxLayout(audio_text_group)
        
        self.audio_encrypt_text = QTextEdit()
        self.audio_encrypt_text.setPlaceholderText("Enter secret message to hide in the audio...")
        self.audio_encrypt_text.setMinimumHeight(100)
        audio_text_layout.addWidget(self.audio_encrypt_text)
        
        audio_content_layout.addWidget(audio_text_group)
        
        # Key selection
        audio_key_group = QGroupBox("Encryption Key")
        audio_key_layout = QHBoxLayout(audio_key_group)
        
        self.audio_encrypt_key = QLineEdit()
        self.audio_encrypt_key.setReadOnly(True)
        self.audio_encrypt_key.setPlaceholderText("No key selected")
        
        audio_select_key_btn = QPushButton("Select Key")
        audio_select_key_btn.clicked.connect(lambda: self.select_key_for_field(self.audio_encrypt_key))
        
        audio_key_layout.addWidget(self.audio_encrypt_key, 7)
        audio_key_layout.addWidget(audio_select_key_btn, 3)
        
        audio_content_layout.addWidget(audio_key_group)
        
        # Progress bar
        self.audio_encrypt_progress = QProgressBar()
        self.audio_encrypt_progress.setRange(0, 100)
        self.audio_encrypt_progress.setValue(0)
        self.audio_encrypt_progress.setTextVisible(True)
        self.audio_encrypt_progress.setFormat("Ready")
        audio_content_layout.addWidget(self.audio_encrypt_progress)
        
        # Hide button with futuristic design
        hide_audio_btn = QPushButton("Hide Message in Audio")
        self.setup_button_style(hide_audio_btn, is_action_button=True)
        hide_audio_btn.clicked.connect(self.hide_in_audio)
        audio_content_layout.addWidget(hide_audio_btn)
        
        audio_encrypt_layout.addWidget(audio_content_frame)
        
        # Add spacer
        audio_encrypt_layout.addStretch()
        
        # Audio Decryption Tab
        audio_decrypt_tab = QWidget()
        audio_decrypt_layout = QVBoxLayout(audio_decrypt_tab)
        audio_decrypt_layout.setSpacing(20)
        
        # Title
        decrypt_title_label = QLabel("Audio Steganography - Reveal")
        decrypt_title_label.setObjectName("sectionTitle")
        decrypt_title_label.setAlignment(Qt.AlignCenter)
        decrypt_title_label.setStyleSheet("font-size: 24px; color: #00e5ff; margin: 10px;")
        audio_decrypt_layout.addWidget(decrypt_title_label)
        
        # Main content frame
        audio_decrypt_frame = QFrame()
        audio_decrypt_frame.setObjectName("contentCard")
        audio_decrypt_frame.setStyleSheet("""
            #contentCard {
                background-color: #1a2035;
                border-radius: 8px;
                border: 1px solid #2d3446;
            }
        """)
        audio_decrypt_layout_inner = QVBoxLayout(audio_decrypt_frame)
        audio_decrypt_layout_inner.setContentsMargins(20, 20, 20, 20)
        audio_decrypt_layout_inner.setSpacing(15)
        
        # Audio selection 
        audio_decrypt_select_group = QGroupBox("Select Encoded Audio File")
        audio_decrypt_select_layout = QHBoxLayout(audio_decrypt_select_group)
        
        self.audio_decrypt_path = QLineEdit()
        self.audio_decrypt_path.setReadOnly(True)
        self.audio_decrypt_path.setPlaceholderText("No audio file selected")
        
        decrypt_select_audio_btn = QPushButton("Browse")
        decrypt_select_audio_btn.clicked.connect(lambda: self.select_audio(self.audio_decrypt_path))
        
        audio_decrypt_info_layout = QVBoxLayout()
        audio_decrypt_info_layout.addWidget(self.audio_decrypt_path)
        
        self.audio_decrypt_info = QLabel("No audio file selected")
        audio_decrypt_info_layout.addWidget(self.audio_decrypt_info)
        
        audio_decrypt_select_layout.addLayout(audio_decrypt_info_layout, 7)
        audio_decrypt_select_layout.addWidget(decrypt_select_audio_btn, 3)
        
        audio_decrypt_layout_inner.addWidget(audio_decrypt_select_group)
        
        # Key selection
        audio_decrypt_key_group = QGroupBox("Decryption Key")
        audio_decrypt_key_layout = QHBoxLayout(audio_decrypt_key_group)
        
        self.audio_decrypt_key = QLineEdit()
        self.audio_decrypt_key.setReadOnly(True)
        self.audio_decrypt_key.setPlaceholderText("No key selected")
        
        audio_decrypt_select_key_btn = QPushButton("Select Key")
        audio_decrypt_select_key_btn.clicked.connect(lambda: self.select_key_for_field(self.audio_decrypt_key))
        
        audio_decrypt_key_layout.addWidget(self.audio_decrypt_key, 7)
        audio_decrypt_key_layout.addWidget(audio_decrypt_select_key_btn, 3)
        
        audio_decrypt_layout_inner.addWidget(audio_decrypt_key_group)
        
        # Extracted message
        extracted_msg_group = QGroupBox("Extracted Message")
        extracted_msg_layout = QVBoxLayout(extracted_msg_group)
        
        self.audio_decrypt_text = QTextEdit()
        self.audio_decrypt_text.setReadOnly(True)
        self.audio_decrypt_text.setPlaceholderText("Extracted message will appear here...")
        self.audio_decrypt_text.setMinimumHeight(100)
        extracted_msg_layout.addWidget(self.audio_decrypt_text)
        
        audio_decrypt_layout_inner.addWidget(extracted_msg_group)
        
        # Progress bar
        self.audio_decrypt_progress = QProgressBar()
        self.audio_decrypt_progress.setRange(0, 100)
        self.audio_decrypt_progress.setValue(0)
        self.audio_decrypt_progress.setTextVisible(True)
        self.audio_decrypt_progress.setFormat("Ready")
        audio_decrypt_layout_inner.addWidget(self.audio_decrypt_progress)
        
        # Extract button
        extract_audio_btn = QPushButton("Extract Hidden Message")
        self.setup_button_style(extract_audio_btn, is_action_button=True)
        extract_audio_btn.clicked.connect(self.unhide_from_audio)
        audio_decrypt_layout_inner.addWidget(extract_audio_btn)
        
        audio_decrypt_layout.addWidget(audio_decrypt_frame)
        
        # Add spacer
        audio_decrypt_layout.addStretch()
        
        # Add tabs
        self.tab_widget.addTab(audio_encrypt_tab, "Hide in Audio")
        self.tab_widget.addTab(audio_decrypt_tab, "Extract from Audio")
    
    def select_audio(self, path_field):
        """Select an audio file"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Audio File", "", 
                "Audio Files (*.wav *.mp3 *.flac *.ogg *.aiff *.au)"
            )
            
            if file_path:
                self.audio_file_path = file_path
                path_field.setText(file_path)
                
                # Update audio info label
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
                
                info_text = f"File: {os.path.basename(file_path)} | Size: {file_size:.2f} MB"
                
                if path_field == self.audio_encrypt_path:
                    self.audio_encrypt_info.setText(info_text)
                else:
                    self.audio_decrypt_info.setText(info_text)
                
                self.statusBar().showMessage(f"Audio file loaded: {file_path}")
        except Exception as e:
            self.show_error_message(f"Error selecting audio file: {str(e)}")
    
    def convert_to_wav(self, input_path, output_path):
        """Convert audio to WAV format if needed"""
        data, samplerate = sf.read(input_path)
        
        # Convert to mono if stereo
        if data.ndim > 1:
            data = data.mean(axis=1)
        
        sf.write(output_path, data, samplerate, subtype='PCM_16')
        return output_path
    
    def hide_in_audio(self):
        """Hide a message in an audio file"""
        try:
            if not self.audio_encrypt_text.toPlainText():
                self.show_error_message("Please enter text to hide")
                return
                
            if not self.audio_file_path:
                self.show_error_message("Please select an audio file")
                return
                
            if not self.audio_encrypt_key.text():
                self.show_error_message("Please select a key file")
                return
            
            # Update progress
            self.audio_encrypt_progress.setValue(10)
            self.audio_encrypt_progress.setFormat("Reading key...")
            QApplication.processEvents()
            
            # Read encryption key
            with open(self.audio_encrypt_key.text(), "rb") as file:
                key = file.read()
            
            fernet = Fernet(key)
            encrypted_message = fernet.encrypt(self.audio_encrypt_text.toPlainText().encode())
            
            # Update progress
            self.audio_encrypt_progress.setValue(25)
            self.audio_encrypt_progress.setFormat("Preparing audio...")
            QApplication.processEvents()
            
            # Convert message to binary bits
            message_bits = ''.join(format(byte, '08b') for byte in encrypted_message)
            message_length = len(message_bits)
            
            # Convert audio to WAV if necessary
            temp_wav_path = self.audio_file_path
            if not temp_wav_path.endswith('.wav'):
                temp_wav_path = os.path.splitext(self.audio_file_path)[0] + '_temp.wav'
                self.convert_to_wav(self.audio_file_path, temp_wav_path)
            
            # Update progress
            self.audio_encrypt_progress.setValue(40)
            self.audio_encrypt_progress.setFormat("Processing audio data...")
            QApplication.processEvents()
            
            # Read audio file
            data, samplerate = sf.read(temp_wav_path, dtype='int16')
            
            # Ensure mono audio for simplicity
            if data.ndim > 1:
                data = data.mean(axis=1).astype('int16')
            
            # Check capacity
            max_capacity = len(data)
            if message_length > max_capacity:
                self.show_error_message("Message is too large to fit in the selected audio file")
                return
            
            # Update progress
            self.audio_encrypt_progress.setValue(60)
            self.audio_encrypt_progress.setFormat("Hiding message...")
            QApplication.processEvents()
            
            # Hide the message in the LSB of audio samples
            modified_data = data.copy()
            bit_index = 0
            for i in range(len(modified_data)):
                if bit_index < message_length:
                    modified_data[i] = (modified_data[i] & ~1) | int(message_bits[bit_index])
                    bit_index += 1
            
            # Update progress
            self.audio_encrypt_progress.setValue(80)
            self.audio_encrypt_progress.setFormat("Saving file...")
            QApplication.processEvents()
            
            # Save modified audio
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save Modified Audio", "", "WAV files (*.wav)"
            )
            
            if save_path:
                sf.write(save_path, modified_data, samplerate)
                
                # Update progress
                self.audio_encrypt_progress.setValue(100)
                self.audio_encrypt_progress.setFormat("Complete!")
                QApplication.processEvents()
                
                # Clean up temp file if needed
                if temp_wav_path != self.audio_file_path and os.path.exists(temp_wav_path):
                    os.remove(temp_wav_path)
                
                self.show_success_message(f"Message hidden in {os.path.basename(save_path)}")
                self.statusBar().showMessage(f"Message hidden in audio and saved to {save_path}")
                
                # Reset progress after a delay
                QApplication.processEvents()
                time.sleep(1)
                self.audio_encrypt_progress.setValue(0)
                self.audio_encrypt_progress.setFormat("Ready")
            else:
                self.audio_encrypt_progress.setValue(0)
                self.audio_encrypt_progress.setFormat("Cancelled")
                
        except Exception as e:
            self.audio_encrypt_progress.setValue(0)
            self.audio_encrypt_progress.setFormat("Error")
            self.show_error_message(f"Error hiding message in audio: {str(e)}")
    
    def unhide_from_audio(self):
        """Extract a hidden message from an audio file"""
        try:
            if not self.audio_file_path:
                self.show_error_message("Please select an audio file")
                return
                
            if not self.audio_decrypt_key.text():
                self.show_error_message("Please select a key file")
                return
            
            # Update progress
            self.audio_decrypt_progress.setValue(20)
            self.audio_decrypt_progress.setFormat("Reading audio data...")
            QApplication.processEvents()
            
            # Read audio file
            data, _ = sf.read(self.audio_file_path)
            
            # Convert to mono if stereo
            if data.ndim > 1:
                data = data.mean(axis=1)
            
            # Update progress
            self.audio_decrypt_progress.setValue(40)
            self.audio_decrypt_progress.setFormat("Extracting data...")
            QApplication.processEvents()
            
            # Extract message bits
            message_bits = ''
            for sample in data:
                # Convert sample to integer and extract LSB
                lsb = int(round(sample * 32767)) & 1
                message_bits += str(lsb)
                if len(message_bits) >= 256 * 8:  # Reasonable max message length
                    break
            
            # Update progress
            self.audio_decrypt_progress.setValue(60)
            self.audio_decrypt_progress.setFormat("Converting to bytes...")
            QApplication.processEvents()
            
            # Convert bits to bytes
            encrypted_bytes = bytes(int(message_bits[i:i+8], 2) for i in range(0, len(message_bits), 8))
            
            # Update progress
            self.audio_decrypt_progress.setValue(80)
            self.audio_decrypt_progress.setFormat("Decrypting message...")
            QApplication.processEvents()
            
            # Decrypt message
            with open(self.audio_decrypt_key.text(), "rb") as file:
                key = file.read()
            
            fernet = Fernet(key)
            decrypted_text = fernet.decrypt(encrypted_bytes).decode()
            
            # Display the decrypted message
            self.audio_decrypt_text.setText(decrypted_text)
            
            self.audio_decrypt_progress.setValue(100)
            self.audio_decrypt_progress.setFormat("Complete!")
            QApplication.processEvents()
            
            self.statusBar().showMessage("Message extracted and decrypted successfully")
            
            # Reset progress after a delay
            QApplication.processEvents()
            time.sleep(1)
            self.audio_decrypt_progress.setValue(0)
            self.audio_decrypt_progress.setFormat("Ready")
            
        except Exception as e:
            self.audio_decrypt_progress.setValue(0)
            self.audio_decrypt_progress.setFormat("Error")
            self.show_error_message(f"Error extracting message from audio: {str(e)}")

    def setup_video_tabs(self):
        """Create tabs for video steganography"""
        # Video Encryption Tab
        video_encrypt_tab = QWidget()
        video_encrypt_layout = QVBoxLayout(video_encrypt_tab)
        video_encrypt_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Video Steganography - Hide")
        title_label.setObjectName("sectionTitle")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; color: #00e5ff; margin: 10px;")
        video_encrypt_layout.addWidget(title_label)
        
        # Main content frame
        video_content_frame = QFrame()
        video_content_frame.setObjectName("contentCard")
        video_content_frame.setStyleSheet("""
            #contentCard {
                background-color: #1a2035;
                border-radius: 8px;
                border: 1px solid #2d3446;
            }
        """)
        video_content_layout = QVBoxLayout(video_content_frame)
        video_content_layout.setContentsMargins(20, 20, 20, 20)
        video_content_layout.setSpacing(15)
        
        # Video selection
        video_select_group = QGroupBox("Select Video File")
        video_select_layout = QHBoxLayout(video_select_group)
        
        self.video_encrypt_path = QLineEdit()
        self.video_encrypt_path.setReadOnly(True)
        self.video_encrypt_path.setPlaceholderText("No video file selected")
        
        select_video_btn = QPushButton("Browse")
        select_video_btn.clicked.connect(lambda: self.select_video(self.video_encrypt_path))
        
        video_info_layout = QVBoxLayout()
        video_info_layout.addWidget(self.video_encrypt_path)
        
        self.video_encrypt_info = QLabel("No video file selected")
        video_info_layout.addWidget(self.video_encrypt_info)
        
        video_select_layout.addLayout(video_info_layout, 7)
        video_select_layout.addWidget(select_video_btn, 3)
        
        video_content_layout.addWidget(video_select_group)
        
        # Text to hide
        video_text_group = QGroupBox("Message to Hide")
        video_text_layout = QVBoxLayout(video_text_group)
        
        self.video_encrypt_text = QTextEdit()
        self.video_encrypt_text.setPlaceholderText("Enter secret message to hide in the video...")
        self.video_encrypt_text.setMinimumHeight(100)
        video_text_layout.addWidget(self.video_encrypt_text)
        
        video_content_layout.addWidget(video_text_group)
        
        # Key selection
        video_key_group = QGroupBox("Encryption Key")
        video_key_layout = QHBoxLayout(video_key_group)
        
        self.video_encrypt_key = QLineEdit()
        self.video_encrypt_key.setReadOnly(True)
        self.video_encrypt_key.setPlaceholderText("No key selected")
        
        video_select_key_btn = QPushButton("Select Key")
        video_select_key_btn.clicked.connect(lambda: self.select_key_for_field(self.video_encrypt_key))
        
        video_key_layout.addWidget(self.video_encrypt_key, 7)
        video_key_layout.addWidget(video_select_key_btn, 3)
        
        video_content_layout.addWidget(video_key_group)
        
        # Progress bar with futuristic design
        self.video_encrypt_progress = QProgressBar()
        self.video_encrypt_progress.setRange(0, 100)
        self.video_encrypt_progress.setValue(0)
        self.video_encrypt_progress.setTextVisible(True)
        self.video_encrypt_progress.setFormat("Ready")
        video_content_layout.addWidget(self.video_encrypt_progress)
        
        # Action button with holographic effect
        hide_video_btn = QPushButton("Hide Message in Video")
        self.setup_button_style(hide_video_btn, is_action_button=True)
        hide_video_btn.clicked.connect(self.hide_in_video)
        video_content_layout.addWidget(hide_video_btn)
        
        video_encrypt_layout.addWidget(video_content_frame)
        
        # Add spacer
        video_encrypt_layout.addStretch()
        
        # Video Decryption Tab
        video_decrypt_tab = QWidget()
        video_decrypt_layout = QVBoxLayout(video_decrypt_tab)
        video_decrypt_layout.setSpacing(20)
        
        # Title
        decrypt_title_label = QLabel("Video Steganography - Reveal")
        decrypt_title_label.setObjectName("sectionTitle")
        decrypt_title_label.setAlignment(Qt.AlignCenter)
        decrypt_title_label.setStyleSheet("font-size: 24px; color: #00e5ff; margin: 10px;")
        video_decrypt_layout.addWidget(decrypt_title_label)
        
        # Main content frame
        video_decrypt_frame = QFrame()
        video_decrypt_frame.setObjectName("contentCard")
        video_decrypt_frame.setStyleSheet("""
            #contentCard {
                background-color: #1a2035;
                border-radius: 8px;
                border: 1px solid #2d3446;
            }
        """)
        video_decrypt_layout_inner = QVBoxLayout(video_decrypt_frame)
        video_decrypt_layout_inner.setContentsMargins(20, 20, 20, 20)
        video_decrypt_layout_inner.setSpacing(15)
        
        # Video selection
        video_decrypt_select_group = QGroupBox("Select Encoded Video")
        video_decrypt_select_layout = QHBoxLayout(video_decrypt_select_group)
        
        self.video_decrypt_path = QLineEdit()
        self.video_decrypt_path.setReadOnly(True)
        self.video_decrypt_path.setPlaceholderText("No video file selected")
        
        decrypt_select_video_btn = QPushButton("Browse")
        decrypt_select_video_btn.clicked.connect(lambda: self.select_video(self.video_decrypt_path))
        
        video_decrypt_info_layout = QVBoxLayout()
        video_decrypt_info_layout.addWidget(self.video_decrypt_path)
        
        self.video_decrypt_info = QLabel("No video file selected")
        video_decrypt_info_layout.addWidget(self.video_decrypt_info)
        
        video_decrypt_select_layout.addLayout(video_decrypt_info_layout, 7)
        video_decrypt_select_layout.addWidget(decrypt_select_video_btn, 3)
        
        video_decrypt_layout_inner.addWidget(video_decrypt_select_group)
        
        # Key selection
        video_decrypt_key_group = QGroupBox("Decryption Key")
        video_decrypt_key_layout = QHBoxLayout(video_decrypt_key_group)
        
        self.video_decrypt_key = QLineEdit()
        self.video_decrypt_key.setReadOnly(True)
        self.video_decrypt_key.setPlaceholderText("No key selected")
        
        video_decrypt_select_key_btn = QPushButton("Select Key")
        video_decrypt_select_key_btn.clicked.connect(lambda: self.select_key_for_field(self.video_decrypt_key))
        
        video_decrypt_key_layout.addWidget(self.video_decrypt_key, 7)
        video_decrypt_key_layout.addWidget(video_decrypt_select_key_btn, 3)
        
        video_decrypt_layout_inner.addWidget(video_decrypt_key_group)
        
        # Extracted message
        extracted_video_msg_group = QGroupBox("Extracted Message")
        extracted_video_msg_layout = QVBoxLayout(extracted_video_msg_group)
        
        self.video_decrypt_text = QTextEdit()
        self.video_decrypt_text.setReadOnly(True)
        self.video_decrypt_text.setPlaceholderText("Extracted message will appear here...")
        self.video_decrypt_text.setMinimumHeight(100)
        extracted_video_msg_layout.addWidget(self.video_decrypt_text)
        
        video_decrypt_layout_inner.addWidget(extracted_video_msg_group)
        
        # Progress bar
        self.video_decrypt_progress = QProgressBar()
        self.video_decrypt_progress.setRange(0, 100)
        self.video_decrypt_progress.setValue(0)
        self.video_decrypt_progress.setTextVisible(True)
        self.video_decrypt_progress.setFormat("Ready")
        video_decrypt_layout_inner.addWidget(self.video_decrypt_progress)
        
        # Extract button
        extract_video_btn = QPushButton("Extract Hidden Message")
        self.setup_button_style(extract_video_btn, is_action_button=True)
        extract_video_btn.clicked.connect(self.unhide_from_video)
        video_decrypt_layout_inner.addWidget(extract_video_btn)
        
        video_decrypt_layout.addWidget(video_decrypt_frame)
        
        # Add spacer
        video_decrypt_layout.addStretch()
        
        # Add tabs
        self.tab_widget.addTab(video_encrypt_tab, "Hide in Video")
        self.tab_widget.addTab(video_decrypt_tab, "Extract from Video")
    
    def select_video(self, path_field):
        """Select a video file"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Video File", "", 
                "Video Files (*.mp4 *.avi *.mov *.mkv)"
            )
            
            if file_path:
                self.video_file_path = file_path
                path_field.setText(file_path)
                
                # Update video info label
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
                
                # Get video duration using OpenCV
                try:
                    cap = cv2.VideoCapture(file_path)
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    duration = frame_count / fps
                    cap.release()
                    
                    info_text = f"File: {os.path.basename(file_path)} | Size: {file_size:.2f} MB | Duration: {duration:.2f} seconds"
                except:
                    info_text = f"File: {os.path.basename(file_path)} | Size: {file_size:.2f} MB"
                
                if path_field == self.video_encrypt_path:
                    self.video_encrypt_info.setText(info_text)
                else:
                    self.video_decrypt_info.setText(info_text)
                
                self.statusBar().showMessage(f"Video file loaded: {file_path}")
        except Exception as e:
            self.show_error_message(f"Error selecting video file: {str(e)}")
    
    def hide_in_video(self):
        """Hide a message in a video file"""
        try:
            if not self.video_encrypt_text.toPlainText():
                self.show_error_message("Please enter text to hide")
                return
                
            if not self.video_file_path:
                self.show_error_message("Please select a video file")
                return
                
            # Note: For a real implementation, you would extract the audio from the video,
            # hide the message in the audio, and then merge it back with the video
            self.video_encrypt_progress.setValue(10)
            self.video_encrypt_progress.setFormat("Extracting audio...")
            QApplication.processEvents()
            
            # In a real implementation, you would use ffmpeg to extract the audio
            # We'll use a placeholder message for demonstration
            self.video_encrypt_progress.setValue(30)
            self.video_encrypt_progress.setFormat("Encrypting message...")
            QApplication.processEvents()
            
            # Read encryption key
            with open(self.video_encrypt_key.text(), "rb") as file:
                key = file.read()
            
            fernet = Fernet(key)
            encrypted_message = fernet.encrypt(self.video_encrypt_text.toPlainText().encode())
            
            self.video_encrypt_progress.setValue(50)
            self.video_encrypt_progress.setFormat("Processing audio data...")
            QApplication.processEvents()
            
            # In a real implementation, you would hide the message in the audio
            self.video_encrypt_progress.setValue(70)
            self.video_encrypt_progress.setFormat("Merging with video...")
            QApplication.processEvents()
            
            # Save path
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save Encoded Video", "", "MP4 files (*.mp4)"
            )
            
            if save_path:
                # In a real implementation, you would merge the audio back with the video
                # For now, we'll just show a success message
                
                self.video_encrypt_progress.setValue(100)
                self.video_encrypt_progress.setFormat("Complete!")
                QApplication.processEvents()
                
                # For demonstration, we're just displaying success
                # In a real implementation, you would actually save the file
                self.show_success_message("Message hidden in video (Demonstration)")
                self.statusBar().showMessage("Message hidden in video (Demonstration)")
                
                # Reset progress after a delay
                QApplication.processEvents()
                time.sleep(1)
                self.video_encrypt_progress.setValue(0)
                self.video_encrypt_progress.setFormat("Ready")
            else:
                self.video_encrypt_progress.setValue(0)
                self.video_encrypt_progress.setFormat("Cancelled")
                
        except Exception as e:
            self.video_encrypt_progress.setValue(0)
            self.video_encrypt_progress.setFormat("Error")
            self.show_error_message(f"Error hiding message in video: {str(e)}")
    
    def unhide_from_video(self):
        """Extract a hidden message from a video file"""
        try:
            if not self.video_file_path:
                self.show_error_message("Please select a video file")
                return
                
            if not self.video_decrypt_key.text():
                self.show_error_message("Please select a key file")
                return
            
            # Placeholder implementation for demonstration
            self.video_decrypt_progress.setValue(20)
            self.video_decrypt_progress.setFormat("Extracting audio...")
            QApplication.processEvents()
            
            # In a real implementation, you would extract the audio from the video
            self.video_decrypt_progress.setValue(40)
            self.video_decrypt_progress.setFormat("Processing data...")
            QApplication.processEvents()
            
            # In a real implementation, you would extract the message from the audio
            self.video_decrypt_progress.setValue(60)
            self.video_decrypt_progress.setFormat("Decrypting message...")
            QApplication.processEvents()
            
            # Read decryption key
            with open(self.video_decrypt_key.text(), "rb") as file:
                key = file.read()
            
            # For demonstration, we'll just show a placeholder message
            fernet = Fernet(key)
            # In a real implementation, you would extract and decrypt the message
            # For demonstration, we're using a placeholder encrypted message
            sample_message = "This is a demonstration of the video steganography feature"
            encrypted_sample = fernet.encrypt(sample_message.encode())
            decrypted_text = fernet.decrypt(encrypted_sample).decode()
            
            # Display the decrypted message
            self.video_decrypt_text.setText("DEMO MESSAGE: " + decrypted_text)
            
            self.video_decrypt_progress.setValue(100)
            self.video_decrypt_progress.setFormat("Complete!")
            QApplication.processEvents()
            
            self.statusBar().showMessage("Message extracted (Demonstration)")
            
            # Reset progress after a delay
            QApplication.processEvents()
            time.sleep(1)
            self.video_decrypt_progress.setValue(0)
            self.video_decrypt_progress.setFormat("Ready")
            
        except Exception as e:
            self.video_decrypt_progress.setValue(0)
            self.video_decrypt_progress.setFormat("Error")
            self.show_error_message(f"Error extracting message from video: {str(e)}")

    def setup_button_style(self, button, is_action_button=False):
        """Set up unified button styling"""
        if is_action_button:
            button.setObjectName("actionButton")
            button.setMinimumHeight(50)
            button.setStyleSheet("""
                #actionButton {
                    background-color: #00bcd4;
                    font-size: 16px;
                    font-weight: bold;
                }
                #actionButton:hover {
                    background-color: #00acc1;
                    border: 2px solid #00bcd4;
                }
                #actionButton:pressed {
                    background-color: #0097a7;
                }
            """)
        else:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #0d8bf2;
                    border: 2px solid #2196f3;
                }
                QPushButton:pressed {
                    background-color: #0b7ad1;
                }
            """)

# Main execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply dark fusion style for better appearance
    app.setStyle("Fusion")
    
    # Set app icon if available
    if os.path.exists("app_icon.png"):
        app.setWindowIcon(QIcon("app_icon.png"))
    
    window = SteganographyApp()
    window.show()
    
    sys.exit(app.exec_())