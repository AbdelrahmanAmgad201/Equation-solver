from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QLabel, QPushButton, QRadioButton, QFrame, QStackedWidget, QWidget, QSizePolicy
from PyQt5.QtCore import QTimer, Qt
from .constants import WIDTH, HEIGHT
from .observers import Observer
import sys


class Ui_Form(object):
    def setupUi(self, Form):
        self.Form = Form
        self.Form.setObjectName("self.Form")
        self.Form.resize(WIDTH, HEIGHT)

        self.input_window = None
        self.vector_line_edits = []

        self.timer = QTimer(self.Form)
        self.timer.timeout.connect(self.adjust_visibility)  
        self.timer.start(100)

        # Main Vertical Layout
        main_layout = QVBoxLayout(Form)

        # ComboBox Layout
        combo_layout = QHBoxLayout()
        self.comboBox = QComboBox(self.Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        self.comboBox.setFont(font)
        self.comboBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox.setStyleSheet("""
            QComboBox {
                text-align: center;
                border: 2px solid black;
                border-radius: 5px;
                background: transparent;
            }
            QComboBox QAbstractItemView {
                text-align: left;
            }
        """)
        self.comboBox.addItem("Gauss")
        self.comboBox.addItem("Jacobi")
        self.comboBox.addItem("Crout")
        self.comboBox.addItem("Doolittle")
        self.comboBox.addItem("Gauss Seidel")
        self.comboBox.addItem("Gauss Jordan")
        self.comboBox.addItem("Cholesky")
        self.comboBox.setFixedSize(200, 30)
        combo_layout.addWidget(self.comboBox, alignment=Qt.AlignHCenter)

        # Radio buttons for scale
        scale_layout = QHBoxLayout()

        self.scaled_radio = QRadioButton("SCALE", self.Form)
        self.not_scaled_radio = QRadioButton("NO SCALE", self.Form)
        self.scaled_radio.setChecked(True)
        self.scaled_radio.setFont(font)
        self.not_scaled_radio.setFont(font)
        scale_layout.addWidget(self.scaled_radio)
        scale_layout.addWidget(self.not_scaled_radio)
        scale_layout.setAlignment(Qt.AlignHCenter)
        scale_layout.setSpacing(100)
        
        main_layout.addLayout(combo_layout)
        main_layout.addLayout(scale_layout)


        # Matrix Size Layout
        matrix_layout = QHBoxLayout()
        self.label_2 = QLabel(self.Form)
        self.label_2.setText("Matrix Size =")

        self.lineEdit = QLineEdit(self.Form)
        self.lineEdit.setMaxLength(1)
        self.lineEdit.setPlaceholderText("Matrix Size (MAX : \"9\")")

        self.lineEdit.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: 2px solid black;
                border-radius: 5px;
                color: black;
                padding-left: 10px;
            }
        """)

        matrix_layout.addWidget(self.label_2)
        matrix_layout.addWidget(self.lineEdit)

        matrix_layout.setAlignment(Qt.AlignHCenter)

        main_layout.addLayout(matrix_layout)


        # Significant Digits Layout
        significant_digits_layout = QHBoxLayout()
        self.label_significant_digits = QLabel(self.Form)
        self.label_significant_digits.setText("Significant Digits =")

        self.lineEdit_significant_digits = QLineEdit(self.Form)
        self.lineEdit_significant_digits.setPlaceholderText("Significant Digits")
        self.lineEdit_significant_digits.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: 2px solid black;
                border-radius: 5px;
                color: black;
                padding-left: 10px;
            }
        """)

        # Add label and lineEdit to layout
        significant_digits_layout.addWidget(self.label_significant_digits)
        significant_digits_layout.addWidget(self.lineEdit_significant_digits)

        # Set alignment to center for both widgets in significant_digits_layout
        significant_digits_layout.setAlignment(Qt.AlignHCenter)

        # Add significant_digits_layout to the main_layout and center it within the parent
        main_layout.addLayout(significant_digits_layout)

        # Frame and additional input fields
        self.frame = QFrame(self.Form)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.hide()
        self.frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        
        frame_layout = QVBoxLayout(self.frame)

        absolute_error_layout = QHBoxLayout()
        self.label_3 = QLabel(self.frame)
        self.label_3.setText("Absolute relative error =")
        self.lineEdit_2 = QLineEdit(self.frame)
        self.lineEdit_2.setPlaceholderText("Error")
        self.lineEdit_2.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: 2px solid black;
                border-radius: 5px;
                color: black;
                padding-left: 10px;
            }
        """)
        absolute_error_layout.addWidget(self.label_3)
        absolute_error_layout.addWidget(self.lineEdit_2)
        absolute_error_layout.setAlignment(Qt.AlignHCenter)

        max_iterations_layout = QHBoxLayout()
        self.label_4 = QLabel(self.Form)
        self.label_4.setText("Max_Iterations =")
        self.lineEdit_3 = QLineEdit(self.Form)
        self.lineEdit_3.setPlaceholderText("Max_Iterations Default:\"1000\"")
        max_iterations_layout.addWidget(self.label_4)
        max_iterations_layout.addWidget(self.lineEdit_3)
        max_iterations_layout.setAlignment(Qt.AlignHCenter)
        self.lineEdit_3.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: 2px solid black;
                border-radius: 5px;
                color: black;
                padding-left: 10px;
            }
        """)

        frame_layout.addLayout(max_iterations_layout)
        frame_layout.addLayout(absolute_error_layout)

        main_layout.addLayout(max_iterations_layout)


        self.pushButton = QPushButton(self.Form)
        self.pushButton.setText("NEXT")
        self.pushButton.setStyleSheet("""
            QPushButton {
                text-align: center;
                border: 2px solid black;
                border-radius: 5px;
                background: grey;
                font-weight: bold;
                font-underline: true;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)

        self.backButton = QPushButton(self.Form)
        self.backButton.setText("BACK")
        self.backButton.setStyleSheet("""
            QPushButton {
                text-align: center;
                border: 2px solid black;
                border-radius: 5px;
                background: grey;
                font-weight: bold;
                font-underline: true;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)

        main_layout.addWidget(self.frame)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.backButton)
        button_layout.addWidget(self.pushButton)

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)


        self.pushButton.clicked.connect(self.get_matrix_properties)

        # Connect the comboBox signal to show or hide the frame based on selection
        self.comboBox.currentIndexChanged.connect(self.toggle_frame)


        self.comboBox.raise_()
        self.lineEdit.raise_()
        self.lineEdit_significant_digits.raise_()
        self.label_significant_digits.raise_()
        self.label_2.raise_()
        self.frame.raise_()
        self.pushButton.raise_()
        self.scaled_radio.raise_()
        self.not_scaled_radio.raise_()

        self.retranslateUi(self.Form)
        QtCore.QMetaObject.connectSlotsByName(self.Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.Form.setWindowTitle(_translate("self.Form", "self.Form"))
        self.comboBox.setItemText(0, _translate("self.Form", "Gauss"))
        self.comboBox.setItemText(1, _translate("self.Form", "Jacobi"))
        self.comboBox.setItemText(2, _translate("self.Form", "Crout"))
        self.comboBox.setItemText(3, _translate("self.Form", "Doolittle"))
        self.comboBox.setItemText(4, _translate("self.Form", "Gauss Seidel"))
        self.comboBox.setItemText(5, _translate("self.Form", "Gauss Jordan"))

        self.lineEdit.setPlaceholderText(_translate("self.Form", "Matrix Size (MAX : \"9\")"))
        self.lineEdit_significant_digits.setPlaceholderText(_translate("self.Form", "Default:10"))

        self.pushButton.setText(_translate("self.Form", "NEXT"))
        self.backButton.setText(_translate("self.Form", "BACK"))


    def get_matrix_properties(self):
        # Check if the input in lineEdit is a digit
        Observer.matrix_observer = None
        Observer.matrix_details = None

        if self.lineEdit.text().isdigit():
            significant_digits = self.lineEdit_significant_digits.text().strip()
            iterations = self.lineEdit_3.text().strip()

            # If no significant digits entered, set a default value
            if significant_digits =="":
                significant_digits = "10"  # Default to 0 if not entered

            if iterations =="":
                iterations = "1000"

            Observer.matrix_details = {
                "significant_digits": significant_digits,  # Store significant digits as integer
                "iterations": iterations,
                "matrix_size": self.lineEdit.text(),
                "absolute_relative_error": self.lineEdit_2.text(),
                "method": self.comboBox.currentText(),
                "initial_vector": self.confirm_vector_input(),
                "scaled": self.get_selected_gender()

            }
            print(Observer.matrix_details)

    def toggle_frame(self):
        # Show or hide the frame based on combo box selection
        selected_method = self.comboBox.currentText()
        if selected_method in ["Jacobi", "Gauss Seidel"]:
            self.frame.hide()
            self.frame.show()
        else:
            self.frame.hide()

        Observer.initial_vector_observer = None

    def adjust_visibility(self):
        matrix_size_text = self.lineEdit.text()  # Get the text from the lineEdit
        if matrix_size_text.isdigit() and (
                self.input_window is None or not self.input_window.isVisible()) and self.comboBox.currentText() in [
            "Jacobi", "Gauss Seidel"]:
            self.ask_for_initial_vector(int(matrix_size_text))  # Open the input window for the vector
        elif (not matrix_size_text.isdigit() or not self.comboBox.currentText() in ["Jacobi",
                                                                                    "Gauss Seidel"]) and self.input_window is not None:
            # Hide the input window if it's already visible
            self.input_window.hide()

        # Visibility logic for other fields
        if not self.lineEdit_2.text() and not self.lineEdit_3.text():
            self.lineEdit_2.setVisible(True)
            self.lineEdit_3.setVisible(True)
            self.label_3.setVisible(True)
            self.label_4.setVisible(True)


    def ask_for_initial_vector(self, matrix_size):
        # Only create the input window if it's not already created
        if self.input_window is not None:
            self.input_window.deleteLater()
            self.input_window = None

        if self.input_window is None:
            self.input_window = QtWidgets.QWidget()

        self.input_window.setWindowTitle("Initial Vector Input")
        self.vector_line_edits.clear()

        # Create a grid layout for the vector input
        grid_layout = QtWidgets.QGridLayout()

        # Create QLineEdit widgets for each element in the vector
        for i in range(matrix_size):
            line_edit = QtWidgets.QLineEdit(self.input_window)
            line_edit.setPlaceholderText(f"Enter value for element {i + 1}")
            grid_layout.addWidget(line_edit, i, 0)
            self.vector_line_edits.append(line_edit)

        # Set the layout for the input window
        self.input_window.setLayout(grid_layout)

        # Set the window's geometry to be next to the current window
        self.input_window.setGeometry(self.Form.x() + self.Form.width() + 100, self.Form.y() + 100, 300, HEIGHT)

        # Show the input window
        self.input_window.show()

    def confirm_vector_input(self):
        # Gather the vector values from the input fields
        vector = []
        for line_edit in self.vector_line_edits:

            value = line_edit.text()  # Convert input to float
            vector.append(value)

            if len(vector) == 0:
                QtWidgets.QMessageBox.warning(self.input_window, "Invalid Input",
                                              "Please enter valid numbers for the vector.")
                Observer.initial_vector_observer = None
                return None
        Observer.initial_vector_observer = vector
        return vector

    def get_selected_gender(self):
        """Return the selected gender as a string."""
        if self.scaled_radio.isChecked():
            return True
        return False
