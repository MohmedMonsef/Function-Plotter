from tkinter import *
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np

def err(msg):
    """Print an Error message to the user.

    Args:
        msg (string): the error message to printed to the user 
    """
    messagebox.showerror("Err", msg)

def validate():
    """Validate the user inputs: 
        Function to be plotted: 
            - should at least have one character.
            - all characters must be allowed.
        min and max range: 
            - both have to be numbers.
            - max must be greater than min.


    Returns:
        valid (Boolean)  : if true, then the function has passed the validation.
        func_val (String): the function to be plotted.
        min_val (Number) : the minimum of the plotted range.
        max_val (Number) : the maximum of the plotted range.
    """
    valid = True

    # get inputs & validate
    func_val = func_var.get()
    func_val = func_val.replace(" ", "")
    func_val = func_val.upper() # to avoid any possibility of system command calls
    if len(func_val) < 1:
        err("Enter a valid function")
        valid = False
        return valid, "", 0, 0
    for char in func_val:
        if char not in allowed_characters:
            err("Enter a valid function")
            valid = False
            return valid, "", 0, 0

    try:
        min_val = float(min_var.get())
    except ValueError:
        err("Min has to be a number")
        valid = False
        return valid, "", 0, 0

    try:
        max_val = float(max_var.get())
    except ValueError:
        err("Max has to be a number")
        valid = False
        return valid, "", 0, 0

    if min_val >= max_val:
        err("min has to be smaller than max")
        valid = False
        return valid, "", 0, 0

    func_val = func_val.replace("^", "**")

    return valid, func_val, min_val, max_val

def plot_func(func_val, min_val, max_val):
    """Plots a given function in a given range

    Args:
        func_val (String): The function to be plotted
        min_val (Number) : the minimum of the plotted range.
        max_val (Number) : the maximum of the plotted range.
    """
    # plot
    fig = Figure(figsize = (4.5, 4.5), dpi = 100)
    X = np.linspace(min_val, max_val, num=500)

    try:
        Y = [eval(func_val)]
    except SyntaxError:
        err('Enter a valid Function')
        return
    Y = np.array(Y)
    if Y.shape[0] == 1:  # for the case of constant function
        Y = np.full(X.shape, Y[0])

    plot1 = fig.add_subplot(111)
    plot1.plot(X, Y)
  
    # Embed the plot:
    canvas = FigureCanvasTkAgg(fig, plotter)  
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=1, pady=15)
    
def plot():
    """A function to be called on user plot action
        - first validate the user input
        - if not valid input, return without plottin
        - else if valid input, plot the function to the user 
    """
    valid, func_val, min_val, max_val = validate()
    if not valid: 
        return

    plot_func(func_val, min_val, max_val)


# Initialize application window:
plotter = Tk()
plotter.title("Function Plotter")
plotter.geometry("700x700")

# Set input labels:
func_lbl = Label(plotter, text="Enter a function: ", height=2, font=("Arial", 16)).grid(row=0, column=0)
min_lbl = Label(plotter, text="Min = ", height=2, font=("Arial", 16)).grid(row=1, column=0)
max_lbl = Label(plotter, text="Max = ", height=2, font=("Arial", 16)).grid(row=2, column=0)

# Set input fields:
allowed_characters = [str(char) for char in range(10)]
allowed_characters += ['X', '+', '-', '*', '/', '^']

func_var = StringVar()
func_var.set("") # default value
func_input = Entry(plotter,width=20, font=("Arial", 20),textvariable=func_var).grid(row=0, column=1)

min_var = StringVar()
min_var.set("")
min_input = Entry(plotter, width=4, font=("Arial", 20), textvariable=min_var).grid(row=1, column=1)

max_var = StringVar()
max_var.set("") 
max_input = Entry(plotter, width=4, font=("Arial", 20), textvariable=max_var).grid(row=2, column=1)

# Create a plot button:
btn = Button(plotter, text="Plot", width=20, height=2, bg="#e91e63", fg="white", borderwidth=0, command=plot).grid(row=3, column=0)

# Loop to stay alive:
plotter.mainloop()