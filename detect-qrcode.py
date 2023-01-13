import ctypes
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import copy
import pyautogui
import time

import cv2 as cv
from pyzbar.pyzbar import decode

# bgr color dict
color = {
    "blue": (255, 0, 0),
    "green": (0, 255, 0),
    "red": ((0, 0, 255)),
}


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


# gui folderdialog
def openfolder():
    root = tkinter.Tk()
    root.withdraw()
    dir_path = tkinter.filedialog.askdirectory()

    if not dir_path:
        quit()

    return dir_path


# get capture info
def getcapinfo(cap):
    w, h, f = (
        int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)),
        int(cap.get(cv.CAP_PROP_FPS)),
    )

    return w, h, f


# resize caputre
def resizecap(cap, scale=0.8):
    w, h = (
        int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)),
    )
    displaysize_w, displaysize_h = pyautogui.size()
    available_displaysize_w, available_displaysize_h = (
        int(displaysize_w * scale),
        int(displaysize_h * scale),
    )

    if (w > available_displaysize_w) or (h > available_displaysize_h):
        if w >= h:
            resized_w = available_displaysize_w
            resized_h = int(h * (available_displaysize_w / w))
        else:
            resized_h = available_displaysize_h
            resized_w = int(w * (available_displaysize_h / h))
    else:
        resized_w, resized_h = w, h

    return resized_w, resized_h


# detect qrcode
def detectqrcode(frame):
    contents = []
    qrcodes = decode(frame)
    for qrcode in qrcodes:
        content = qrcode.data.decode("utf-8")
        contents.append(content)

        x, y, w, h = qrcode.rect
        cv.rectangle(frame, (x, y), (x + w, y + h), color["green"], 2)

    return contents, frame


# read videos with cv2


def readvideo(src):
    if src == 0:
        window_title = "marker-tracking [Camera 0]"
    else:
        window_title = "marker-tracking [{}]".format(src)
    timenow = time.strftime("%Y-%m-%d %H%M%S", time.strptime(time.ctime()))
    cap = cv.VideoCapture(src)
    if cap.isOpened() == False:
        print("Error in opening video stream of file")

    w, h, f = getcapinfo(cap)
    rw, rh = resizecap(cap)

    frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_num % (f / 5) == 0:
            contens, frame = detectqrcode(frame)
            print(contens)
        else:
            pass

        resized_frame = cv.resize(copy.copy(frame), dsize=(rw, rh))
        cv.imshow(window_title, resized_frame)

        if cv.waitKey(1) & 0xFF == 27:
            break

        frame_num += 1

    cap.release()
    cv.destroyAllWindows()

    return None


if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass

    readvideo(0)
