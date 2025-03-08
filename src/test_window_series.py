from utils.window_screenshot_series import capture_front_window_series
import time
print('Capture starting in 5 seconds...')
# Wait 5 seconds before starting the capture
time.sleep(5)
# Capture screenshots for 30 seconds, taking a screenshot every 5 seconds
capture_front_window_series(duration=180, interval=3)
