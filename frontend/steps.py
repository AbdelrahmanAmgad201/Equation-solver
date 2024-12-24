from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
)
import sys
import numpy as np
import math
import time

class TableWindow(QWidget):
    """Window to display steps as a table."""
    def __init__(self, steps):
        super().__init__()
        self.setWindowTitle("Steps Table")
        self.setGeometry(200, 200, 600, 400)

        self.setStyleSheet("font-size: 20px")
        # Create layout
        layout = QVBoxLayout()

        # Create table widget
        self.table = QTableWidget()
        self.table.setRowCount(len(steps))
        self.table.setColumnCount(len(steps[0]))
        self.table.setHorizontalHeaderLabels(steps[0].keys())  # Set column headers

        # Fill the table with data
        for row_idx, step in enumerate(steps):
            for col_idx, key in enumerate(step):
                item = QTableWidgetItem(str(step[key]))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

        # Add table to layout
        layout.addWidget(self.table)
        self.setLayout(layout)