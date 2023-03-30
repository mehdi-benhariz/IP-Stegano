import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox


class SteganographyApp:
    def __init__(self, master):
        self.master = master
        master.title("Steganography Project App")
        master.geometry("600x600")

        button_width = 20
        button_height = 5

        # create buttons and text field
        self.load_button = tk.Button(master, text="Load Image", command=self.load_image, bg="#4CAF50", fg="white",
                                     width=button_width, height=button_height)
        self.load_button.grid(row=0, column=0, padx=10, pady=10)

        self.write_button = tk.Button(master, text="Write Text", command=self.write_text, bg="#2196F3", fg="white",
                                      width=button_width, height=button_height)
        self.write_button.grid(row=0, column=1, padx=10, pady=10)

        self.token_button = tk.Button(master, text="Generate Token", command=self.generate_token, bg="#9C27B0", fg="white",
                                      width=button_width, height=button_height)
        self.token_button.grid(row=1, column=0, padx=10, pady=10)

        self.verify_button = tk.Button(master, text="Verify Images", command=self.open_verify_window, bg="#FF9800", fg="white",
                                       width=button_width, height=button_height)
        self.verify_button.grid(row=1, column=1, padx=10, pady=10)

        self.text_entry = tk.Entry(master, width=50)
        self.text_entry.grid(row=2, column=0, padx=10,
                             pady=10, columnspan=2, sticky="nsew")

    def load_image(self):
        filename = filedialog.askopenfilename()
        image = cv2.imread(filename)
        # TODO display the image in the GUI

    def write_text(self):
        text = self.text_entry.get()
        print("Write Text:", text)
        # TODO get the text message from the input field in the GUI

    def generate_token(self):
        print("Generate Token")
        # TODO finish this function

    def open_verify_window(self):
        verify_window = tk.Toplevel(self.master)
        verify_window.title("Verify Images")
        verify_window.geometry("400x200")

        # create two buttons to upload the two images
        image1_button = tk.Button(
            verify_window, text="Upload Image 1", command=self.upload_image1)
        image1_button.pack(pady=10)

        image2_button = tk.Button(
            verify_window, text="Upload Image 2", command=self.upload_image2)
        image2_button.pack(pady=10)

    def upload_image1(self):
        filename = filedialog.askopenfilename()
        image1 = cv2.imread(filename)
        # TODO store the first image and close the window

    def upload_image2(self):
        filename = filedialog.askopenfilename()
        image2 = cv2.imread(filename)
        # TODO store the second image and close the window


def open_verify_window(self):
    verify_window = tk.Toplevel(self.master)
    verify_window.title("Verify Images")
    verify_window.geometry("600x400")

    # create two buttons to upload the two images
    button_width = 20
    button_height = 5
    image1_button = tk.Button(
        verify_window, text="Upload Image 1", command=self.upload_image1, bg="#4CAF50", fg="white",
        width=button_width, height=button_height)
    image1_button.grid(row=0, column=0, padx=10, pady=10)

    image2_button = tk.Button(
        verify_window, text="Upload Image 2", command=self.upload_image2, bg="#2196F3", fg="white",
        width=button_width, height=button_height)
    image2_button.grid(row=0, column=1, padx=10, pady=10)

    self.image1_label = tk.Label(verify_window, text="", bg="white")
    self.image1_label.grid(row=1, column=0, padx=10, pady=10)

    self.image2_label = tk.Label(verify_window, text="", bg="white")
    self.image2_label.grid(row=1, column=1, padx=10, pady=10)

    verify_button = tk.Button(
        verify_window, text="Verify", command=self.verify_images, bg="#9C27B0", fg="white",
        width=button_width, height=button_height)
    verify_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


def verify_images(self):
    # TODO finish this function
    pass


root = tk.Tk()
app = SteganographyApp(root)
root.mainloop()
