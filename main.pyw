import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
import serial
import queue
import os
import sys

feed_queue = queue.Queue()
workdir = sys.argv[1]	#first argument is workdir
configs = {}            #configs var

def update_terminal(feed_queue):
    try:
        #with serial.Serial("/dev/ttyUSB0", 115200, timeout=1) as ser:
        with serial.Serial(configs["serial_port"], 115200, timeout=1) as ser:
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
        send_command("stopscan")
        exit()
    if command == "Minimize":
        root.state("iconic")	
        return
    if command == "tbd":
        return
    try:
        #with serial.Serial("/dev/ttyUSB0", 115200, timeout=1) as ser:
        with serial.Serial(configs["serial_port"], 115200, timeout=1) as ser:
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

def read_config():
    with open(workdir+"/config.txt") as f:
        lines=f.readlines()
        lines_parsed = []
        for line in lines:
            if line[0] == "#":          #comments start with #
                continue
            elif line[0] == "\n":
                continue
            else:
                lines_parsed.append(line)
        for line in lines_parsed:
            param_key = line.split("=")[0]
            param_value = line.split("=")[1]
            configs.update({param_key.rstrip():param_value.rstrip()})    #key val pairs as a dict should have.

def apply_serial_port():
    selected_serial_port = serial_var.get()  # Get the value from the serial_entry widget
    print(f"Serial Port entered: '{selected_serial_port}'")  # Debugging line

    if selected_serial_port:
        configs["serial_port"] = selected_serial_port  # Update the serial port in the configs

        # Save to config file
        with open(workdir + "/config.txt", "w") as f:
            for key, value in configs.items():
                f.write(f"{key}={value}\n")  # Write the updated config back to the file

        # Update the serial port label with the new value
        serial_label.config(text="Serial Port of ESP32: " + selected_serial_port)  # Update label

        terminal_feed.insert("end", f"Serial Port set to: {selected_serial_port}\n")
        terminal_feed.yview("end")
    else:
        terminal_feed.insert("end", "Error: Invalid serial port\n")
        terminal_feed.yview("end")

def apply_theme(selected_theme):
    global configs
    root.style.theme_use("darkly" if selected_theme == "darkly" else "cosmo")
    configs["theme"] = selected_theme
    # Save to config
    with open(workdir+"/config.txt", "w") as f:
        for key, value in configs.items():
            f.write(key + "=" + value + "\n") 

# Send button
def send_manual_input():
    command = mi_textbox.get("1.0", "end").strip()
    if command:
        send_command(command)
        terminal_feed.insert("end", f"> {command}\n")
        terminal_feed.yview("end")
        mi_textbox.delete("1.0", "end")


def open_keyboard():
    try:
        if os.name == "nt":  # Windows
            os.system("osk")
        else:  # Linux (adjust as needed)
            os.system("onboard &")
    except Exception as e:
        terminal_feed.insert("end", f"Keyboard Error: {e}\n")


# --- Main Window ---
read_config()
if configs["theme"] == "dark" or configs["theme"] == "darkly":
    theme = "darkly"
elif configs["theme"] == "light" or configs["theme"] == "cosmo":
    theme = "cosmo"
root = ttk.Window(themename=theme)
root.update_idletasks()  # Ensures accurate screen size
if root.winfo_screenwidth() > 1920:
    screen_width = 1920
else:
    screen_width = root.winfo_screenwidth()
root.geometry(f"{screen_width}x{root.winfo_screenheight()}+0+0")
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
    "tbd", "tbd", "Exit", "Minimize"
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
    "blespam -t all", "stopscan", "tbd", "tbd",
    "tbd", "tbd", "Exit", "Minimize"
]

for index, label in enumerate(bt_buttons):
    row = index // 2
    col = index % 2
    btn = ttk.Button(bt_button_grid, text=label, command=lambda l=label: dummy_action(l), width=12)
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

for i in range(4):
    bt_button_grid.rowconfigure(i, weight=1)
for i in range(2):
    bt_button_grid.columnconfigure(i, weight=1)


# === Manual input tab ===
mi_tab = ttk.Frame(tabs)
tabs.add(mi_tab, text="Manual input")

mi_input_var = ttk.StringVar()

# Create a text widget for manual input
mi_textbox = ttk.Text(mi_tab, height=6, width=50, font=("Courier", 12))
mi_textbox.pack(padx=20, pady=(20, 10), fill=X)


send_button = ttk.Button(mi_tab, text="Send", command=send_manual_input)
send_button.pack(pady=5)

# Open on-screen keyboard

keyboard_button = ttk.Button(mi_tab, text="Open Keyboard", command=open_keyboard)
keyboard_button.pack(pady=5)

# === Settings Tab ===
settings_tab = ttk.Frame(tabs)
tabs.add(settings_tab, text="Settings")

theme_var = theme


ttk.Label(settings_tab, text="Theme:").pack(pady=(20, 5))

theme_frame = ttk.Frame(settings_tab)
theme_frame.pack()

ttk.Radiobutton(theme_frame, text="Light", variable=theme_var, value="light", command=lambda: apply_theme("cosmo")).pack(side=LEFT, padx=10)
ttk.Radiobutton(theme_frame, text="Dark", variable=theme_var, value="dark", command=lambda: apply_theme("darkly")).pack(side=LEFT, padx=10)

# --- Serial Port Section ---
# Create a Label for Serial Port display
serial_label = ttk.Label(settings_tab, text="Serial Port: " + configs.get("serial_port", "Not Set"))
serial_label.pack(pady=(20, 5))

# Initialize serial_var with the current serial port value
serial_var = ttk.StringVar(value=configs.get("serial_port", ""))  # Get serial port from config or default to empty string

serial_frame = ttk.Frame(settings_tab)
serial_frame.pack()

# Entry widget for serial port input
serial_entry = ttk.Entry(serial_frame, textvariable=serial_var, width=30, font=("Courier", 12))
serial_entry.pack(side=LEFT, padx=10)

# Apply Serial Port Button
apply_serial_button = ttk.Button(serial_frame, text="Apply Port", command=apply_serial_port)
apply_serial_button.pack(side=LEFT, padx=10)

# Button to open the on-screen keyboard
keyboard_button = ttk.Button(serial_frame, text="Open Keyboard", command=open_keyboard)
keyboard_button.pack(side=LEFT, padx=10)



#....More stuff 

# --- Start GUI ---


root.mainloop()
