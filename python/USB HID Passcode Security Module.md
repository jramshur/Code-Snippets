
# **USB HID Passcode Security Module**

## Purpose
This code implements a **passcode system** using physical buttons, a NeoPixel for visual feedback, and a HID (Human Interface Device) keyboard for sending character sequences upon successful authentication. It is designed for microcontroller-based platforms (e.g., CircuitPython). 

## **Key Features**

1. **Passcode Authentication**:
   - Users input a passcode using physical buttons.
   - The system validates the input against the expected passcode.

2. **Visual Feedback**:
   - A NeoPixel provides immediate feedback:
     - **Green** for a correct passcode.
     - **Red** for an incorrect passcode.
     - **Yellow** when the system is locked due to too many failed attempts.

3. **Keyboard Emulation**:
   - Upon successful passcode entry, the system sends a customizable sequence of characters (e.g., "Hello123!@#") via USB as if typed on a keyboard.

4. **Timeout and Lockout**:
   - Clears partial input if no activity is detected within a specified timeout period.
   - Temporarily locks the system after exceeding a maximum number of incorrect attempts.

## **Use Cases**
- **Secure Access Control**: Use it as a passcode-protected interface for controlling access to devices or systems.
- **Custom Keyboard Input**: Automate typing specific strings or commands when the correct passcode is entered.
- **Learning and Pro

# Solutions

## **Solution 1: Class-Based Solution**

### **Overview**
The class-based solution organizes the passcode system into a single class, `PasscodeSystem`. This approach encapsulates the state and behavior, making the code modular, reusable, and scalable.

---

### **Code Components**

#### **1. Constants**
- Defined at the top for easy configuration:
  - `PASSCODE`: The required sequence of button presses.
  - `BUTTON_PINS`: GPIO pins connected to the buttons.
  - `TIMEOUT`, `MAX_ATTEMPTS`, and `LOCKOUT_TIME`: Control timeout and lockout behavior.
  - `NEOPIXEL_COLOR_GREEN`, `NEOPIXEL_COLOR_RED`, `NEOPIXEL_COLOR_YELLOW`: Colors for NeoPixel feedback.
  - `CHARACTER_SEQUENCE`: The keyboard sequence sent on a correct passcode.

#### **2. `PasscodeSystem` Class**
Encapsulates all functionality:
- **Attributes**:
  - `self.data`: Tracks the current button press sequence.
  - `self.attempts`: Counts incorrect attempts.
  - `self.pixel`: Controls the NeoPixel for feedback.
  - `self.keyboard`: Sends keyboard input via HID.
  - `self.buttons`: A list of debounced buttons.

- **Methods**:
  - `_init_buttons(pins)`: Initializes debounced buttons.
  - `show_feedback(color, duration=1)`: Controls NeoPixel feedback.
  - `send_character_sequence(sequence)`: Sends a character sequence via HID.
  - `check_passcode()`: Validates the entered passcode and handles success/failure.
  - `run()`: The main loop handling user input and logic.

---

### **Usage**

#### Configuration
Update constants like `PASSCODE`, `BUTTON_PINS`, or `CHARACTER_SEQUENCE` to fit your system.

#### Run the System
```python
passcode_system = PasscodeSystem(PASSCODE, BUTTON_PINS, TIMEOUT, MAX_ATTEMPTS, LOCKOUT_TIME)
passcode_system.run()
```

---

### **Complete Code**
```python
import board
import digitalio
import neopixel
from adafruit_debouncer import Debouncer
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Constants for configuration
PASSCODE = [0, 1, 2]
BUTTON_PINS = [board.D0, board.D1, board.D2]
TIMEOUT = 5
MAX_ATTEMPTS = 3
LOCKOUT_TIME = 10
NEOPIXEL_COLOR_GREEN = (0, 255, 0)
NEOPIXEL_COLOR_RED = (255, 0, 0)
NEOPIXEL_COLOR_YELLOW = (255, 255, 0)
CHARACTER_SEQUENCE = "Hello123!@#"

class PasscodeSystem:
    def __init__(self, passcode, button_pins, timeout, max_attempts, lockout_time):
        self.passcode = passcode
        self.timeout = timeout
        self.max_attempts = max_attempts
        self.lockout_time = lockout_time

        self.data = []
        self.last_press_time = time.monotonic()
        self.attempts = 0

        self.pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
        self.keyboard = Keyboard(usb_hid.devices)
        self.buttons = self._init_buttons(button_pins)

    def _init_buttons(self, pins):
        buttons = []
        for pin in pins:
            pin_input = digitalio.DigitalInOut(pin)
            pin_input.direction = digitalio.Direction.INPUT
            pin_input.pull = digitalio.Pull.UP
            buttons.append(Debouncer(pin_input))
        return buttons

    def show_feedback(self, color, duration=1):
        self.pixel.fill(color)
        time.sleep(duration)
        self.pixel.fill((0, 0, 0))

    def send_character_sequence(self, sequence):
        special_char_map = {"!": (Keycode.SHIFT, Keycode.ONE)}
        digit_map = {"0": Keycode.ZERO}

        for char in sequence:
            if char.isupper():
                self.keyboard.press(Keycode.SHIFT, getattr(Keycode, char.upper()))
            elif char.islower():
                self.keyboard.press(getattr(Keycode, char.upper()))
            elif char in digit_map:
                self.keyboard.press(digit_map[char])
            elif char in special_char_map:
                self.keyboard.press(*special_char_map[char])
            self.keyboard.release_all()
            time.sleep(0.1)

    def check_passcode(self):
        if self.data == self.passcode:
            print("Passcode correct.")
            self.show_feedback(NEOPIXEL_COLOR_GREEN)
            self.send_character_sequence(CHARACTER_SEQUENCE)
            self.attempts = 0
        else:
            print("Incorrect passcode!")
            self.show_feedback(NEOPIXEL_COLOR_RED)
            self.attempts += 1
        self.data.clear()

    def run(self):
        while True:
            if self.attempts >= self.max_attempts:
                print("System locked.")
                self.show_feedback(NEOPIXEL_COLOR_YELLOW, self.lockout_time)
                self.attempts = 0

            for index, button in enumerate(self.buttons):
                button.update()
                if button.fell:
                    self.data.append(index)
                    self.last_press_time = time.monotonic()
                    print(f"Button {index} pressed.")
                    if len(self.data) == len(self.passcode):
                        self.check_passcode()

            if self.data and (time.monotonic() - self.last_press_time > self.timeout):
                print("Timeout!")
                self.data.clear()

# Instantiate and run
passcode_system = PasscodeSystem(PASSCODE, BUTTON_PINS, TIMEOUT, MAX_ATTEMPTS, LOCKOUT_TIME)
passcode_system.run()
```

---

## **Solution 2: Non-Class Solution**

### **Overview**
The non-class solution uses standalone functions and global variables to implement the passcode system. This approach is simpler and more suitable for smaller projects.

---

### **Code Components**

#### **1. Constants**
- `PASSCODE`, `BUTTON_PINS`, `TIMEOUT`, `MAX_ATTEMPTS`, `LOCKOUT_TIME`, and NeoPixel colors.

#### **2. Global Variables**
- `data`, `last_press_time`, `attempts`.

#### **3. Functions**
- `init_buttons(pins)`: Sets up debounced buttons.
- `show_feedback(color, duration=1)`: Controls NeoPixel feedback.
- `send_character_sequence(sequence)`: Sends a character sequence via HID.
- `check_passcode()`: Validates the entered passcode and handles success/failure.
- `handle_lockout()`: Manages lockout behavior after too many incorrect attempts.
- `main()`: The primary loop.

---

### **Usage**

#### Run the System
```python
main()
```

---

### **Complete Code**
```python
import board
import digitalio
import neopixel
from adafruit_debouncer import Debouncer
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

PASSCODE = [0, 1, 2]
BUTTON_PINS = [board.D0, board.D1, board.D2]
TIMEOUT = 5
MAX_ATTEMPTS = 3
LOCKOUT_TIME = 10
NEOPIXEL_COLOR_GREEN = (0, 255, 0)
NEOPIXEL_COLOR_RED = (255, 0, 0)
NEOPIXEL_COLOR_YELLOW = (255, 255, 0)
CHARACTER_SEQUENCE = "Hello123!@#"

data = []
last_press_time = time.monotonic()
attempts = 0

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
keyboard = Keyboard(usb_hid.devices)

def init_buttons(pins):
    buttons = []
    for pin in pins:
        pin_input = digitalio.DigitalInOut(pin)
        pin_input.direction = digitalio.Direction.INPUT
        pin_input.pull = digitalio.Pull.UP
        buttons.append(Debouncer(pin_input))
    return buttons

buttons = init_buttons(BUTTON_PINS)

def show_feedback(color, duration=1):
    pixel.fill(color)
    time.sleep(duration)
    pixel.fill((0, 0, 0))

def send_character_sequence(sequence):
    special_char_map = {"!": (Keycode.SHIFT, Keycode.ONE)}
    digit_map = {"0": Keycode.ZERO}
    for char in sequence:
        if char.isupper():
            keyboard.press(Keycode.SHIFT, getattr(Keycode, char.upper()))
        elif char.islower():
            keyboard.press(getattr(Keycode, char.upper()))
        elif char in digit_map:
            keyboard.press(digit_map[char])
        elif char in special_char_map:
            keyboard.press(*special_char_map[char])
        keyboard.release_all()
        time.sleep(0.1)

def check_passcode():
    global data, attempts
    if data == PASSCODE:
        print("Passcode correct.")
        show_feedback(NEOPIXEL_COLOR_GREEN)
        send_character_sequence(CHARACTER_SEQUENCE)
        attempts = 0
    else:
        print("Incorrect passcode!")
        show_feedback(NEOPIXEL_COLOR_RED)
        attempts += 1
    data.clear()

def handle_lockout():
    global attempts
    if attempts >= MAX_ATTEMPTS:
        print("System locked.")
        show_feedback(NEOPIXEL_COLOR_YELLOW, LOCKOUT_TIME)
        attempts = 0

def main():
    global data, last_press_time
    while True:
        handle_lockout()
        for index, button in enumerate(buttons):
            button.update()
            if button.fell:
                data.append(index)
                last_press_time = time.monotonic()
                print(f"Button {index} pressed.")
                if len(data) == len(PASSCODE):
                    check_passcode()
        if data and (time.monotonic() - last_press_time > TIMEOUT):
            print("Timeout!")
            data.clear()

main()
```

---
