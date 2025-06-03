from tkinter import Frame, Text, Scrollbar, LEFT, RIGHT, Y, BOTH, END

def create_news_section(canvas, root, bar_x, bar_y, width=400, height=300, file_path="data/patch_notes.txt"):
    # Create frame to hold the text and scrollbar
    news_frame = Frame(root, width=width, height=height)
    news_frame.pack_propagate(False)

    # Create the Text widget
    news_text = Text(news_frame, wrap='word', font=("Helvetica", 10),
                     cursor="arrow", bg="white", fg="black", bd=1, highlightthickness=0)
    scrollbar = Scrollbar(news_frame, command=news_text.yview)
    news_text.configure(yscrollcommand=scrollbar.set)

    news_text.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Load patch notes from file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        content = "No patch notes found."

    news_text.insert(END, content)
    news_text.config(state='disabled')

    # Embed in canvas above the progress bar
    canvas.create_window(bar_x, bar_y - height - 20, anchor="nw", window=news_frame)
