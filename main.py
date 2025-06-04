import os
import subprocess
from tkinter import *
from backend.patch import run_patcher
from backend.utils import get_launcher_root
from constants import *
from ui.news import create_news_section

root = Tk()
root.geometry("900x500")
root.resizable(False, False)
root.attributes("-alpha", 0.0)

def update_progress(percent):
    fill_width = BAR_X + int(percent * BAR_WIDTH)
    bg_canvas.coords(progress_fill, BAR_X, BAR_Y, fill_width, BAR_Y + BAR_HEIGHT)

def update_status(message):
    bg_canvas.itemconfig(status_text, text=message)
    root.update_idletasks()

def start_patching():
    version_file = os.path.join(get_launcher_root(), "version.dat")
    temp_dir = os.path.join(get_launcher_root(), "temp")

    run_patcher(
        base_url=BASE_URL,
        version_file=version_file,
        temp_dir=temp_dir,
        update_progress=update_progress,
        update_status=update_status
    )

    play_button.config(state="normal", image=play_img_enabled)

def launch_game():
    game_path = os.path.join(get_launcher_root(), "game.exe")
    subprocess.Popen([game_path], shell=True)
    root.destroy()

# Load background and assets
bg_image = PhotoImage(file="assets/background.png")
play_img_enabled = PhotoImage(file="assets/play_enabled.png")
play_img_disabled = PhotoImage(file="assets/play_disabled.png")
bg_canvas = Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
bg_canvas.pack(fill="both", expand=True)
bg_canvas.create_image(0, 0, image=bg_image, anchor="nw")

# Draw progress bar and patch status text
bg_canvas.create_rectangle(BAR_X, BAR_Y, BAR_X + BAR_WIDTH, BAR_Y + BAR_HEIGHT, outline="#444", width=2)
progress_fill = bg_canvas.create_rectangle(BAR_X, BAR_Y, BAR_X, BAR_Y + BAR_HEIGHT, fill="#6a5acd", width=0)
status_text = bg_canvas.create_text(BAR_X + 20, BAR_Y - 20, text="Ready", fill="black", font=("Helvetica", 10), anchor="s")

# Create the play button
play_button = Button(root, image=play_img_enabled, borderwidth=0, state="disabled", command=launch_game)
bg_canvas.create_window(BAR_X + BAR_WIDTH + 20, BAR_Y, anchor="nw", window=play_button)

# Add news section
#create_news_section(bg_canvas, root, BAR_X ,BAR_Y, patch_notes_url=PATCH_NOTES_URL)

# Begin version check and auto patch
#start_patching()

root.mainloop()
