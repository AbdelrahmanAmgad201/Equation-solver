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
        self.root.geometry("750x900")

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
        
        self.absolute_error = None
        self.iterations = None


        self.matrix_frame = tk.Frame(self.root)

        self.special_frame = tk.Frame(self.main_frame)
        self.initial_vector_button = tk.Button(self.special_frame, text="Initial vector", command=self.enter_initial_vector)


        self.description = tk.Label(self.special_frame, font=('Comic Sans MS', 8))


        self.absolute_error_button = tk.Button(self.special_frame, text="absolute_error", command=self.enter_absolute_error)
        self.iteration_button = tk.Button(self.special_frame, text="iteration_button", command=self.enter_iterations)
        self.absolute_error_button.grid(column=0, row=0)
        self.iteration_button.grid(column=1,row=0)

        self.is_matrix_ready = False
        self.matrix = None

        self.header = tk.Label(self.root, text="Numerical Analysis!", font=('Comic Sans MS', 20))
        self.header.pack(pady=20)

        self.equations_number = -1
        self.matrix_button = tk.Button(self.main_frame, text="Create Matrix", command=self.show_matrix_page)
        self.start_button = tk.Button(self.main_frame, text="Start", font=("Comic Sans MS", 10), command=self.get_matrix_details)


        self.create_menu()

        self.label = tk.Label(self.main_frame, text="Select number of equations", font=('Comic Sans MS', 16))
        self.label.pack(pady=20)


        self.signifcant_digits_place_holder = "Significant digits"
        
        self.signifcant_digits = tk.Entry(self.main_frame, fg='gray')
        self.signifcant_digits.insert(0, self.signifcant_digits_place_holder)
        self.signifcant_digits.bind("<FocusIn>", self.on_focus_in)
        self.signifcant_digits.bind("<FocusOut>", self.on_focus_out)

        self.signifcant_digits.pack(pady=10)


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

        self.dropdown = tk.OptionMenu(self.main_frame, self.selected_operation, *self.options, command=self.on_option_change)
        self.dropdown.pack(pady=20)

    def on_option_change(self, selection):
        if selection in ["Jacobi", "Gauss Seidel"]:
            self.special_frame.pack(pady=2)
            self.create_initial_vector()
            
        else:
            self.special_frame.pack_forget()

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



        if self.matrix_toolkit is None:
            self.matrix_toolkit = matrixDelegator.MatrixDelegator(self.main_frame, self.matrix_frame, self.equations_number)
        else:
            self.matrix_frame.destroy()
            self.matrix_frame = tk.Frame(self.root)
            for widget in self.main_frame.winfo_children():
                if isinstance(widget, tk.Text):
                    widget.destroy()

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
            self.create_initial_vector()


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
            self.create_initial_vector()


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
            if isinstance(widget, tk.Toplevel) or not shared_data.start_operation:
                self.destroy_start_button()
                break
            elif isinstance(widget, tk.Text) and shared_data.start_operation:
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
            "significant digits": self.signifcant_digits.get(),
            "absolute_error":self.absolute_error,
            "iterations":self.iterations,
            "initial_vector":self.initial_vector

        }
        shared_data.matrix_data = details
        shared_data.start_operation = True


    def display_output(self,output : list):
        self.destroy_start_button()
        self.matrix_toolkit.draw_output_matrix(output)

    def on_focus_in(self, event):
        """Clears the placeholder text when the entry field is clicked."""
        current_text = self.signifcant_digits.get()
        if current_text == self.signifcant_digits_place_holder:
            self.signifcant_digits.delete(0, tk.END)  # Clear the placeholder text
            self.signifcant_digits.config(fg='black')  # Change text color to black

    def on_focus_out(self, event):
        """Restores the placeholder text if the entry field is empty."""
        current_text = self.signifcant_digits.get()
        if current_text == "":
            self.signifcant_digits.insert(0, self.signifcant_digits_place_holder)  # Insert placeholder text
            self.signifcant_digits.config(fg='gray') 


    def enter_absolute_error(self):
        entry_window = tk.Toplevel(self.root)
        entry_window.title("Absolute Relative Error")
        entry_window.geometry("300x150")
        entry_window.resizable(False, False)

        # Validation command
        validate_command = self.root.register(self.validate_numeric_input)

        # Label for guidance
        label = tk.Label(entry_window, text="Enter Absolute Relative Error:", font=("Comic Sans MS", 12))
        label.pack(pady=10)

        # Numeric Entry with validation
        entry = tk.Entry(
            entry_window, validate="key", validatecommand=(validate_command, "%P")
        )
        entry.pack(pady=10)

        # Function to handle the input and assign it to `self.absolute_error`
        def submit():
            value = entry.get()
            if not value:
                messagebox.showerror("Input Error", "Absolute error cannot be empty!")
            else:
                self.absolute_error = float(value)  # Convert to float
                entry_window.destroy()
                self.description.config(text = f"Absolute error = {self.absolute_error}")
                self.description.grid(row=1,columnspan=2)
                self.iterations = 0


        # Submit Button
        submit_button = tk.Button(entry_window, text="Submit", command=submit)
        submit_button.pack(pady=10)



    def enter_iterations(self):
        entry_window = tk.Toplevel(self.root)
        entry_window.title("Maximum Iterations")
        entry_window.geometry("300x150")
        entry_window.resizable(False, False)

        # Validation command
        validate_command = self.root.register(self.validate_numeric_input)

        # Label for guidance
        label = tk.Label(entry_window, text="Enter Maximum Iterations:", font=("Comic Sans MS", 12))
        label.pack(pady=10)

        # Numeric Entry with validation
        entry = tk.Entry(
            entry_window, validate="key", validatecommand=(validate_command, "%P")
        )
        entry.pack(pady=10)

        # Function to handle the input and assign it to `self.iterations`
        def submit():
            value = entry.get()
            if not value:
                messagebox.showerror("Input Error", "Iterations cannot be empty!")
            else:
                self.iterations = int(value)  # Convert to integer
                entry_window.destroy()
                self.absolute_error = 0
                self.description.config(text = f"Iterations = {self.iterations}")
                self.description.grid(row=1,columnspan=2)

        # Submit Button
        submit_button = tk.Button(entry_window, text="Submit", command=submit)
        submit_button.pack(pady=10)


    def validate_numeric_input(self, char):
        """Validation function for numeric input."""
        return char.isdigit() or char == "." or char == ""
    
    def create_initial_vector(self):
        if self.selected_operation.get() in ["Jacobi", "Gauss Seidel"] and self.equations_number >0:
            self.initial_vector_button.grid(row=2, column=0, columnspan=2)
        
        else:
            self.initial_vector_button.grid_forget()


    def enter_initial_vector(self):
        """
        Opens a Toplevel window to input an initial vector of length equal to self.equations_number.
        """
        if self.equations_number <= 0:
            messagebox.showerror("Error", "Number of equations must be greater than 0!")
            return

        vector_window = tk.Toplevel(self.root)
        vector_window.title("Initial Vector")
        vector_window.geometry("300x400")
        vector_window.resizable(False, False)

        # Instructions label
        instruction_label = tk.Label(vector_window, text="Enter the initial vector values:")
        instruction_label.pack(pady=10)

        # Entries to store the vector values
        self.initial_vector_entries = []
        for i in range(self.equations_number):
            frame = tk.Frame(vector_window)
            frame.pack(pady=5)
            tk.Label(frame, text=f"Value {i+1}:").pack(side=tk.LEFT, padx=5)
            
            entry = tk.Entry(frame, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P"))
            entry.pack(side=tk.RIGHT, padx=5)
            self.initial_vector_entries.append(entry)

        # Submit button
        submit_button = tk.Button(vector_window, text="Enter", command=lambda: self.save_initial_vector(vector_window))
        submit_button.pack(pady=20)

    def save_initial_vector(self, window):
        """
        Retrieves and stores the initial vector values entered by the user.
        """
        try:
            self.initial_vector = [
                float(entry.get()) for entry in self.initial_vector_entries
            ]
            messagebox.showinfo("Success", f"Initial vector saved: {self.initial_vector}")
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for the initial vector.")

