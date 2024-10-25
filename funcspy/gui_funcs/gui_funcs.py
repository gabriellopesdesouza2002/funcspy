import tkinter as tk
from tkinter import messagebox

def show_popup(title:str, text:str):
    """
    Displays a popup window with a given title and text.

    This function initializes a Tkinter window, hides it, and then displays a 
    popup message box with the specified title and text. After the popup is 
    displayed, the Tkinter window is destroyed.

    Args:
        title (str): The title of the popup window.
        text (str): The text to be displayed in the popup window.

    Returns:
        None
    """
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, text)
    root.destroy()