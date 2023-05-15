import cv2
import numpy as np
import tkinter as tk
from tkinter import StringVar, filedialog, ttk, END ,messagebox
import BitHiding
import BitHidingGrayscale
import PrinterHiding
import SecretSharing
import dctMessage
from TextHiding import hide_text_in_image, extract_text_from_image
# Tkinter documentation:
# https://www.pythontutorial.net/tkinter/


class SteganographyApp:
    def __init__(self, master):
        self.master = master
        master.title("Steganography Project App")
        master.geometry("600x600")

        button_width = 20
        button_height = 5

        # Setup for dropdown menu
        options = [
            "None Selected",
            "Color Bit Hiding",
            "Grayscale Bit Hiding",
            "Image Originality Token",
            "Hidden Printer Info",
            "Visual Secret Sharing",
            "Message in DCT"
        ]
        selected = StringVar()
        selected.set(options[0])

        dropdown = ttk.Combobox(master, textvariable=selected)
        dropdown['values'] = options
        dropdown['state'] = 'readonly'
        dropdown.grid(row=4, column=0, padx=10, pady=10)

        # Setup for the text entry box
        def modifyText(text):
            global textBox
            textBox = text.get()
        textEntry = StringVar()
        textEntry.trace("w", lambda name, index, mode,
                        textEntry=textEntry: modifyText(textEntry))

        self.image_1 = None
        self.image_2 = None
        # TODO This doesn't work for styling the ComboBox... documentation didn't really help. I'll look into it later
        # self.style = ttk.Style(self)
        # self.style.configure('TCombobox', bg="#ff0000", fg="white", width=button_width, height=button_height)

        # Function updates buttons depending on the type of steganography selected
        def updateButtons(event):
            global button1, button2, button3, button4, label, text_entry

            # Remove everything
            try:
                button1.grid_remove()
            except:
                # Do nothing, exception is only called if the widget does not already exist
                pass
            try:
                button2.grid_remove()
            except:
                pass
            try:
                button3.grid_remove()
            except:
                pass
            try:
                button4.grid_remove()
            except:
                pass
            try:
                label.grid_remove()
            except:
                pass
            try:
                text_entry.grid_remove()
            except:
                pass

            # If an option is selected, place everything
            if dropdown.get() != options[0]:

                button1 = tk.Button(master, text="", bg="#4CAF50", fg="white",
                                    width=button_width, height=button_height)
                button1.grid(row=0, column=0, padx=10, pady=10)
                button2 = tk.Button(master, text="", bg="#2196F3", fg="white",
                                    width=button_width, height=button_height)
                button2.grid(row=0, column=1, padx=10, pady=10)
                button3 = tk.Button(master, text="", bg="#9C27B0", fg="white",
                                    width=button_width, height=button_height)
                button3.grid(row=1, column=0, padx=10, pady=10)
                button4 = tk.Button(master, text="", bg="#FF9800", fg="white",
                                    width=button_width, height=button_height)
                button4.grid(row=1, column=1, padx=10, pady=10)
                label = tk.Label(master, text="", wraplength=300)
                label.grid(row=2, column=0)
                text_entry = tk.Entry(master, width=50, textvariable=textEntry)
                text_entry.grid(row=3, column=0, padx=10,
                                pady=10, columnspan=2, sticky="nsew")
                text_entry.delete(0, END)

                # Depending on which dropdown option is selected, switch the buttons labels and functions appropriately
                match dropdown.get():

                    case "Color Bit Hiding":
                        button1.config(text="Select Image 1",
                                       command=self.upload_image1)
                        button2.config(text="Select Image 2",
                                       command=self.upload_image2)
                        button3.config(text="Run", command=self.runBitHider)
                        label.config(
                            text="Enter the number of bits to use to hide the second image in the first")
                        button4.grid_forget()
                    case "Grayscale Bit Hiding":
                        button1.config(text="Select Color Image",
                                       command=self.upload_image1)
                        button2.config(
                            text="Select Grayscale Image", command=self.upload_grayscale_image, wraplength=100)
                        button3.config(
                            text="Run", command=self.runBitHiderGrayscale)
                        label.config(
                            text="Enter one or two bits to use for the grayscale image")
                        button4.grid_forget()
                    # TODO: work on this
                    case "Image Originality Token":
                        button1.config(text="Load Image",
                                       command=self.load_image)
                        button2.config(text="Write Text",
                                       command=self.write_text)
                        button3.config(text="Generate Token",
                                       command=self.generate_token)
                        button4.config(text="Verify Images",
                                       command=self.open_verify_window)
                        label.config(
                            text="TODO put a description of what to do here")
                    case "Hidden Printer Info":
                        button1.config(text="Select Color Image",
                                       command=self.upload_image1)
                        button2.config(
                            text="Select Grayscale Image", command=self.upload_grayscale_image, wraplength=100)
                        button3.config(
                            text="Run", command=self.runPrinterHiding)
                        label.config(
                            text="Enter: \"X ########\" where # is serial number of printer and X is G for grayscale, C for color")
                        button4.grid_forget()
                    case "Visual Secret Sharing":
                        button1.config(text="Select Grayscale Image",
                                       command=self.upload_grayscale_image)
                        label.config(
                            text="Enter the number of shared images to use.")
                        button2.config(
                            text="Run", command=self.runSecretSharing)
                        button3.grid_forget()
                        button4.grid_forget()
                    case "Message in DCT":
                        button1.config(text="Select Grayscale Image",
                                       command=self.upload_grayscale_image)
                        label.config(
                            text="Enter the message to hide in the dct.")
                        button2.config(text="Run", command=self.runDCTMessage)
                        button3.grid_forget()
                        button4.grid_forget()

        # Event handler that will run the updateButtons function upon combobox change
        dropdown.bind('<<ComboboxSelected>>', updateButtons)

    def load_image(self):
        filename = filedialog.askopenfilename()
        image = cv2.imread(filename)
        print("Load Image:", image)
        self.image_1 = image

    def write_text(self):
        text = textBox
        print("Write Text:", text)

        if (text == ""):
            print("No text entered")
            return
        # TODO check if the image is loaded and dispaly it in the GUI

        cv2.imshow("Image", self.image_1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        secret_image = hide_text_in_image(self.image_1, text)
        cv2.imwrite("secret_image.png", secret_image)

    def generate_token(self):
        print("Generate Token")
        text = text_entry.get()
        # TODO finish this function

    def open_verify_window(self):
        verify_window = tk.Toplevel(self.master)
        verify_window.title("Verifying Images...")
        verify_window.geometry("400x200")

        # create two buttons to upload the two images
        image1_button = tk.Button(
            verify_window, text="Upload Image 1", command=self.upload_image1)
        image1_button.pack(pady=10)

        image2_button = tk.Button(
            verify_window, text="Upload Image 2", command=self.upload_image2)
        image2_button.pack(pady=10)

        # create a button to run the verification
        verify_button = tk.Button(
            verify_window, text="Verify", command=self.verify_images)
        verify_button.pack(pady=10)

    def upload_image1(self):
        global image1
        filename = filedialog.askopenfilename()
        image1 = cv2.imread(filename)
        cv2.waitKey(0)

    def upload_image2(self):
        global image2
        filename = filedialog.askopenfilename()
        image2 = cv2.imread(filename)
        cv2.waitKey(0)

    def upload_grayscale_image(self):
        global imageGrayscale
        filename = filedialog.askopenfilename()
        imageGrayscale = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    
    def verify_images(self):
        print("Verify Images")
        text_1 = extract_text_from_image(image1)
        text_2 = extract_text_from_image(image2)
        print("Text 1:", text_1)
        print("Text 2:", text_2)
        if (text_1 == text_2):
            messagebox.showinfo("Result", "Images are the same")
        else:
            messagebox.showinfo("Result", "Images are different")
        cv2.destroyAllWindows()
    def runBitHider(self):
        bitHidingResult = BitHiding.BitHiding(image1, image2, int(textBox))
        cv2.imshow("Original 1, Bit Modified 1", np.concatenate(
            [image1, bitHidingResult[0]], axis=1))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.imshow("Original 2, Bit Modified, Averaged Bit Modified 2", np.concatenate(
            [image2, bitHidingResult[1], bitHidingResult[2]], axis=1))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def runBitHiderGrayscale(self):
        bitHidingResultBW = BitHidingGrayscale.BitHidingGrayscale(
            image1, imageGrayscale, int(textBox))

        cv2.imshow("Original 1, Bit Modified 1", np.concatenate(
            [image1, bitHidingResultBW[0]], axis=1))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.imshow("Original 2, Bit Modified", np.concatenate(
            [imageGrayscale, bitHidingResultBW[1]], axis=1))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def runPrinterHiding(self):
        printerHiding = PrinterHiding.PrinterHiding(
            textBox[2:], imageGrayscale, True)

        # Prints the information hidden in the printed copy
        print(printerHiding[2])

        # Formatting depending on if gray or colored image
        if textBox[0] == 'G':
            cv2.imshow("Original, Printed Copy Code, and Final Printed Copy", np.concatenate([cv2.cvtColor(
                imageGrayscale, cv2.COLOR_GRAY2BGR), cv2.cvtColor(printerHiding[0], cv2.COLOR_GRAY2BGR), printerHiding[1]], axis=1))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            printerHiding = PrinterHiding.PrinterHiding(
                textBox[2:], image1, False)
            cv2.imshow("Original and Printed Copy", np.concatenate([image1, cv2.cvtColor(
                printerHiding[0], cv2.COLOR_GRAY2BGR), printerHiding[1]], axis=1))
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def runSecretSharing(self):
        shares = SecretSharing.SecretSharing(imageGrayscale, int(textBox))
        height, width = imageGrayscale.shape[:2]

        # Combine all the shares together into one image to make viewing it nicer
        combinedShares = np.zeros(
            (height*(int(textBox)), width), dtype=np.uint8)
        for i in range(int(textBox)):
            combinedShares[height * i:height * (i + 1)] = shares[0][i]

        cv2.imshow("Noisy shares", combinedShares)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.imshow("Image created from two random shares", shares[1])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def runDCTMessage(self):

        dctMsg = dctMessage.dctMessage(imageGrayscale, textBox)

        cv2.imshow("Original Image, DCT Modified Image", np.concatenate(
            [imageGrayscale, np.uint8(np.round(dctMsg[0]))], axis=1))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(dctMsg[1])


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
