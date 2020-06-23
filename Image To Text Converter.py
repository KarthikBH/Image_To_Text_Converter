import os
from tkinter.filedialog import askopenfilename, asksaveasfilename
import cv2
import imutils as imutils
import pytesseract
import tkinter as tk
from PIL import Image, ImageTk

pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"

txt_edit = None
img_edit = None

def open_file():

    filepath = askopenfilename(
        filetypes=[("Image Files", "*.jpg, *.png"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)

    required_width = txt_edit.winfo_width()

    image = cv2.imread(filepath)
    cv2.imwrite("users_pic.png", image)
    resized = imutils.resize(image, width=required_width)
    cv2.imwrite("pic.png", resized)

    load = Image.open("pic.png")
    render = ImageTk.PhotoImage(load)
    img_edit = tk.Label(fr_bottom,image=render)
    img_edit.image = render
    img_edit.grid(row=1, column=0, sticky="ns", padx=5, pady=15)
    window.title(f"Image > Text Converter : {filepath}")
def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"Image > Text Converter - {filepath}")
def extract_text_from_img():
    if not os.path.exists("users_pic.png"):
        return

    image = cv2.imread("users_pic.png")
    text = pytesseract.image_to_string(image)
    text = text.split("\n")
    for line in text:
        if line.strip() == "":
            continue
        else:
            txt_edit.insert(tk.END, line)
            txt_edit.insert(tk.END, "\n")
def on_closing():
    if os.path.exists("pic.png"):
        os.remove("pic.png")
    if os.path.exists("users_pic.png"):
        os.remove("users_pic.png")
    window.destroy()

window = tk.Tk()
window.title("Image > Text Converter")
window.resizable(0,0)
if os.path.exists("icon.ico"):
    window.iconbitmap('icon.ico')
fr_top = tk.Frame(window, bg = "#3b3934")
btn_open = tk.Button(fr_top, text="Open", command=open_file, activeforeground = "white", activebackground = "black")
btn_save = tk.Button(fr_top, text="Save As...", command=save_file, activeforeground = "white", activebackground = "black")
btn_open.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
btn_save.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
fr_top.grid(row=0, column=0, sticky="nsew")

fr_bottom = tk.Frame(window, bg = "#3b3934")
img_edit = tk.Text(fr_bottom)
img_edit.grid(row=1, column=0, sticky="ns", padx=5, pady=15)
btn_Find = tk.Button(fr_bottom, text=" >>> ", command=extract_text_from_img, activeforeground = "white", activebackground = "black")
btn_Find.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

scroll_bar = tk.Scrollbar(fr_bottom)
scroll_bar.grid(row=1, column=3, sticky="ns")
txt_edit = tk.Text(fr_bottom, yscrollcommand=scroll_bar.set)
txt_edit.grid(row=1, column=2, sticky="ns", padx=5, pady=15)
fr_bottom.grid(row=1, column=0, sticky="ns")
scroll_bar.config(command=txt_edit.yview)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()