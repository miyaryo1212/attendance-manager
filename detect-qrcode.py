import ctypes
import tkinter
import tkinter.filedialog
import tkinter.messagebox

import cv2 as cv
import pyzbar


# gui messagebox
def msgbox(title, content):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo(title, content)

    return None


# gui filedialog
def openfile(file_type=[("", "*")]):
    root = tkinter.Tk()
    root.withdraw()
    file_path = tkinter.filedialog.askopenfilename(filetypes=file_type)

    if not file_path:
        quit()

    return file_path


if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass
