import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style
from ttkbootstrap.widgets import Meter
from tkinter import ttk
from plyer import notification
import os
import platform

WORK_TIME = 50 * 60
SHORT_BREAK_TIME = 10 * 60
LONG_BREAK_TIME = 60 * 60

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x370")
        self.root.title("Pomodoro Timer")
        
        # Dark theme
        self.style = Style(theme="cyborg")

        # Session label
        self.session_label = ttk.Label(
            self.root, text="Pomodoro #0", font=("Segoe UI", 16, "bold"),
             foreground="white"
        )
        self.session_label.pack(pady=(15, 5))

        # Timer label
        self.timer_label = ttk.Label(
            self.root, text="50:00", font=("Segoe UI", 36, "bold"),
             foreground="white"
        )
        self.timer_label.pack(pady=(0, 20))

        # Progress meter
        self.meter = Meter(
            self.root,
            amountused=0,
            metertype='full',
            subtext='Progress',
            interactive=False,
            textright='%',
            stripethickness=15,
            metersize=200,
            bootstyle='success'
        )
        self.meter.pack(pady=10)

        # Buttons frame
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10)

        # Start button
        self.start_button = ttk.Button(
            self.button_frame, text="Start", command=self.start_timer,
            bootstyle="success-outline", width=12
        )
        self.start_button.grid(row=0, column=0, padx=10)

        # Stop button
        self.stop_button = ttk.Button(
            self.button_frame, text="Stop", command=self.stop_timer,
            bootstyle="danger-outline", state=tk.DISABLED, width=12
        )
        self.stop_button.grid(row=0, column=1, padx=10)

        # Timer variables
        self.work_time = WORK_TIME
        self.break_time = SHORT_BREAK_TIME
        self.is_work_time = True
        self.pomodoros_completed = 0
        self.is_running = False

        self.root.mainloop()

    def start_timer(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.is_running = True
        self.update_timer()
    
    def stop_timer(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.is_running = False

    def play_sound(self):
        """Simple cross-platform beep"""
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 300)
        else:
            # Linux / Mac
            os.system('printf "\a"')  # simple system beep

    def send_notification(self, title, message):
        """Desktop notification using plyer"""
        notification.notify(
            title=title,
            message=message,
            timeout=5  # seconds
        )

    def update_timer(self):
        if self.is_running:
            total_time = self.work_time if self.is_work_time else self.break_time
            max_time = WORK_TIME if self.is_work_time else (LONG_BREAK_TIME if self.pomodoros_completed % 4 == 0 else SHORT_BREAK_TIME)
            
            if self.is_work_time:
                self.work_time -= 1
                if self.work_time == 0:
                    self.is_work_time = False
                    self.pomodoros_completed += 1
                    self.break_time = LONG_BREAK_TIME if self.pomodoros_completed % 4 == 0 else SHORT_BREAK_TIME
                    self.play_sound()
                    self.send_notification(
                        "Break Time!",
                        "Take a long break." if self.pomodoros_completed % 4 == 0 else "Take a short break!"
                    )
                    messagebox.showinfo(
                        "Great job!" if self.pomodoros_completed % 4 == 0 else "Good job!",
                        "Take a long break and rest your mind." if self.pomodoros_completed % 4 == 0
                        else "Take a short break and stretch your legs!"
                    )
            else:
                self.break_time -= 1
                if self.break_time == 0:
                    self.is_work_time = True
                    self.work_time = WORK_TIME
                    self.play_sound()
                    self.send_notification("Work Time!", "Get back to work!")
                    messagebox.showinfo("Work Time", "Get back to work!")

            # Update labels
            minutes, seconds = divmod(self.work_time if self.is_work_time else self.break_time, 60)
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.session_label.config(text=f"Pomodoro #{self.pomodoros_completed + (0 if self.is_work_time else 0)}")

            # Update meter and color
            progress = int(((max_time - total_time) / max_time) * 100)
            meter_color = 'success' if self.is_work_time else 'info'
            self.meter.configure(amountused=progress, bootstyle=meter_color)

            self.root.after(1000, self.update_timer)

PomodoroTimer()