import pyautogui
import time

print("Move your mouse to the search bar in 5 seconds...")
time.sleep(5)
print(f"Search bar coordinates: {pyautogui.position()}")

print("Move your mouse to the first contact result in 5 seconds...")
time.sleep(5)
print(f"First contact coordinates: {pyautogui.position()}")

print("Move your mouse to the message input box in 5 seconds...")
time.sleep(5)
print(f"Message box coordinates: {pyautogui.position()}")
