import os
import subprocess
import threading
from tkinter import *
from backend.patch import run_patcher
from backend.utils import get_launcher_root
from constants import *
from ui.news import create_news_section

# Initialize the main application window
root = Tk()
root.geometry("900x500")
root.resizable(False, False)
root.title("Launcher")

# Update the width of the progress bar fill based on percent (0.0 to 1.0).
def update_progress(percent):
    fill_width = BAR_X + int(percent * BAR_WIDTH)
    bg_canvas.coords(progress_fill, BAR_X, BAR_Y, fill_width, BAR_Y + BAR_HEIGHT)
    root.update_idletasks()

# Update the status text above the progress bar.
def update_status(message):
    bg_canvas.itemconfig(status_text, text=message)

def start_patching():
    # Start the patching process in a separate thread to keep the UI responsive.
    def patching_task():
        version_file = os.path.join(get_launcher_root(), "version.dat")
        temp_dir = os.path.join(get_launcher_root(), "temp")

        # Run the patcher and update UI based on result
        success = run_patcher(
            base_url=BASE_URL,
            version_file=version_file,
            temp_dir=temp_dir,
            update_progress=update_progress,
            update_status=update_status
        )

        if success:
            play_button.config(state="normal", image=play_img_enabled)
            update_status("Game is ready.")
        else:
            update_status("Patching failed. Please try again.")

    threading.Thread(target=patching_task, daemon=True).start()

# Launch the game executable and close the launcher.
def launch_game():
    try:
        subprocess.Popen(["./game.exe"])
        root.destroy()
    except Exception as e:
        print(f"Failed to launch game: {e}")
        
# Load background and button images
bg_image = PhotoImage(file="assets/background.png")
play_img_enabled = PhotoImage(file="assets/play_enabled.png")
play_img_disabled = PhotoImage(file="assets/play_disabled.png")

# Create the main canvas for background and UI elements
bg_canvas = Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
bg_canvas.pack(fill="both", expand=True)
bg_canvas.create_image(0, 0, image=bg_image, anchor="nw")

# Draw the progress bar and status text
bg_canvas.create_rectangle(BAR_X, BAR_Y, BAR_X + BAR_WIDTH, BAR_Y + BAR_HEIGHT, outline="#444", width=2)
progress_fill = bg_canvas.create_rectangle(BAR_X, BAR_Y, BAR_X, BAR_Y + BAR_HEIGHT, fill="#6a5acd", width=0)
status_text = bg_canvas.create_text(BAR_X + BAR_WIDTH // 2, BAR_Y - 20, text="Ready", fill="#fff8e7", font=("Helvetica", 10), anchor="s")

# Create the play button (disabled until patching is complete)
play_button = Button(
    root,
    borderwidth=0,
    state="disabled",
    command=launch_game,
    text="Play",
    image=play_img_disabled,
    highlightthickness=0,
    background="#666666"
)
bg_canvas.create_window(BAR_X + BAR_WIDTH + 20, BAR_Y, anchor="nw", window=play_button)

# Add the news/patch notes section to the UI
create_news_section(bg_canvas, root, NEWS_X, NEWS_Y, patch_notes_url=PATCH_NOTES_URL)

# Begin version check and auto patch after a short delay
update_status("Checking for updates...")
root.after(3000, start_patching)

# Start the Tkinter event loop
root.mainloop()