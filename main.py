import pygetwindow as gw
from pywinauto.application import Application
import keyboard, pyautogui, time

# ---------- MODIFIABLE ----------

default_selected = "selected.txt"

# --------------------------------

selected = default_selected
paste = False
ready = False

def select_paste():
    global selected, default_selected

    select_input = input(f"File name: (press Enter without text to select \"{default_selected}\") ")
    if select_input != "": selected = select_input

def switch_to_roblox_old():
    # Search for windows containing "Roblox" in the title
    roblox_windows = [window for window in gw.getWindowsWithTitle("") if "Roblox" in window.title]

    if roblox_windows:
        # Assuming there's only one Roblox window, activate it
        roblox_windows[0].activate()
    else:
        print("Roblox window not found.")

def switch_to_roblox():
    roblox_windows = [window for window in gw.getWindowsWithTitle("") if "Roblox" in window.title]

    if roblox_windows:
        app = Application().connect(handle=roblox_windows[0]._hWnd)
        app.top_window().set_focus()
    else:
        print("Roblox window not found.")


def read_file_into_list(filename):
    try:
        with open("pastes/"+filename, 'r') as file:
            lines = file.readlines()
            cleaned_lines = [line.strip() for line in lines]
            return cleaned_lines
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return False

def process_line(line):
    time.sleep(0.3)

    pyautogui.press('/')
    pyautogui.write(line)
    #time.sleep(0.5)  # Adjust the delay as needed

def wait_for_enter():
    print("Press Enter to continue...")
    while True:
        if keyboard.is_pressed("enter"):
            break

def on_f10_press(event):
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

def main():
    global paste, selected, ready

    while paste == False:
        select_paste()
        paste = read_file_into_list(selected)
    
    ready = True
    
    print("Press F10 to start the program or Esc to stop.")

# Register the hotkey
keyboard.on_press_key("F10", on_f10_press)

if __name__ == "__main__":
    main()

# Wait to stop
keyboard.wait("Esc")