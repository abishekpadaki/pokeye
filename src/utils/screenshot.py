import pyautogui
import os

def capture_screenshot():
    save_path = "data/screenshot.png"
    os.makedirs("data", exist_ok=True)
    screenshot = pyautogui.screenshot()
    screenshot.save(save_path)
    print(f"Screenshot saved at: {save_path}")
    return save_path
