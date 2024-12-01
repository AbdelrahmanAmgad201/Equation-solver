from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from .observers import Observer
from .constants import WIDTH, HEIGHT

from PyQt5.QtWidgets import QMessageBox, QScrollArea, QFrame


class SecondPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Second Page")

        # Background Image
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, WIDTH, HEIGHT))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("numerical2.jpg"))
        self.label.setScaledContents(True)

        # Scrollable Area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(WIDTH // 8, HEIGHT // 8, WIDTH * 3 // 4, HEIGHT * 3 // 8)
        self.scroll_area.setStyleSheet("background: rgba(0, 0, 0, 0.5); border: 2px solid white;")
        self.scroll_area.setWidgetResizable(True)

        # Frame inside scroll area
        self.scroll_frame = QFrame()
        self.scroll_frame.setStyleSheet("background: transparent;")
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_frame)
        self.scroll_area.setWidget(self.scroll_frame)

        # Matrix entry container
        self.matrix_entries = []

        # Buttons
        self.startButton = None
        self.backButton = None

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SecondPage", "Second Page"))

    def go_back(self):
        # Switch to the first page when the button is clicked
        self.parent().setCurrentIndex(0)

    def display_matrix_entries(self, num_rows, num_cols):
        """Display matrix input fields based on the matrix size."""

        # Clear previous matrix entries by removing the widgets in the layout
        for entry_row in self.matrix_entries:
            for entry in entry_row:
                entry.deleteLater()  # Remove the previous entry fields
        self.matrix_entries.clear()

        # Remove existing container widget if it exists
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()  # Remove the old widget

        # Create a new container widget for the grid layout
        container_widget = QtWidgets.QWidget(self.scroll_frame)
        grid_layout = QtWidgets.QGridLayout(container_widget)

        # Create the matrix input fields again based on the new size
        for i in range(num_rows):
            row_entries = []
            row_label = QtWidgets.QLabel(f"Row {i + 1}", container_widget)
            row_label.setStyleSheet("color: white;")
            grid_layout.addWidget(row_label, i, 0)  # Add row label

            for j in range(num_cols + 1):
                entry = QtWidgets.QLineEdit(container_widget)
                entry.setPlaceholderText(f"(A{i}{j})")
                entry.setStyleSheet('''
                    QLineEdit {
                        background: transparent;
                        border: 2px solid white;
                        border-radius: 5px;
                        color: white;
                        padding-left: 10px;
                    }
                    QLineEdit::placeholder {
                        color: white;
                    }
                ''')
                if j == num_cols:
                    entry.setPlaceholderText(f"(B{i})")
                    entry.setStyleSheet('''
                        QLineEdit {
                            background: transparent;
                            border: 2px solid white;
                            border-radius: 5px;
                            color: yellow;
                            padding-left: 10px;
                        }
                        QLineEdit::placeholder {
                            color: white;
                        }
                    ''')
                grid_layout.addWidget(entry, i, j + 1)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

        # Add the new container widget to the scroll frame layout
        self.scroll_layout.addWidget(container_widget)

        # Update the button placement if necessary
        self.update_buttons()

    def update_buttons(self):
        # Update the button placement
        if not self.startButton:
            self.startButton = QtWidgets.QPushButton("Start", self)
            self.startButton.setStyleSheet('''QPushButton {
                text-align: center;
                border: 2px solid black;
                border-radius: 5px;
                background: transparent;
                font-weight: bold;
                padding: 5px 10px;
                color: blue;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }''')
            self.startButton.clicked.connect(self.get_matrix)
            self.startButton.setGeometry(WIDTH // 2 - 40, HEIGHT // 2 + HEIGHT // 4 + 10, 80, 30)
            self.startButton.show()

        if not self.backButton:
            self.backButton = QtWidgets.QPushButton("Back to First Page", self)
            self.backButton.setStyleSheet('''QPushButton {
                text-align: center;
                border: 2px solid black;
                border-radius: 5px;
                background: transparent;
                font-weight: bold;
                padding: 5px 10px;
                color: red;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }''')
            self.backButton.clicked.connect(self.go_back)
            self.backButton.setGeometry(WIDTH // 2 - 75, HEIGHT // 2 + HEIGHT // 4 + 50, 150, 30)
            self.backButton.show()

    def get_matrix(self):
        """Print the matrix based on entered values."""
        flag = True
        matrix = []
        for row in self.matrix_entries:
            row_data = []
            for entry in row:
                value = entry.text()
                if value.strip() != "":
                    row_data.append(value)
                    entry.setStyleSheet('''
                        QLineEdit {
                            background: transparent;
                            border: 2px solid green;
                            border-radius: 5px;
                            color: white;
                            padding-left: 10px;
                        }
                    ''')
                else:
                    entry.setStyleSheet('''
                        QLineEdit {
                            background: transparent;
                            border: 2px solid red;
                            border-radius: 5px;
                            color: white;
                            padding-left: 10px;
                        }
                    ''')
                    flag = False
            matrix.append(row_data)

        if flag:
            if Observer.matrix_observer is None or Observer.matrix_observer != matrix:
                Observer.matrix_observer = matrix
        else:
            Observer.matrix_observer = None
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("Matrix should be filled!")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        # Create the QStackedWidget to hold multiple pages
        self.stackedWidget = QtWidgets.QStackedWidget(self)

        # Create instances of your pages
        self.firstPage = QtWidgets.QWidget()
        self.secondPage = SecondPage()

        # Set up first page (simple button to navigate to the second page)
        self.firstPageButton = QtWidgets.QPushButton("Go to Second Page", self.firstPage)
        self.firstPageButton.clicked.connect(self.show_second_page)
        self.firstPageButton.setGeometry(100, 100, 150, 30)

        # Add pages to stacked widget
        self.stackedWidget.addWidget(self.firstPage)
        self.stackedWidget.addWidget(self.secondPage)

        # Set stacked widget as central widget of the main window
        self.setCentralWidget(self.stackedWidget)

    def show_second_page(self, matrix_size):
        # Show the second page with matrix entries based on the matrix size
        num_rows = matrix_size
        num_cols = matrix_size  # Assuming a square matrix for simplicity
        self.secondPage.display_matrix_entries(num_rows, num_cols)
        self.stackedWidget.setCurrentIndex(1)
