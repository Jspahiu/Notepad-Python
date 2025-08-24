import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import os

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
after_id = None
what_tab = 1
counter_tab = 1

tab_texts = {1: ""}
tab_filepaths = {1: ""}
tab_buttons = {}

screen = tk.Tk()
screen.title("Notepad Python - Tab 1")
screen.config(bg=SCREEN_SCREEN_COLOR)
screen.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
screen.resizable(False, True)

def save_file(event=None):
    global filename, what_tab
    filename = tab_filepaths.get(what_tab, "")
    if not filename:
        open_file()
        return
    with open(filename, 'w') as f:
        text2save = textbox.get("1.0", tk.END)
        f.write(text2save)
    messagebox.showinfo("Notepad Python", "File Saved!")

def save_file_auto(event=None):
    global filename
    if not filename:
        return
    with open(filename, 'w') as f:
        text2save = textbox.get("1.0", tk.END)
        f.write(text2save)

def stop_action():
    global after_id
    if after_id:
        screen.after_cancel(after_id)
        after_id = None
        print("Stopped repeating")
    else:
        print("No action to stop")

def open_file(event=None):
    global filename, after_id, what_tab
    filename = filedialog.askopenfilename(initialdir="/", title="Open File", filetypes=(("all files", "*.*"),))
    if not filename:
        return
    tab_filepaths[what_tab] = filename
    screen.title(f"Notepad Python - Tab {what_tab} - {filename}")
    with open(filename, 'r', encoding="utf-8") as contents:
        content = contents.read()
    textbox.delete("1.0", tk.END)
    textbox.insert(tk.END, content)
    messagebox.showinfo("Notepad Python", "File Opened!")
    after_id = screen.after(TIMEOUT, save_file_auto)

def create_file(event=None):
    global filename, after_id, what_tab
    fileobj = filedialog.asksaveasfile(title="Create File", mode='w', defaultextension="*.*")
    if not fileobj:
        return
    fileobj.write("")
    fileobj.close()
    filename = fileobj.name
    tab_filepaths[what_tab] = filename
    screen.title(f"Notepad Python - Tab {what_tab} - {filename}")
    messagebox.showinfo("Notepad Program", "File Created!")
    after_id = screen.after(TIMEOUT, save_file_auto)

def delete_file(event=None):
    global filename, what_tab
    filename = tab_filepaths.get(what_tab, "")
    if not filename:
        open_file()
    else:
        warning = messagebox.askyesno("Notepad Python", "Are you sure?")
        if warning:
            textbox.delete("1.0", tk.END)
            screen.title(f"Notepad Python - Tab {what_tab}")
            os.remove(filename)
            tab_filepaths[what_tab] = ""
            messagebox.showinfo("Notepad Python", "File Deleted!")
        else:
            messagebox.showinfo("Notepad Python", "Deletion Cancelled!")

def exit_program(event=None):
    if messagebox.askyesno("Notepad Python", "Are you sure you want to exit?"):
        screen.destroy()
        screen.quit()
    else:
        messagebox.showinfo("Notepad Python", "Exit Cancelled!")

def go_to_tab(tab_number, event=None):
    global what_tab
    # Save current tab's text before switching
    prev_tab = what_tab
    prev_text = textbox.get("1.0", tk.END)
    tab_texts[prev_tab] = prev_text

    # If the previous tab has a file path, save its text to the file
    prev_filepath = tab_filepaths.get(prev_tab, "")
    if prev_filepath:
        try:
            with open(prev_filepath, 'w', encoding='utf-8') as f:
                f.write(prev_text)
        except Exception as e:
            messagebox.showerror("Notepad Python", f"Error saving file for Tab {prev_tab}:\n{e}")

    if what_tab == tab_number:
        return
    if tab_number not in tab_buttons:
        messagebox.showerror("Notepad Python", "Invalid tab number.")
        return

    what_tab = tab_number
    textbox.delete("1.0", tk.END)

    # If the new tab has a file path and the file exists, load from file
    filepath = tab_filepaths.get(tab_number, "")
    if filepath and os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            textbox.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Notepad Python", f"Error loading file for Tab {tab_number}:\n{e}")
    # Otherwise, load from tab_texts
    elif tab_number in tab_texts:
        textbox.insert(tk.END, tab_texts[tab_number])

    # Update title with file path if it exists
    if filepath:
        screen.title(f"Notepad Python - Tab {tab_number} - {filepath}")
    else:
        screen.title(f"Notepad Python - Tab {tab_number}")

def create_new_tab(event=None):
    global counter_tab, button_kwargs_tab, buttons_padx, tab_buttons
    if counter_tab >= 11:
        messagebox.showwarning("Notepad Python", "Maximum number of tabs reached (11).")
        return

    # Find the next available tab number
    next_tab = 1
    while next_tab in tab_buttons:
        next_tab += 1

    counter_tab = next_tab

    # Remove the add_tab button before packing new tab
    add_tab.pack_forget()

    # Only create if not already present
    if counter_tab not in tab_buttons:
        new_tab_btn = tk.Button(tab_frame, text=f"Tab {counter_tab}", command=lambda n=counter_tab: go_to_tab(n), **button_kwargs_tab)
        tab_buttons[counter_tab] = new_tab_btn
        new_tab_btn.pack(side="left", padx=buttons_padx)
        tab_texts[counter_tab] = ""
        tab_filepaths[counter_tab] = ""

    # Re-add the add_tab button at the end
    add_tab.pack(side="left", padx=buttons_padx)

def delete_tab(event=None):
    global what_tab, counter_tab, tab_buttons
    if len(tab_buttons) <= 1:
        messagebox.showwarning("Notepad Python", "Cannot delete the last tab.")
        return
    if messagebox.askyesno("Notepad Python", f"Are you sure you want to delete Tab {what_tab}?"):
        tab_btn = tab_buttons.get(what_tab)
        if tab_btn:
            tab_btn.destroy()
            del tab_buttons[what_tab]
        if what_tab in tab_texts:
            del tab_texts[what_tab]
        if what_tab in tab_filepaths:
            del tab_filepaths[what_tab]
        # Switch to the lowest remaining tab
        remaining_tabs = sorted(tab_buttons.keys())
        if remaining_tabs:
            go_to_tab(remaining_tabs[0])
        counter_tab = max(remaining_tabs) if remaining_tabs else 1
    else:
        messagebox.showinfo("Notepad Python", "Tab deletion cancelled.")

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

    label_font_size = tk.Label(style_window, text="---- Font Size ----", bg="white", font=("Segoe UI", 15, "bold"))
    label_font_size.pack(pady=20)

    button_frame = tk.Frame(style_window, bg="white")
    button_frame.pack(pady=10)

    LeftButton = tk.Button(button_frame, text="<---", bg="white", command=decrease_size, font=("Segoe UI", 10))
    LeftButton.config(width=10)
    Font_Button = tk.Button(button_frame, text=font_size, bg="white", command=edit_font_size, font=("Segoe UI", 10, "bold"))
    RightButton = tk.Button(button_frame, text="--->", bg="white", command=increase_size, font=("Segoe UI", 10))
    RightButton.config(width=10)

    LeftButton.pack(side="left", padx=0)
    Font_Button.pack(side="left", padx=0)
    RightButton.pack(side="left", padx=0)

    label_font_style = tk.Label(style_window, text="---- Font Style ----", bg="white", font=("Segoe UI", 15, "bold"))
    label_font_style.pack(pady=20)

    button_frame_for_style = tk.Frame(style_window, bg="white")
    button_frame_for_style.pack(pady=10)

    LeftButton_Style = tk.Button(button_frame_for_style, text="<---", bg="white", command=decrease_style, font=("Segoe UI", 10))
    LeftButton_Style.config(width=10)
    Font_Style_Button = tk.Button(button_frame_for_style, text=font_style, bg="white", font=("Segoe UI", 10, "bold"))
    RightButton_Style = tk.Button(button_frame_for_style, text="--->", bg="white", command=increase_style, font=("Segoe UI", 10))
    RightButton_Style.config(width=10)

    LeftButton_Style.pack(side="left", padx=0)
    Font_Style_Button.pack(side="left", padx=0)
    RightButton_Style.pack(side="left", padx=0)

    label_font_color = tk.Label(style_window, text="---- Font Color ----", bg="white", font=("Segoe UI", 15, "bold"))
    label_font_color.pack(pady=20)

    button_frame_for_color = tk.Frame(style_window, bg="white")
    button_frame_for_color.pack(pady=10)

    LeftButton_color = tk.Button(button_frame_for_color, text="<---", bg="white", command=decrease_color, font=("Segoe UI", 10))
    LeftButton_color.config(width=10)
    Font_color_Button = tk.Button(button_frame_for_color, text=font_color, bg=font_color, fg="white", font=("Segoe UI", 10, "bold"))
    RightButton_color = tk.Button(button_frame_for_color, text="--->", bg="white", command=increase_color, font=("Segoe UI", 10))
    RightButton_color.config(width=10)

    LeftButton_color.pack(side="left", padx=0)
    Font_color_Button.pack(side="left", padx=0)
    RightButton_color.pack(side="left", padx=0)

    close_button = tk.Button(style_window, text="Close", command=style_window.destroy)
    close_button.pack(pady=10)

button_frame = tk.Frame(screen, bg="white")
button_frame.pack(anchor="w", padx=5, pady=5)

button_kwargs_buttons = {
    "relief": "flat",
    "borderwidth": 0,
    "highlightthickness": 0,
    "bg": button_frame["bg"],
    "activebackground": button_frame["bg"],
    "padx": 0,
    "pady": 0
}

buttons_padx = 6

btn1 = tk.Button(button_frame, text="Create", command=create_file, **button_kwargs_buttons)
btn1.pack(side="left", padx=buttons_padx)

btn2 = tk.Button(button_frame, text="Open", command=open_file, **button_kwargs_buttons)
btn2.pack(side="left", padx=buttons_padx)

btn3 = tk.Button(button_frame, text="Save", command=save_file, **button_kwargs_buttons)
btn3.pack(side="left", padx=buttons_padx)

btn4 = tk.Button(button_frame, text="Delete", command=delete_file, **button_kwargs_buttons)
btn4.pack(side="left", padx=buttons_padx)

btn5 = tk.Button(button_frame, text="Style", command=style_program, **button_kwargs_buttons)
btn5.pack(side="left", padx=buttons_padx)

btn6 = tk.Button(button_frame, text="Delete Tab", command=delete_tab, **button_kwargs_buttons)
btn6.pack(side="left", padx=buttons_padx)

btn7 = tk.Button(button_frame, text="Exit", command=exit_program, **button_kwargs_buttons)
btn7.pack(side="left", padx=buttons_padx)

textbox = tk.Text(
    screen,
    height=10,
    font=(font_style, font_size),
    bg="white",
    fg=font_color,
    bd=0,
    relief="flat",
    highlightthickness=1,
    highlightbackground="#C0C0C0",
    highlightcolor="#C0C0C0"
)
textbox.pack(fill="both", padx=2, expand=True)

tab_frame = tk.Frame(screen, bg="white", width=SCREEN_WIDTH, height=30)
tab_frame.pack(anchor="w", padx=5, pady=5)

button_kwargs_tab = {
    "relief": "solid",
    "border": 1,
    "highlightthickness": 0,
    "bg": button_frame["bg"],
    "activebackground": button_frame["bg"],
    "padx": 10,
    "pady": 5
}

tab_1 = tk.Button(tab_frame, text="Tab 1", command=lambda: go_to_tab(1), **button_kwargs_tab)
tab_1.pack(side="left", padx=buttons_padx)
tab_buttons[1] = tab_1

add_tab = tk.Button(tab_frame, text="+", command=create_new_tab, **button_kwargs_tab)
add_tab.pack(side="left", padx=buttons_padx)

screen.protocol("WM_DELETE_WINDOW", exit_program)
screen.bind("<Control-s>", save_file)
screen.bind("<Control-o>", open_file)
screen.bind("<Control-t>", create_file)
screen.bind("<Control-d>", delete_file)
screen.bind("<Control-a>", style_program)
screen.bind("<Control-q>", exit_program)

screen.mainloop()