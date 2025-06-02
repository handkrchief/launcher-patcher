import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x300")
app.title("Game Launcher")

label = ctk.CTkLabel(app, text="Welcome to the Launcher!")
label.pack(pady=20)

app.mainloop()