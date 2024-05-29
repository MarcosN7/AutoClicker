import pyautogui
import time
import tkinter as tk
from pynput import mouse
import threading

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")

        # Initialize the stop event
        self.stop_event = threading.Event()

        # Click position
        self.click_x = 0
        self.click_y = 0

        # Auto clicker status
        self.auto_clicker_running = False
        self.auto_clicker_thread = None

        # Frame for settings
        self.settings_frame = tk.LabelFrame(root, text="Settings")
        self.settings_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Interval options in seconds
        self.interval_options_seconds = [300, 600, 900, 1800]  # 5 mins, 10 mins, 15 mins, 30 mins

        # Convert interval options to minutes
        self.interval_options_minutes = [seconds // 60 for seconds in self.interval_options_seconds]

        # Interval between clicks
        self.interval_label = tk.Label(self.settings_frame, text="Click Interval (minutes):")
        self.interval_label.grid(row=0, column=0, padx=5, pady=5)
        self.interval_var = tk.StringVar(root)
        self.interval_var.set(str(self.interval_options_minutes[0]))  # Default: 5 mins
        self.interval_menu = tk.OptionMenu(self.settings_frame, self.interval_var, *map(str, self.interval_options_minutes))
        self.interval_menu.grid(row=0, column=1, padx=5, pady=5)

        # Click position button
        self.position_button = tk.Button(self.settings_frame, text="Set Click Position", command=self.set_click_position)
        self.position_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # Start and stop buttons
        self.start_button = tk.Button(self.settings_frame, text="Start Auto Clicker", command=self.start_auto_clicker)
        self.start_button.grid(row=2, column=0, padx=5, pady=5, sticky="we")
        self.stop_button = tk.Button(self.settings_frame, text="Stop Auto Clicker", command=self.stop_auto_clicker)
        self.stop_button.grid(row=2, column=1, padx=5, pady=5, sticky="we")
        self.stop_button.config(state=tk.DISABLED)

        # Message label
        self.message_label = tk.Label(root, text="", fg="green")
        self.message_label.pack(padx=10, pady=(0, 10))

    # Callback function for mouse click event
    def on_click(self, x, y, button, pressed):
        if pressed:
            self.click_x = x
            self.click_y = y
            self.message_label.config(text=f"Click position set to ({self.click_x}, {self.click_y})")
            return False  # Stop listener

    # Method to set click position
    def set_click_position(self):
        self.message_label.config(text="Please click the mouse at the desired position on the screen...")
        threading.Thread(target=self.capture_click_position).start()

    # Method to capture click position
    def capture_click_position(self):
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()

    # Method to perform auto-clicking
    def auto_click(self, x, y, interval):
        while self.auto_clicker_running:
            pyautogui.click(x, y)
            print(f"Clicked at ({x}, {y})")
            if self.stop_event.wait(interval):
                break
        print("Auto clicker stopped.")

    # Method to start auto clicker
    def start_auto_clicker(self):
        try:
            interval_minutes = int(self.interval_var.get())
            interval_seconds = self.interval_options_seconds[self.interval_options_minutes.index(interval_minutes)]
        except ValueError:
            self.message_label.config(text="Please enter a valid click interval", fg="red")
            return

        if self.click_x == 0 and self.click_y == 0:
            self.message_label.config(text="Please set the click position", fg="red")
            return

        self.message_label.config(text=f"Auto clicker started. Clicking at ({self.click_x}, {self.click_y}) every {interval_minutes} minutes.")
        self.auto_clicker_running = True
        self.auto_clicker_thread = threading.Thread(target=self.auto_click, args=(self.click_x, self.click_y, interval_seconds))
        self.auto_clicker_thread.start()

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    # Method to stop auto clicker
    def stop_auto_clicker(self):
        if self.auto_clicker_running:
            self.auto_clicker_running = False
            self.stop_event.set()  # Set the event to signal stop
            self.auto_clicker_thread.join()  # Wait for the auto-clicking thread to finish
            self.reset()  # Reset the program to its initial state

    # Method to reset the program to its initial state
    def reset(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.message_label.config(text="Auto clicker stopped. Program reset.")
        self.stop_event.clear()  # Clear the stop event
        self.click_x = 0  # Reset click position
        self.click_y = 0
        self.interval_var.set(str(self.interval_options_minutes[0]))  # Reset interval option
        self.auto_clicker_thread = None  # Reset auto-clicker thread

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()

