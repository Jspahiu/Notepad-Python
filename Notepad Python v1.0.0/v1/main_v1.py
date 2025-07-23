import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog

PROGRAM_NAME = "Notepad Python"
PROGRAM_VERSION = "1.0.0"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
SCREEN_SCREEN_COLOR = 'white'
TIMEOUT = 10 * 1000  # 10 seconds
STYLES = ["Segoe UI", "Arial", "Courier New", "Times New Roman", "Verdana", "Tahoma", "Georgia", "Impact", "Comic Sans MS", "Garamond"]
COLORS = ["Black", "Red", "Green", "Blue", "Cyan", "Magenta", "Yellow", "Gray", "White"]

font_size = 11
font_color = "Black"
font_style = "Segoe UI"

filename = ""
after_id = None  # Initialize after_id to None

screen = tk.Tk()
screen.title("Notepad Python")
screen.config(bg=SCREEN_SCREEN_COLOR)
screen.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")





def save_file(event=None):
    global filename
    if filename == "" or filename is None:
        open_file()
    else:
        if filename is None or filename == "":
            return
        with open(filename, 'w') as f:
            text2save = textbox.get("1.0", tk.END)
            f.write(text2save)
        messagebox.showinfo("Notepad Python", "File Saved!")

def save_file_auto(event=None):
    global filename
    if filename is None or filename == "":
        return
    with open(filename, 'w') as f:
        text2save = textbox.get("1.0", tk.END)
        f.write(text2save)
    #messagebox.showinfo("Notepad Python", "File Saved!")

def stop_action():
    if after_id:
        screen.after_cancel(after_id)
        print("Stopped repeating")
        after_id = None
        return
    else:
        print("No action to stop")
        return


def open_file(event=None):
    global filename, after_id
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Open File",
                                          filetypes = (("all files",
                                                        "*.*"),
                                                       ("all files",
                                                        "*.*")))
    if filename == "" or filename is None:
        return
    else:
        screen.title(f"Notepad Python - {filename}")
        with open(filename, 'r', encoding="utf-8") as contents:
                content = contents.read()
        textbox.delete("1.0", tk.END)  # Delete all existing text
        textbox.insert(tk.END, content)  # Insert new text
        print(filename)
        messagebox.showinfo("Notepad Python", "File Opened!")
        #screen.after(TIMEOUT, save_file_auto)
        after_id = screen.after(TIMEOUT, save_file_auto)  # Schedule again in 1 second  

def create_file(event=None):
    global filename, after_id
    filename = filedialog.asksaveasfile(title = "Create File", mode='w', defaultextension="*.*")
    print(filename)
    if filename is None or filename == "": # asksaveasfile return `None` if dialog closed with "cancel".
        return
    else:
        filename.write("")
        filename.close()
        filename = filename.name
        screen.title(f"Notepad Python - {filename}")
        messagebox.showinfo("Notepad Program", "File Created!")
        #screen.after(TIMEOUT, save_file_auto)
        after_id = screen.after(TIMEOUT, save_file_auto)  # Schedule again in 1 second

def delete_file(event=None):
    if filename == "" or filename is None:
        open_file()
    else:
        warning = messagebox.askyesno("Notepad Python", "Are you sure?")
        if warning:
            textbox.delete("1.0", tk.END)
            screen.title("Notepad Python")
            print("Did IT!")
            messagebox.showinfo("Notepad Python", "File Deleted!")
        else:
            messagebox.showinfo("Notepad Python", "Deletion Cancelled!")

def exit_program(event=None):
    if messagebox.askyesno("Notepad Python", "Are you sure you want to exit?"):
        screen.destroy()
        screen.quit()
    else:
        messagebox.showinfo("Notepad Python", "Exit Cancelled!")

def style_program(event=None):
    global font_size, font_color, font_style
    style_window = tk.Toplevel()
    style_window.title("Style Program")
    style_window.geometry("500x600")
    style_window.config(bg="white")

    label = tk.Label(style_window, text="Style Options", bg="white", font=("Segoe UI", 20, "bold"))
    label.pack(pady=20)

    # --------------------- Close Button ---------------------

    # Close button below everything
    close_button = tk.Button(style_window, text="Close", command=style_window.destroy)
    close_button.pack(pady=10)


# Button row container
button_frame = tk.Frame(screen, bg="white")
button_frame.pack(anchor="w", padx=5, pady=5)

# Reusable button style
button_kwargs = {
    "relief": "flat",
    "borderwidth": 0,
    "highlightthickness": 0,
    "bg": button_frame["bg"],
    "activebackground": button_frame["bg"],
    "padx": 0,
    "pady": 0
}

buttons_padx = 6

# Buttons
btn1 = tk.Button(button_frame, text="Create", command=create_file, **button_kwargs)
btn1.pack(side="left", padx=buttons_padx)

btn2 = tk.Button(button_frame, text="Open", command=open_file, **button_kwargs)
btn2.pack(side="left", padx=buttons_padx)

btn3 = tk.Button(button_frame, text="Save", command=save_file, **button_kwargs)
btn3.pack(side="left", padx=buttons_padx)

btn4 = tk.Button(button_frame, text="Delete", command=delete_file, **button_kwargs)
btn4.pack(side="left", padx=buttons_padx)

btn5 = tk.Button(button_frame, text="Style", command=style_program, **button_kwargs)
btn5.pack(side="left", padx=buttons_padx)

btn6 = tk.Button(button_frame, text="Exit", command=exit_program, **button_kwargs)
btn6.pack(side="left", padx=buttons_padx)


# Text area
textbox = tk.Text(
    screen,
    font=(font_style, font_size),
    bg="white",
    fg=font_color,
    bd=0,                        # No built-in border
    relief="flat",              # Flat edge
    highlightthickness=1,       # Thin border
    highlightbackground="#C0C0C0",  # Light gray when not focused
    highlightcolor="#C0C0C0"        # Same gray when focused
)
textbox.pack(fill="both", padx=2, expand=True)






screen.protocol("WM_DELETE_WINDOW", exit_program)
screen.bind("<Control-s>", save_file)
screen.bind("<Control-o>", open_file)
screen.bind("<Control-t>", create_file)
screen.bind("<Control-d>", delete_file)
screen.bind("<Control-a>", style_program)
screen.bind("<Control-q>", exit_program)

screen.mainloop()
