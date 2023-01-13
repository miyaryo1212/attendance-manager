import ctypes

import tkinter
import tkinter.filedialog
import tkinter.messagebox


# gui messagebox
def msgbox(title, content):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo(title, content)

    return None


# gui folderdialog
def openfolder():
    root = tkinter.Tk()
    root.withdraw()
    dir_path = tkinter.filedialog.askdirectory()

    if not dir_path:
        quit()

    return dir_path


if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass
