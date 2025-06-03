from tkinter import *
from constants import *
from ui.news import create_news_section

root = Tk()
root.title("Launcher")
root.geometry("900x500")
root.resizable(False, False)
root.attributes("-alpha", 0.0)

# Load background
bg_image = PhotoImage(file="assets/background.png")
bg_canvas = Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
bg_canvas.pack(fill="both", expand=True)
bg_canvas.create_image(0, 0, image=bg_image, anchor="nw")

# Draw progress bar
bg_canvas.create_rectangle(BAR_X, BAR_Y, BAR_X + BAR_WIDTH, BAR_Y + BAR_HEIGHT, outline="#444", width=2)
progress_fill = bg_canvas.create_rectangle(BAR_X, BAR_Y, BAR_X, BAR_Y + BAR_HEIGHT, fill="#6a5acd", width=0)

# Dummy update function
def update_progress(percent):
    fill_width = BAR_X + int(percent * BAR_WIDTH)
    bg_canvas.coords(progress_fill, BAR_X, BAR_Y, fill_width, BAR_Y + BAR_HEIGHT)

# Add news section
create_news_section(bg_canvas, root, BAR_X ,BAR_Y)

root.mainloop()
