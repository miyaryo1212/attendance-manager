import ctypes
import tkinter
import tkinter.filedialog
import tkinter.messagebox

import qrcode


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


# generate qrcode
def generateqrcode(qty, dir="./saved"):
    digits = len(str(qty))
    for i in range(qty):
        content = format(str(i).zfill(digits))
        img = qrcode.make("{}".format(content))
        img.save("{}/{}.png".format(dir, content))

    return None


if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass

    qty = 100
    dir_path = openfolder()
    generateqrcode(qty, dir_path)
