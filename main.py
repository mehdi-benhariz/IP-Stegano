import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import BitHiding

window = tk.Tk()
window.title("Steganography App")
window.geometry("600x600")


def load_image():
    filename = filedialog.askopenfilename()
    image = cv2.imread(filename)
    # display the image in the GUI


def write_text():
    print("Write Text")
    # get the text message from a text box in the GUI
    # write the text message to the image
    # display the updated image in the GUI


load_button = tk.Button(window, text="Load Image", command=load_image)
write_button = tk.Button(window, text="Write Text", command=write_text)
# add more widgets and event handlers here...

window.mainloop()
