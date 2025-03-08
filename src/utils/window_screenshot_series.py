import subprocess
import pyautogui
import os
import time
import datetime

def get_front_window_bounds():
    """
    Returns (x, y, width, height) for the currently frontmost window on macOS.
    """
    script = """
    tell application "System Events"
        set frontApp to first process whose frontmost is true
        tell front window of frontApp
            set {posX, posY} to its position
            set {w, h} to its size
            return (posX as text) & "," & (posY as text) & "," & (w as text) & "," & (h as text)
        end tell
    end tell
    """
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error fetching window bounds:", result.stderr)
        return None
    
    coords = [c.strip() for c in result.stdout.strip().split(",")]
    if len(coords) != 4:
        print("Could not parse window bounds.")
        return None
    
    x, y, w, h = map(int, coords)
    return x, y, w, h

def capture_front_window_series(duration=30, interval=5):
    """
    Captures screenshots of the frontmost window every 'interval' seconds
    for a total of 'duration' seconds.
    
    duration: total time (seconds) to keep taking screenshots
    interval: how often (seconds) to take a screenshot
    """
    os.makedirs("data", exist_ok=True)
    
    start_time = time.time()
    while time.time() - start_time < duration:
        bounds = get_front_window_bounds()
        if not bounds:
            print("Could not retrieve front window bounds. Retrying...")
            time.sleep(interval)
            continue
        
        x, y, w, h = bounds
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        
        # Name each screenshot with a timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"data/window_screenshot_{timestamp}.png"
        screenshot.save(save_path)
        
        print(f"Screenshot saved at: {save_path}")
        
        # Wait the specified interval before taking the next screenshot
        time.sleep(interval)
