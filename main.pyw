import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
import serial
import queue
import os

feed_queue = queue.Queue()

def update_terminal(feed_queue):
    try:
        with serial.Serial("/dev/ttyUSB0", 115200, timeout=1) as ser:
            while True:
                line = ser.readline()
                if line:
                    feed_queue.put(line.decode("utf-8"))
    except Exception as e:
        feed_queue.put(f"Error: {str(e)}\n")

def refresh_terminal(feed_text_widget):
    try:
        while not feed_queue.empty():
            line = feed_queue.get_nowait()
            feed_text_widget.insert("end", line)
            feed_text_widget.yview("end")
    except Exception as e:
        feed_text_widget.insert("end", f"Error: {str(e)}\n")
    root.after(100, refresh_terminal, feed_text_widget)

def send_command(command):
    if command == "Exit":
        exit()
    if command == "Minimize":
        root.state("iconic")	

    try:
        with serial.Serial("/dev/ttyUSB0", 115200, timeout=1) as ser:
            ser.write(f"{command}\n".encode())
    except Exception as e:
        print(f"Error sending command: {e}")

def button_input(value):
    current = input_var.get()
    input_var.set(current + value)

def clear_input():
    input_var.set("")

def send_input():
    command = input_var.get().strip()
    input_var.set("")
    if command.isdigit():
        formatted_command = f"select -a {command}"
        send_command(formatted_command)
    else:
        send_command(command)

def dummy_action(name):
    print(f"Pressed: {name}")
    send_command(name)
# --- Main Window ---
root = ttk.Window(themename="cosmo")
root.update_idletasks()  # Ensures accurate screen size
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
#root.state("zoomed")
#root.geometry("800x400")
root.title("Serial Terminal with Tabs")
root.resizable(False, False)

# === Top Terminal Feed with Scrollbar ===
terminal_frame = ttk.Frame(root)
terminal_frame.pack(fill=X, side=TOP)

terminal_scrollbar = ttk.Scrollbar(terminal_frame, orient="vertical")
terminal_scrollbar.pack(side=RIGHT, fill=Y)

terminal_feed = ttk.Text(
    terminal_frame,
    wrap="none",
    height=12,
    width=100,
    yscrollcommand=terminal_scrollbar.set
)
terminal_feed.pack(side=LEFT, fill=BOTH, expand=True)
terminal_scrollbar.config(command=terminal_feed.yview)

terminal_thread = threading.Thread(target=update_terminal, args=(feed_queue,))
terminal_thread.daemon = True
terminal_thread.start()
root.after(100, refresh_terminal, terminal_feed)

# === Tabs Section ===
tabs = ttk.Notebook(root)
tabs.pack(fill=BOTH, expand=True)

# === WiFi Tab ===
wifi_tab = ttk.Frame(tabs)
tabs.add(wifi_tab, text="WiFi")

# Keypad + Extra Buttons Grid
top_wifi_frame = ttk.Frame(wifi_tab)
top_wifi_frame.pack(side=LEFT, padx=10, pady=10)

keypad_frame = ttk.Frame(top_wifi_frame)
keypad_frame.pack()

input_var = ttk.StringVar()
input_entry = ttk.Entry(keypad_frame, textvariable=input_var, width=20, font=("Courier", 12))
input_entry.grid(row=0, column=0, columnspan=3, pady=(0, 10))

keypad_buttons = [
    ("1", 1, 0), ("2", 1, 1), ("3", 1, 2),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2),
    ("7", 3, 0), ("8", 3, 1), ("9", 3, 2),
    (";", 4, 0), ("0", 4, 1), ("C", 4, 2),
    ("Enter", 5, 0, 3),
]

for (text, row, col, colspan) in [b if len(b) == 4 else (*b, 1) for b in keypad_buttons]:
    action = clear_input if text == "C" else (send_input if text == "Enter" else lambda v=text: button_input(v))
    btn = ttk.Button(keypad_frame, text=text, command=action, width=6)
    btn.grid(row=row, column=col, columnspan=colspan, padx=2, pady=2, sticky="nsew")

for i in range(6):
    keypad_frame.rowconfigure(i, weight=1)
for i in range(3):
    keypad_frame.columnconfigure(i, weight=1)

# Extra Buttons Grid (WiFi Actions)
wifi_button_grid = ttk.Frame(wifi_tab)
wifi_button_grid.pack(side=LEFT, expand=True, fill=BOTH, padx=10, pady=10)

wifi_buttons = [
    "scanap", "stopscan", "list -a", "attack -t deauth",
    "Stop", "Clear Logs", "Exit", "Minimize"
]

for index, label in enumerate(wifi_buttons):
    row = index // 2
    col = index % 2
    btn = ttk.Button(wifi_button_grid, text=label, command=lambda l=label: dummy_action(l), width=12)
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

for i in range(4):
    wifi_button_grid.rowconfigure(i, weight=1)
for i in range(2):
    wifi_button_grid.columnconfigure(i, weight=1)

# === Bluetooth Tab ===
bt_tab = ttk.Frame(tabs)
tabs.add(bt_tab, text="Bluetooth")

bt_button_grid = ttk.Frame(bt_tab)
bt_button_grid.pack(expand=True, fill=BOTH, padx=20, pady=20)

bt_buttons = [
    "Scan BT", "Pair", "Unpair", "Connect",
    "Disconnect", "Info", "Rename", "Exit"
]

for index, label in enumerate(bt_buttons):
    row = index // 2
    col = index % 2
    btn = ttk.Button(bt_button_grid, text=label, command=lambda l=label: dummy_action(f"bt:{l}"), width=12)
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

for i in range(4):
    bt_button_grid.rowconfigure(i, weight=1)
for i in range(2):
    bt_button_grid.columnconfigure(i, weight=1)


# === Manual input tab ===
mi_tab = ttk.Frame(tabs)
tabs.add(mi_tab, text="Manualinput")

mi_input_var = ttk.StringVar()

# Create a text widget for manual input
mi_textbox = ttk.Text(mi_tab, height=6, width=50, font=("Courier", 12))
mi_textbox.pack(padx=20, pady=(20, 10), fill=X)

# Send button
def send_manual_input():
    command = mi_textbox.get("1.0", "end").strip()
    if command:
        send_command(command)
        terminal_feed.insert("end", f"> {command}\n")
        terminal_feed.yview("end")
        mi_textbox.delete("1.0", "end")

send_button = ttk.Button(mi_tab, text="Send", command=send_manual_input)
send_button.pack(pady=5)

# Open on-screen keyboard
def open_keyboard():
    try:
        if os.name == "nt":  # Windows
            os.system("osk")
        else:  # Linux (adjust as needed)
            os.system("onboard &")
    except Exception as e:
        terminal_feed.insert("end", f"Keyboard Error: {e}\n")

keyboard_button = ttk.Button(mi_tab, text="Open Keyboard", command=open_keyboard)
keyboard_button.pack(pady=5)

# --- Start GUI ---


root.mainloop()
