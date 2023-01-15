import copy
import ctypes
import time
import tkinter
import tkinter.filedialog
import tkinter.messagebox

import cv2 as cv
import numpy as np
import pyautogui
from pyzbar.pyzbar import decode

# bgr color dict
color = {
    "blue": (255, 0, 0),
    "green": (0, 255, 0),
    "red": ((0, 0, 255)),
}

# optimized for my shcool
# 11-19HR, 21-29HR, 30-39HR each class has less than 45 students
# inactive=-1 / active=1
status = {
    "11": np.full(45, -1),
    "11": np.full(45, -1),
    "11": np.full(45, -1),
    "12": np.full(45, -1),
    "13": np.full(45, -1),
    "14": np.full(45, -1),
    "15": np.full(45, -1),
    "16": np.full(45, -1),
    "17": np.full(45, -1),
    "18": np.full(45, -1),
    "19": np.full(45, -1),
    "21": np.full(45, -1),
    "22": np.full(45, -1),
    "23": np.full(45, -1),
    "24": np.full(45, -1),
    "25": np.full(45, -1),
    "26": np.full(45, -1),
    "27": np.full(45, -1),
    "28": np.full(45, -1),
    "29": np.full(45, -1),
    "30": np.full(45, -1),
    "31": np.full(45, -1),
    "32": np.full(45, -1),
    "33": np.full(45, -1),
    "34": np.full(45, -1),
    "35": np.full(45, -1),
    "36": np.full(45, -1),
    "37": np.full(45, -1),
    "38": np.full(45, -1),
    "39": np.full(45, -1),
}

last_updated_time = {
    "11": np.full(45, time.time()),
    "11": np.full(45, time.time()),
    "11": np.full(45, time.time()),
    "12": np.full(45, time.time()),
    "13": np.full(45, time.time()),
    "14": np.full(45, time.time()),
    "15": np.full(45, time.time()),
    "16": np.full(45, time.time()),
    "17": np.full(45, time.time()),
    "18": np.full(45, time.time()),
    "19": np.full(45, time.time()),
    "21": np.full(45, time.time()),
    "22": np.full(45, time.time()),
    "23": np.full(45, time.time()),
    "24": np.full(45, time.time()),
    "25": np.full(45, time.time()),
    "26": np.full(45, time.time()),
    "27": np.full(45, time.time()),
    "28": np.full(45, time.time()),
    "29": np.full(45, time.time()),
    "30": np.full(45, time.time()),
    "31": np.full(45, time.time()),
    "32": np.full(45, time.time()),
    "33": np.full(45, time.time()),
    "34": np.full(45, time.time()),
    "35": np.full(45, time.time()),
    "36": np.full(45, time.time()),
    "37": np.full(45, time.time()),
    "38": np.full(45, time.time()),
    "39": np.full(45, time.time()),
}

active_members = {
    "11": [],
    "11": [],
    "11": [],
    "12": [],
    "13": [],
    "14": [],
    "15": [],
    "16": [],
    "17": [],
    "18": [],
    "19": [],
    "21": [],
    "22": [],
    "23": [],
    "24": [],
    "25": [],
    "26": [],
    "27": [],
    "28": [],
    "29": [],
    "30": [],
    "31": [],
    "32": [],
    "33": [],
    "34": [],
    "35": [],
    "36": [],
    "37": [],
    "38": [],
    "39": [],
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


def updatestatus(contents):
    global status, last_updated_time

    max_active = 20

    for content in contents:
        key = [str(content[:2])]
        if (
            time.time()
            - last_updated_time[str(content[:2])][int(content) % 100]
            >= 10
        ):
            if not content in active_members[str(content[:2])]:
                if len(active_members[str(content[:2])]) <= max_active:
                    status[str(content[:2])][int(content) % 100] *= -1
                    last_updated_time[str(content[:2])][
                        int(content) % 100
                    ] = time.time()
                    active_members[str(content[:2])].append(content)
                    print("Append {}".format(content))
                else:
                    print("Up to only 20 people: {}".format(content))
            else:
                last_updated_time[str(content[:2])][
                    int(content) % 100
                ] = time.time()
                active_members[str(content[:2])].remove(content)
                print("Remove {}".format(content))

        else:
            pass

    return None


# read videos with cv2
def readvideo(src):
    global status, last_updated_time

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
            contents, frame = detectqrcode(frame)
            if not len(contents) == 0:
                updatestatus(contents)
            else:
                pass
        else:
            pass

        resized_frame = cv.resize(copy.copy(frame), dsize=(rw, rh))
        resized_frame = cv.flip(resized_frame, 1)
        cv.imshow(window_title, resized_frame)

        if cv.waitKey(1) & 0xFF == 27:
            break

        frame_num += 1

    cap.release()
    cv.destroyAllWindows()

    print(status, active_members, sep=",\n")

    return None


if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass

    print(status, sep=",\n")

    readvideo(0)
