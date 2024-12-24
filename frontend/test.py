from PyQt5.QtCore import Qt  # Import Qt for alignment constants
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QWidget
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Window")
        self.setGeometry(100, 100, 400, 200)  # Window size and position

        # Create the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Title label in the middle
        title_label = QLabel("Window Title", self)
        title_label.setAlignment(Qt.AlignCenter)  # Use Qt.AlignCenter for center alignment

        # Label and dropdown list
        method_label = QLabel("Method:")
        dropdown = QComboBox()
        dropdown.addItems(["Option 1", "Option 2", "Option 3"])  # Add dropdown items

        # Layouts
        method_layout = QHBoxLayout()
        method_layout.addWidget(method_label)
        method_layout.addWidget(dropdown)

        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(title_label)
        main_layout.addLayout(method_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
