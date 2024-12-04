from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from PyQt5.QtCore import QTimer
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
        self.timer.timeout.connect(self.adjust_visibility)  # Connect the timeout to the visibility check function
        self.timer.start(100)
        # Set comboBox style (centered text and border)
        self.comboBox = QtWidgets.QComboBox(self.Form)
        self.comboBox.setGeometry(QtCore.QRect(WIDTH // 2 - 111 // 2, 30, 150, 30))
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
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Gauss")
        self.comboBox.addItem("Jacobi")
        self.comboBox.addItem("Crout")
        self.comboBox.addItem("Dolittle")
        self.comboBox.addItem("Gauss Seidel")
        self.comboBox.addItem("Gauss Jordan")
        self.comboBox.addItem("Cholesky")

        self.scaled_radio = QtWidgets.QRadioButton("SCALE", self.Form)
        self.not_scaled_radio = QtWidgets.QRadioButton("NO SCALE", self.Form)

        # Set default selection to Male
        self.scaled_radio.setChecked(True)

        font = QtGui.QFont()
        font.setBold(True)
        self.scaled_radio.setFont(font)
        self.not_scaled_radio.setFont(font)

        # Position of the comboBox
        comboBox_y = self.comboBox.geometry().y()  # y-coordinate of comboBox
        comboBox_height = self.comboBox.geometry().height()  # Height of comboBox

        # Set positions for radio buttons and button
        self.scaled_radio.setGeometry(WIDTH // 2 - 60, comboBox_y + comboBox_height + 10, 100,
                                      30)  # Male radio below comboBox
        self.not_scaled_radio.setGeometry(WIDTH // 2 + 60, comboBox_y + comboBox_height + 10, 100,
                                          30)  # Female radio below Male radio

        # Label for Significant Digits (Position it below Matrix Size)
        self.label_significant_digits = QtWidgets.QLabel(self.Form)
        self.label_significant_digits.setGeometry(
            QtCore.QRect(WIDTH // 2 - 150, 180, 200, 31))  # Adjusted Y position to fit below Matrix Size
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        self.label_significant_digits.setFont(font)
        self.label_significant_digits.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_significant_digits.setObjectName("label_significant_digits")
        self.label_significant_digits.setText("Significant Digits =")
        self.label_significant_digits.adjustSize()  # Adjust size to fit text

        # Line Edit for Significant Digits
        self.lineEdit_significant_digits = QtWidgets.QLineEdit(self.Form)
        self.lineEdit_significant_digits.setGeometry(
            QtCore.QRect(WIDTH // 2 + 110, 180, 110, 31))  # Adjusted Y position to fit below Matrix Size
        self.lineEdit_significant_digits.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.lineEdit_significant_digits.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: 2px solid black;
                border-radius: 5px;
                color: black;
                padding-left: 10px;
            }
        """)
        self.lineEdit_significant_digits.setObjectName("lineEdit_significant_digits")
        self.lineEdit_significant_digits.setPlaceholderText("Significant Digits")

        # Line Edit with transparent background and border (style)
        self.lineEdit = QtWidgets.QLineEdit(self.Form)
        self.lineEdit.setGeometry(QtCore.QRect(WIDTH // 2 + 40, 140, 110, 31))
        self.lineEdit.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.lineEdit.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: 2px solid black;
                border-radius: 5px;
                color: black;
                padding-left: 10px;
            }
        """)
        self.lineEdit.setObjectName("lineEdit")

        # Label for Matrix Size (Position it to the left of the Line Edit)
        self.label_2 = QtWidgets.QLabel(self.Form)
        self.label_2.setGeometry(QtCore.QRect(WIDTH // 2 - 150, 140, 200, 31))  # Increased width to fit the text
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Matrix Size =")
        self.label_2.adjustSize()  # Adjust size to fit text

        # Background Image
        self.label = QtWidgets.QLabel(self.Form)
        self.label.setGeometry(QtCore.QRect(0, 0, WIDTH, HEIGHT))
        self.label.setPixmap(QtGui.QPixmap("numbers.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # Frame for additional input fields
        self.frame = QtWidgets.QFrame(self.Form)
        self.frame.setGeometry(QtCore.QRect(10, 250, WIDTH, 131))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.hide()

        # Label for Absolute Relative Error (Position it correctly)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(WIDTH // 2 - 210, 10, 250, 31))  # Increased width to fit the text
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        self.label_3.setFont(font)
        self.label_3.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Absolute relative error =")
        self.label_3.adjustSize()  # Adjust size to fit text

        # Line Edit for Absolute Relative Error
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(WIDTH // 2 + 90, 10, 113, 31))
        self.lineEdit_2.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.lineEdit_2.setText("")
        self.lineEdit_2.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: 2px solid black;
                border-radius: 5px;
                color: black;
                padding-left: 10px;
            }
        """)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("Error")

        # Label for Iterations
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(WIDTH // 2 - 160, 60, 200, 31))  # Increased width to fit the text
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        self.label_4.setFont(font)
        self.label_4.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("Iterations =")
        self.label_4.adjustSize()  # Adjust size to fit text

        # Line Edit for Iterations
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_3.setGeometry(QtCore.QRect(WIDTH // 2 + 40, 60, 113, 31))
        self.lineEdit_3.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.lineEdit_3.setText("")
        self.lineEdit_3.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: 2px solid black;
                border-radius: 5px;
                color: black;
                padding-left: 10px;
            }
        """)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setPlaceholderText("Iterations")

        # PushButton (Start)
        self.pushButton = QtWidgets.QPushButton(self.Form)
        self.pushButton.setGeometry(QtCore.QRect(WIDTH // 2 - 50, 380, 80, 30))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("NEXT")

        # PushButton Style
        self.pushButton.setStyleSheet("""
            QPushButton {
                text-align: center;
                border: 2px solid black;
                border-radius: 5px;
                background: transparent;
                font-weight: bold;
                font-underline: true;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)

        # Connect the button to the function that prints the input fields
        self.pushButton.clicked.connect(self.get_matrix_properties)

        # Connect the comboBox signal to show or hide the frame based on selection
        self.comboBox.currentIndexChanged.connect(self.toggle_frame)

        # Raise components to their proper layer
        self.label.raise_()
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
        self.comboBox.setItemText(3, _translate("self.Form", "Dolittle"))
        self.comboBox.setItemText(4, _translate("self.Form", "Gauss Seidel"))
        self.comboBox.setItemText(5, _translate("self.Form", "Gauss Jordan"))

        self.lineEdit.setPlaceholderText(_translate("self.Form", "Matrix Size"))
        self.lineEdit_significant_digits.setPlaceholderText(_translate("self.Form", "Default:10"))

        self.pushButton.setText(_translate("self.Form", "NEXT"))

    def get_matrix_properties(self):
        # Check if the input in lineEdit is a digit
        Observer.matrix_observer = None
        Observer.matrix_details = None

        if self.lineEdit.text().isdigit():
            significant_digits = self.lineEdit_significant_digits.text().strip()
            # If no significant digits entered, set a default value
            if significant_digits.strip() =="":
                significant_digits = "10"  # Default to 0 if not entered

            Observer.matrix_details = {
                "significant_digits": significant_digits,  # Store significant digits as integer
                "iterations": self.lineEdit_3.text(),
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
        elif not self.lineEdit_2.text():
            self.lineEdit_2.setVisible(False)
            self.lineEdit_3.setVisible(True)
            self.label_3.setVisible(False)
            self.label_4.setVisible(True)
        elif not self.lineEdit_3.text():
            self.lineEdit_2.setVisible(True)
            self.lineEdit_3.setVisible(False)
            self.label_3.setVisible(True)
            self.label_4.setVisible(False)

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
