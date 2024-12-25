from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
)
import sys
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import math
import time

class ResultWindow(QWidget):
    """Window to display root-finding results."""
    def __init__(self, results):
        super().__init__()
        self.setWindowTitle("Root-Finding Results")
        self.setGeometry(150, 150, 500, 400)

        self.setStyleSheet("font-size: 24px;")

        # Main layout
        main_layout = QVBoxLayout()

        # Error message
        if (results['error_msg'] != ""):
            self.error_label = QLabel(results['error_msg'])
            self.error_label.setAlignment(Qt.AlignCenter)
            self.error_label.setStyleSheet("background-color: red; color: white; font-weight: bold;")
            main_layout.addWidget(self.error_label)

        # Dynamic labels
        self.root_label = QLabel(f"Approximate Root: {results['root']}")
        self.iterations_label = QLabel(f"Number of Iterations: {results['iterations']}")
        self.error_label = QLabel(f"Approximate Relative Error: {results['relative_error']}")
        self.significant_figures_label = QLabel(f"Number of Correct Significant Figures: {results['significant_figures']}")
        self.time_label = QLabel(f"Execution Time: {results['time']:.4f} seconds")

        # Align labels
        for label in [self.root_label, self.iterations_label, self.error_label, self.significant_figures_label, self.time_label]:
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            main_layout.addWidget(label)

        self.setLayout(main_layout)