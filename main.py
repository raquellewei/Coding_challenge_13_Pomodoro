import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox
import random

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#F7A4A4"
RED = "#E97777"
GREEN = "#B6E2A1"
YELLOW = "#FFFBC1"
FONT_NAME = "Comic Sans MS"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECK = "✔"
reps = 0
timer = None

BACK_TO_WORK_MSG=["Back to work, slave!", "You think you have a choice?",
                  "Back to the salt mines!", "Pull your weight!",
                  "Roll up your sleeves!", "Shape up or ship out!",
                  "Step on it!", "Suck it up!", "The clock is ticking!",
                  "Work fingers to the bone!", "Work like a dog!",]

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global current_state
    current_state = 0
    window.after_cancel(timer)
    global reps
    reps = 0
    check_label.config(text="")
    timer_label.config(text="Timer")
    canvas.itemconfig(timer_text, text="00:00")

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global current_state
    if current_state == 1:
        messagebox.showwarning("Playing smart?", "Can't trick your boss!")
        return
    current_state = 1
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        messagebox.showinfo("Long Break", "Time for a cup\n ... ...\n of coffee!")
        timer_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=PINK)
        messagebox.showinfo("Short Break", "Ooh la la!")
    else:
        timer_label.config(text="Work", fg=GREEN)
        while True:
            ans = messagebox.askyesno("Work", random.choice(BACK_TO_WORK_MSG), icon=messagebox.ERROR)
            if isinstance(ans, bool):
                if ans: break
            else:
                if ans == "YES": break
        count_down(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = count // 60
    count_sec = count % 60
    if count_sec < 10:
        count_sec = "0" + str(count_sec)
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    else:
        if reps % 2 == 1:
            current_checks = check_label.cget("text")
            check_label.config(text=f"{current_checks}{CHECK}")
        global current_state
        current_state = 0
        start_timer()

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=20, bg=YELLOW)

canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 92, image=tomato_img)
timer_text = canvas.create_text(100, 110, text="00:00", fill="white", font=(FONT_NAME, 40, "normal"))
canvas.grid(row=2, column=2)

current_state = 0 # 0:not yet started, 1:started
timer_label = tk.Label(text="Timer", font=(FONT_NAME, 35, "bold"), fg=GREEN, bg=YELLOW)
timer_label.grid(row=1, column=2, pady=20)

start_button = tk.Button(text="Start", highlightthickness=0, borderwidth=0, highlightbackground=YELLOW,
                         command=start_timer)
start_button.config(bg=YELLOW)
start_button.grid(row=3, column=1)

reset_button = tk.Button(text="Reset", highlightthickness=0, borderwidth=0, highlightbackground=YELLOW,
                         command=reset_timer)
reset_button.grid(row=3, column=3)

check_label = tk.Label(font=(FONT_NAME, 20, "bold"), fg=GREEN, bg=YELLOW)
check_label.grid(row=4, column=2)


window.mainloop()