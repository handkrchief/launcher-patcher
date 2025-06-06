import requests
from tkinter import Frame, Text, Scrollbar, LEFT, RIGHT, Y, BOTH, END

def create_news_section(canvas, root, bar_x, bar_y, patch_notes_url, width=325, height=225):
    # Create frame to hold the text and scrollbar
    news_frame = Frame(root, width=width, height=height)
    news_frame.pack_propagate(False)

    news_text = Text(news_frame, wrap='word', font=("Helvetica", 10),
                     cursor="arrow", bg="#3f2832", fg="#fff8e7", bd=0, highlightthickness=0)
    scrollbar = Scrollbar(news_frame, command=news_text.yview)
    news_text.configure(yscrollcommand=scrollbar.set)

    news_text.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Fetch patch notes from URL
    try:
        response = requests.get(patch_notes_url, timeout=10)
        response.raise_for_status()
        content = response.text.strip()
    except requests.exceptions.RequestException:
        content = "Failed to load patch notes."

    news_text.insert(END, content)
    news_text.config(state='disabled')

    # Embed in canvas above the progress bar
    canvas.create_window(bar_x, bar_y, anchor="nw", window=news_frame)