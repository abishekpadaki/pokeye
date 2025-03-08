import pyautogui
import subprocess
import os

def get_front_window_bounds():
    """
    Returns (x, y, width, height) for the currently frontmost window on macOS.
    """
    script = """
    tell application "System Events"
        set frontApp to first process whose frontmost is true
        tell front window of frontApp
            set {posX, posY} to its position
            set {width, height} to its size
            return (posX as text) & "," & (posY as text) & "," & (width as text) & "," & (height as text)
        end tell
    end tell
    """

    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    print("Raw AppleScript output:", repr(result.stdout))
    coords = result.stdout.strip().split(",")
    # Run AppleScript to get the window bounds
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error fetching window bounds:", result.stderr)
        return None
    
    if len(coords) != 4:
        print(coords)
        print("Could not parse window bounds.")
        return None
    
    # Convert to integers and return
    x, y, w, h = map(int, coords)
    return x, y, w, h

def capture_front_window():
    os.makedirs("data", exist_ok=True)
    save_path = "data/window_screenshot.png"
    
    bounds = get_front_window_bounds()
    if not bounds:
        print("Could not retrieve front window bounds.")
        return
    
    x, y, w, h = bounds
    
    # Take a screenshot of that region
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screenshot.save(save_path)
    print(f"Screenshot of front window saved at: {save_path}")
