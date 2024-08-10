import pygetwindow as gw
from pywinauto.application import Application
import keyboard, pyautogui, time

# ---------- MODIFIABLE ----------

default_selected = "selected.txt"   # The default file that runs if you only press Enter
hotkey = "F10"                      # The Hotkey to start Pasting Lines (Example hotkeys: F10, F5, a, b, c, space, enter, ctrl, alt, shift, windows. You can also combine keys using the + operator: ctrl+alt+p, shift+a)

# --------------------------------

selected = default_selected
paste = False
ready = False

# Asks the user to select a file
def select_paste():
    global selected, default_selected

    select_input = input(f"File name: (press Enter without text to select \"{default_selected}\") ")
    if select_input != "": selected = select_input

# Reads the file and makes it a list
def read_file_into_list(filename):
    try:
        with open("pastes/"+filename, 'r') as file:
            lines = file.readlines()
            cleaned_lines = [line.strip() for line in lines]
            return cleaned_lines
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return False

# This switches back to Roblox (Incase the user would accidentaly Switch Tabs)
def switch_to_roblox():
    roblox_windows = [window for window in gw.getWindowsWithTitle("") if "Roblox" in window.title]

    if roblox_windows:
        app = Application().connect(handle=roblox_windows[0]._hWnd)
        app.top_window().set_focus()
    else:
        print("Roblox window not found.")

# This opens the chat and pastes the line
def process_line(line):
    time.sleep(0.3) # The wait is needed so Roblox doesn't freak out

    pyautogui.press('/')
    pyautogui.write(line)
    #time.sleep(0.5)

# Waits for the User to Send the line
def wait_for_enter():
    print("Press Enter to continue...")
    while True:
        if keyboard.is_pressed("enter"):
            break

# This waits for the User to Press the assigned Hotkey (This allows the user to switch to their Roblox tab)
def on_hotkey_press(event):
    global paste, ready

    if ready != True: return
    ready = "done"
    print("Starting to Write!")
    for line in paste:
        print(f"Writing: {line}")
        switch_to_roblox()
        process_line(line)
        wait_for_enter()
    
    print("Done Writing! :D")

# The Main part of the code which runs most of the functions
def main():
    global paste, selected, ready, hotkey

    while paste == False: #This makes the program loop until the User submits a valid File
        select_paste()
        paste = read_file_into_list(selected)
    
    ready = True
    
    print(f"Press {hotkey} to start the program or Esc to stop.")

# Register the hotkey to the on_hotkey_press functiom
keyboard.on_press_key(hotkey, on_hotkey_press)

if __name__ == "__main__":
    main()

# Wait to stop
keyboard.wait("Esc")
