import ctypes
import os
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
def generateqrcode(qty, dir):
    digits = len(str(qty))
    for i in range(qty):
        content = format(str(i).zfill(digits))
        img = qrcode.make("{}".format(content))
        img.save("{}/{}.png".format(dir, content))

    return None


# generate qrcode based on HRNo
def hrnoqrcode(dir):
    for i in range(10, 40):
        os.makedirs("{}/{}HR".format(dir, i))
        for j in range(1, 46):
            HRNo = "{}{}".format(i, str(j).zfill(2))
            img = qrcode.make("{}".format(HRNo))
            img.save("{}/{}HR/{}.png".format(dir, i, HRNo))


if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass

    dir_path = openfolder()
    hrnoqrcode(dir_path)
