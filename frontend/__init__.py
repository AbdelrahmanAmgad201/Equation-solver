import threading
from homePage import HomePage
import shared_data
import time

test = [
    [[2, -1, 1], [3, 3, 9], [3, 3, 5]], 
    [[1.0, -0.5, 0.5], [3, 3, 9], [3, 3, 5]],
    [[1.0, -0.5, 0.5], [0.0, 4.5, 7.5], [3, 3, 5]],
    [[1.0, -0.5, 0.5], [0.0, 1.0, 1.6667], [0.0, 4.5, 3.5]],
    [[1.0, -0.5, 0.5], [0.0, 1.0, 1.6667], [0.0, 0.0, -4.0]]
]

output = None

def print_matrix(stop_event):
    global output

    while not stop_event.is_set():  # Continuously check if stop_event is not set
        if shared_data.matrix_data is not None and shared_data.start_operation:
            shared_data.start_operation = False
            print(shared_data.matrix_data)
            '''''''''''''''''''''''''''''''''''''''''''''
               Send the shared data from here to parser
               put your results in output
            '''''''''''''''''''''''''''''''''''''''''''''

            output = test

            
            gui.display_output(output=output)
            
        time.sleep(1)

if __name__ == "__main__":
    stop_event = threading.Event()
    matrix_thread = threading.Thread(target=print_matrix, args=(stop_event,))
    matrix_thread.daemon = True
    matrix_thread.start()

    gui = HomePage()

    gui.root.protocol("WM_DELETE_WINDOW", lambda: (stop_event.set(), gui.root.quit()))

    gui.root.mainloop()
