import tkinter as tk
from tkinter import messagebox
import matrixDelegator
import shared_data
from PIL import Image, ImageTk


class HomePage:
    options = ["Gauss", "Doolittle", "Crout", "Jacobi", "Gauss Seidel", "Gauss Jordan", "Cholesky"]

    def __init__(self):
        self.root = tk.Tk()
        self.matrix_toolkit = None
        self.root.geometry("750x750")

        self.root.title("Numerical")

        # self.bg_image = Image.open("Equation-solver\\frontend\\static\\pxfuel.jpg")  # Replace with your image path
        # self.bg_image = self.bg_image.resize((750, 750), Image.Resampling.LANCZOS)  # Replace ANTIALIAS
        # self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # # Add the image as a label
        # self.bg_label = tk.Label(self.root, image=self.bg_photo)
        # self.bg_label.place(relwidth=1, relheight=1)

        self.main_frame = tk.Frame(self.root)

        #self.fm_image = Image.open("Equation-solver\\frontend\\static\\there.jpg")  # Replace with your image path
        #self.fm_image = self.fm_image.resize((750, 750), Image.Resampling.LANCZOS)  # Replace ANTIALIAS
        #self.fm_photo = ImageTk.PhotoImage(self.fm_image)

        ## Add the image as a label
        # self.fm_label = tk.Label(self.main_frame, image=self.fm_photo)
        # self.fm_label.place(relwidth=1, relheight=1)


        

        self.start_button_life = False


        self.matrix_frame = tk.Frame(self.root)

        self.is_matrix_ready = False
        self.matrix = None

        self.header = tk.Label(self.root, text="Numerical Analysis!", font=('Comic Sans MS', 20))
        self.header.pack(pady=20)

        self.equations_number = -1
        self.matrix_button = tk.Button(self.main_frame, text="Create Matrix", command=self.show_matrix_page)
        self.start_button = tk.Button(self.main_frame, text="Start", font=("Comic Sans MS", 10), command=self.get_matrix_details)

        self.next_button = tk.Button(self.main_frame, text='Next', command=lambda: self.increment_output_index())
        self.prev_button = tk.Button(self.main_frame, text='Previous', command=lambda: self.decrement_output_index())
        




        self.create_menu()

        self.label = tk.Label(self.main_frame, text="Select number of equations", font=('Comic Sans MS', 16))
        self.label.pack(pady=20)

        self.number_selector = tk.Button(self.main_frame, text="Number of equations", command=self.open_number_selector)
        self.number_selector.pack(pady=20)

        self.selected_number_label = tk.Label(
            self.main_frame, text=f"Number of equations is unknown!", foreground='red', font=('Comic Sans MS', 14)
        )
        self.selected_number_label.pack(pady=20)

        self.main_frame.pack()

        # Periodically check
        self.main_frame.after(1000, self.check_matrix_button)
        
        self.main_frame.after(1000, self.create_start_button)



    def create_menu(self):
        self.selected_operation = tk.StringVar(self.root)
        self.selected_operation.set(self.options[0])

        self.dropdown = tk.OptionMenu(self.main_frame, self.selected_operation, *self.options)
        self.dropdown.pack(pady=20)

    def check_matrix_button(self):
        if self.equations_number >= 0:
            self.create_matrix_button()
        else:
            self.destroy_matrix_button()

    def create_matrix_button(self):
        self.matrix_button.pack(pady=10)

    def destroy_matrix_button(self):
        self.matrix_button.pack_forget()

    def show_matrix_page(self):
        if self.equations_number == 0:
            messagebox.showerror("Error", "Number of equations must be greater than 0!")
            return

        self.main_frame.pack_forget()
        self.create_matrix_page()

    def create_matrix_page(self):

        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.Text):
                widget.destroy()

        if self.matrix_toolkit is None:
            self.matrix_toolkit = matrixDelegator.MatrixDelegator(self.main_frame, self.matrix_frame, self.equations_number)
        else:
            self.matrix_frame.destroy()
            self.matrix_frame = tk.Frame(self.root)

            self.matrix_toolkit = matrixDelegator.MatrixDelegator(self.main_frame, self.matrix_frame, self.equations_number)

        self.matrix_frame.pack(fill="both", expand=True)

    def open_number_selector(self):
        shared_data.matrix_data = None
        self.destroy_start_button()


        def select_number(number):
            self.destroy_start_button()
            equations_number_list.append(str(number))
            self.equations_number = int("".join(equations_number_list))
            self.selected_number_label.config(
                text=f"Number of equations: {self.equations_number}", foreground="#059212"
            )
            self.check_matrix_button()

        def undo():
            self.destroy_start_button()
            if equations_number_list:
                equations_number_list.pop()
                if len(equations_number_list) == 0:
                    self.equations_number = -1
                    self.selected_number_label.config(
                        text=f"Number of equations is unknown!", foreground="red"
                    )
                else:
                    self.equations_number = int("".join(equations_number_list))
                    self.selected_number_label.config(
                        text=f"Number of equations: {self.equations_number}"
                    )
            self.check_matrix_button()

        equations_number_list = []
        number_window = tk.Toplevel(self.root)
        number_window.geometry("200x200")
        number_window.resizable(False, False)
        number_window.title("Numbers")

        numbers = list(range(0, 10))

        for num in numbers:
            button = tk.Button(number_window, text=str(num), command=lambda n=num: select_number(n))
            button.grid(row=num // 3, column=num % 3, padx=0, pady=5)

        back_button = tk.Button(number_window, text="Back", command=undo)
        back_button.grid(row=3, column=1, padx=0, pady=5)

        input_button = tk.Button(number_window, text="Enter", command=lambda: number_window.destroy())
        input_button.grid(row=3, column=2, padx=0, pady=5)

        number_window.grid_columnconfigure(0, weight=1)
        number_window.grid_columnconfigure(1, weight=1)
        number_window.grid_columnconfigure(2, weight=1)

    def create_start_button(self):

        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.Toplevel):
                self.destroy_start_button()
                break
            elif isinstance(widget, tk.Text):
                self.start_button.pack(pady=10)
        
        self.main_frame.after(1000, self.create_start_button)

    def destroy_start_button(self):
        self.start_button.pack_forget()
        

    def get_matrix_details(self):
        # Simulating matrix details retrieval
        self.matrix = self.matrix_toolkit.get_matrix()
        details = {
            "method": self.selected_operation.get(),
            "size": self.equations_number,
            "matrix": self.matrix,
        }
        shared_data.matrix_data = details
        shared_data.start_operation = True


    def display_output(self,output : list):
        self.destroy_start_button()
        self.matrix_toolkit.draw_output_matrix(output)
    
    
