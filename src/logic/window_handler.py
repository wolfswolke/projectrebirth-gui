from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
import sys

from logic.api_handler import api_handler


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project Rebirth Launcher")
        self.setGeometry(200, 200, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout(main_widget)

        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        layout.addWidget(sidebar_widget)

        button1 = QPushButton("Open Main")
        button1.clicked.connect(self.show_subview)
        sidebar_layout.addWidget(button1)

        button2 = QPushButton("Open Settings")
        button2.clicked.connect(self.show_subview)
        sidebar_layout.addWidget(button2)

        button3 = QPushButton("Open Website")
        button3.clicked.connect(self.show_subview)
        sidebar_layout.addWidget(button3)

        main_section_widget = QWidget()
        main_section_layout = QVBoxLayout(main_section_widget)
        layout.addWidget(main_section_widget)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        main_section_layout.addWidget(self.table)

        self.populate_table()

    def populate_table(self):
        items = [
            {"name": "Item 1", "image_url": "https://via.placeholder.com/150", "description": "Description 1"},
            {"name": "Item 2", "image_url": "https://via.placeholder.com/150", "description": "Description 2"},
            {"name": "Item 3", "image_url": "https://via.placeholder.com/150", "description": "Description 3"},
        ]

        self.table.setRowCount(len(items))

        for i, item in enumerate(items):
            name_item = QTableWidgetItem(item["name"])
            self.table.setItem(i, 0, name_item)

            image_label = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(api_handler.get_image(item["image_url"]).content)
            pixmap = pixmap.scaledToWidth(100)
            image_label.setPixmap(pixmap)
            self.table.setCellWidget(i, 1, image_label)

            description_item = QTableWidgetItem(item["description"])
            self.table.setItem(i, 2, description_item)

    def show_subview(self):
        pass
