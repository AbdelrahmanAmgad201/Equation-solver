from .observers import Observer
from PyQt5 import QtWidgets

class ckeck_observer:
    @staticmethod
    def check_observer_out(window):
        return [Observer.matrix_observer, Observer.matrix_details, Observer.initial_vector_observer]

    @staticmethod
    def check_observer_in(window, input,time):

        if Observer.matrix_observer is not None:
            print("11")
            if input is None:
                QtWidgets.QMessageBox.warning( "Invalid Input", "Invalid Input")
            elif Observer.matrix_details['method'] == "Gauss" or Observer.matrix_details['method'] == "Gauss Jordan":
                window.go_to_matrix_display(
                    [ele.tolist() for ele in input]
                )
            elif Observer.matrix_details['method'] == "Jacobi" or Observer.matrix_details['method'] == "Gauss Seidel":
                window.go_to_matrix_display(
                    [[ele.tolist() for ele in input]]
                )
            elif Observer.matrix_details['method'] == "Crout":
                window.display_LU_matrix(
                    [input[0].tolist(), input[2].tolist()], [input[1].tolist(), input[2].tolist()]
                )
            elif Observer.matrix_details['method'] == "Dolittle":
                window.display_LU_matrix(
                    [input[0].tolist(), input[2].tolist()], [input[1].tolist(), input[2].tolist()]
                )
            elif Observer.matrix_details['method'] == "Cholesky":
                window.display_LU_matrix(
                    [input[0].tolist(), input[2].tolist()], [input[1].tolist(), input[2].tolist()]
                )
                # Create a message box
            ckeck_observer.show_message(time)
            Observer.matrix_observer = None
    @staticmethod
    def show_message(time):
        # Create a message box
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)  # Set the icon to Information
        msg.setWindowTitle("time")  # Set the window title
        msg.setText(f'time = {time}')  # Set the main message text
        # Show the message box
        msg.exec_()
