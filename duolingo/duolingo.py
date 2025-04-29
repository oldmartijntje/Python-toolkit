import tkinter as tk
from tkinter import messagebox
import threading
import webbrowser
import time
from datetime import datetime, timedelta

NOTIFY_TIMES = ["13:00", "17:00", "20:00", "21:00", "22:00", "23:00", "23:30", "23:45", "23:50", "23:55"]
duolingo_url = "https://www.duolingo.com"

popup_open = False
lesson_done = False
current_day = datetime.now().date()
last_popup_time = None


def open_duolingo():
    webbrowser.open(duolingo_url)


def popup():
    global popup_open, lesson_done, last_popup_time
    if popup_open or lesson_done:
        return

    now = datetime.now()
    if last_popup_time and now - last_popup_time < timedelta(minutes=1):
        return

    popup_open = True
    last_popup_time = now

    def on_yes():
        global lesson_done, popup_open
        lesson_done = True
        popup_open = False
        root.destroy()

    def on_no(openDuolingo=True):
        global popup_open
        if openDuolingo:
            open_duolingo()
        popup_open = False
        root.destroy()

    def on_close():
        on_no(False)

    root = tk.Tk()
    root.title("Duolingo Check-in")
    root.geometry("300x150")
    root.attributes("-topmost", True)
    root.protocol("WM_DELETE_WINDOW", on_close)

    label = tk.Label(root, text="Did you do your Duolingo lesson today?", wraplength=250)
    label.pack(pady=20)

    button_frame = tk.Frame(root)
    button_frame.pack()

    yes_button = tk.Button(button_frame, text="Yes", command=on_yes, width=10)
    yes_button.grid(row=0, column=0, padx=10)

    no_button = tk.Button(button_frame, text="No", command=on_no, width=10)
    no_button.grid(row=0, column=1, padx=10)

    root.mainloop()


def time_check_loop():
    global current_day, lesson_done

    while True:
        now = datetime.now()
        # Reset lesson_done if day has changed
        if now.date() != current_day:
            current_day = now.date()
            lesson_done = False

        current_time_str = now.strftime("%H:%M")
        if current_time_str in NOTIFY_TIMES:
            threading.Thread(target=popup).start()
            time.sleep(1)
        else:
            time.sleep(30)


if __name__ == "__main__":
    threading.Thread(target=time_check_loop, daemon=True).start()
    while True:
        time.sleep(1)
