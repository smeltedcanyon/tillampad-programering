from pynput import keyboard
from pynput.keyboard import Controller, Key

kb_controller = Controller()

def on_press(key):
    if key == keyboard.Key.end:
        print("Triggering sequence...")
        
        # Press 'z' once
        kb_controller.press('z')
        kb_controller.release('z')
        kb_controller.press('z')
        kb_controller.release('z')
        kb_controller.press('z')
        kb_controller.release('z')
        
        # Press Shift+Enter
        kb_controller.press(Key.shift)
        kb_controller.press(Key.enter)
        kb_controller.release(Key.enter)
        kb_controller.release(Key.shift)
        
        print("Done!")
        return False  # Stop listener

# Start listening to keyboard
with keyboard.Listener(on_press=on_press) as listener:
    print("Press END to trigger sequence...")
    listener.join()
