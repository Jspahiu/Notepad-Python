import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog

PROGRAM_NAME = "Notepad Python"
PROGRAM_VERSION = "2.0.0"
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

    def decrease_size():
        global font_size
        if font_size > 0:
            font_size -= 1
            Font_Button.config(text=font_size)
            textbox.config(font=("Segoe UI", font_size))
    
    def edit_font_size():
        global font_size
        new_size = simpledialog.askinteger("Font Size", "Enter new font size:", initialvalue=font_size)
        if new_size is not None and new_size > 0:
            font_size = new_size
            Font_Button.config(text=font_size)
            textbox.config(font=("Segoe UI", font_size))

    def increase_size():
        global font_size
        font_size += 1
        Font_Button.config(text=font_size)
        textbox.config(font=("Segoe UI", font_size))
    
    def decrease_style():
        global font_style, font_size, STYLES
        current_index = STYLES.index(font_style)
        new_index = (current_index - 1) % len(STYLES)
        font_style = STYLES[new_index]
        Font_Style_Button.config(text=font_style)
        textbox.config(font=(font_style, font_size))
    
    def increase_style():
        global font_style, font_size, STYLES
        current_index = STYLES.index(font_style)
        new_index = (current_index + 1) % len(STYLES)
        font_style = STYLES[new_index]
        Font_Style_Button.config(text=font_style)
        textbox.config(font=(font_style, font_size))

    def decrease_color():
        global font_color, COLORS
        Font_color_Button.config(fg="black")
        current_index = COLORS.index(font_color)
        new_index = (current_index - 1) % len(COLORS)
        font_color = COLORS[new_index]
        Font_color_Button.config(text=font_color)
        textbox.config(fg=font_color)
        if font_color.lower() == "white":
            Font_color_Button.config(fg="black", bg=font_color.lower())
        elif font_color.lower() == "black":
            Font_color_Button.config(fg="white", bg=font_color.lower())
        elif font_color.lower() == "yellow":
            Font_color_Button.config(fg="black", bg=font_color.lower())
        elif font_color.lower() == "blue":
            Font_color_Button.config(fg="white", bg=font_color.lower())
        elif font_color.lower() == "green":
            Font_color_Button.config(fg="white", bg=font_color.lower())
        else:
            Font_color_Button.config(bg=font_color.lower())

    def increase_color():
        global font_color, COLORS
        Font_color_Button.config(fg="black")
        current_index = COLORS.index(font_color)
        new_index = (current_index + 1) % len(COLORS)
        font_color = COLORS[new_index]
        Font_color_Button.config(text=font_color)
        textbox.config(fg=font_color)
        if font_color.lower() == "white":
            Font_color_Button.config(fg="black", bg=font_color.lower())
        elif font_color.lower() == "black":
            Font_color_Button.config(fg="white", bg=font_color.lower())
        elif font_color.lower() == "yellow":
            Font_color_Button.config(fg="black", bg=font_color.lower())
        elif font_color.lower() == "blue":
            Font_color_Button.config(fg="white", bg=font_color.lower())
        elif font_color.lower() == "green":
            Font_color_Button.config(fg="white", bg=font_color.lower())
        else:
            Font_color_Button.config(bg=font_color.lower())


    label = tk.Label(style_window, text="Style Options", bg="white", font=("Segoe UI", 20, "bold"))
    label.pack(pady=20)

    # --------------------- Font Size Section ---------------------

    label_font_size = tk.Label(style_window, text="---- Font Size ----", bg="white", font=("Segoe UI", 15, "bold"))
    label_font_size.pack(pady=20)

    # Frame to hold the buttons in a single centered row
    button_frame = tk.Frame(style_window, bg="white")
    button_frame.pack(pady=10)

    LeftButton = tk.Button(button_frame, text="<---", bg="white", command=decrease_size, font=("Segoe UI", 10))
    LeftButton.config(width=10)  # Set width for better alignment
    Font_Button = tk.Button(button_frame, text=font_size, bg="white", command=edit_font_size, font=("Segoe UI", 10, "bold"))
    RightButton = tk.Button(button_frame, text="--->", bg="white", command=increase_size, font=("Segoe UI", 10))
    RightButton.config(width=10)

    # Pack the buttons side by side (tight layout)
    LeftButton.pack(side="left", padx=0)
    Font_Button.pack(side="left", padx=0)
    RightButton.pack(side="left", padx=0)

    # --------------------- Font Style Section ---------------------

    label_font_style = tk.Label(style_window, text="---- Font Style ----", bg="white", font=("Segoe UI", 15, "bold"))
    label_font_style.pack(pady=20)

    button_frame_for_style = tk.Frame(style_window, bg="white")
    button_frame_for_style.pack(pady=10)

    LeftButton_Style = tk.Button(button_frame_for_style, text="<---", bg="white", command=decrease_style, font=("Segoe UI", 10))
    LeftButton_Style.config(width=10)  # Set width for better alignment
    Font_Style_Button = tk.Button(button_frame_for_style, text=font_style, bg="white", font=("Segoe UI", 10, "bold"))
    RightButton_Style = tk.Button(button_frame_for_style, text="--->", bg="white", command=increase_style, font=("Segoe UI", 10))
    RightButton_Style.config(width=10)

    # Pack the buttons side by side (tight layout)
    LeftButton_Style.pack(side="left", padx=0)
    Font_Style_Button.pack(side="left", padx=0)
    RightButton_Style.pack(side="left", padx=0)

    # --------------------------  Font color section --------------------------

    label_font_color = tk.Label(style_window, text="---- Font Color ----", bg="white", font=("Segoe UI", 15, "bold"))
    label_font_color.pack(pady=20)

    button_frame_for_color = tk.Frame(style_window, bg="white")
    button_frame_for_color.pack(pady=10)

    LeftButton_color = tk.Button(button_frame_for_color, text="<---", bg="white", command=decrease_color, font=("Segoe UI", 10))
    LeftButton_color.config(width=10)  # Set width for better alignment
    Font_color_Button = tk.Button(button_frame_for_color, text=font_color, bg=font_color, fg="white", font=("Segoe UI", 10, "bold"))
    RightButton_color = tk.Button(button_frame_for_color, text="--->", bg="white", command=increase_color, font=("Segoe UI", 10))
    RightButton_color.config(width=10)

    # Pack the buttons side by side (tight layout)
    LeftButton_color.pack(side="left", padx=0)
    Font_color_Button.pack(side="left", padx=0)
    RightButton_color.pack(side="left", padx=0)

    button_frame_for_color_rgb = tk.Frame(style_window, bg="white")
    button_frame_for_color_rgb.pack(pady=10)

    # RGB color buttons
    def set_color(color):   
        global font_color
        font_color = color
        Font_color_Button.config(text=font_color)
        textbox.config(fg=font_color)


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
