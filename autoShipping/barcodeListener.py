from pynput import keyboard
from ahk import AHK
import time
from threading import Thread


def setLocations():
    global positions
    if positions["printbtn"] == 0:
        for position in positions:
            value = positions.get(position)
            if value == 0:
                mousePos = ahk.mouse_position
                positions[position] = mousePos
                tooltip = str(position) + " set:" + \
                    str(mousePos[0]) + " " + str(mousePos[1])
                ahk.show_tooltip(
                    tooltip, x=ahk.mouse_position[0], y=ahk.mouse_position[1])
                time.sleep(2)
                ahk.hide_tooltip()
                break


class BarcodeListener:
    def __init__(self):
        self.capture = False
        self.barcode = ''
        self.busy = False

    def on_press(self, key):
        if not self.busy:
            try:
                if key.char == "\\":
                    self.capture = True
                    self.barcode = ''
                elif key.char == "/":
                    self.capture = False
                    # Here you can handle the captured barcode
                    self.busy = True
                    print(f'Barcode: {self.barcode}')
                    handleCode(self.barcode)
                    self.busy = False
                elif self.capture:
                    self.barcode += key.char
            except AttributeError:
                pass  # Non-character key pressed, we can ignore it

    def listen(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()


def handleCode(code):
    ahk.mouse_position = positions['searchbar']
    ahk.click()
    ahk.key_down('Control')
    ahk.key_press('a')
    ahk.key_up('Control')
    ahk.send_input(code)
    ahk.key_press("Enter")
    time.sleep(1)
    ahk.mouse_position = positions['orderpos']
    ahk.click()


positions = {
    "searchbar": 0,
    "orderpos": 0,
    "printbtn": 0
}
ahk = AHK()
ahk.add_hotkey('.', callback=setLocations)
ahk.start_hotkeys()

barcode_listener = BarcodeListener()
listener = keyboard.Listener(on_press=barcode_listener.on_press)


def run_listener():
    with listener:
        listener.join()


listener_thread = Thread(target=run_listener)
listener_thread.start()

try:
    while True:
        pass  # The rest of your code goes here, make sure the main thread doesn't exit
except KeyboardInterrupt:
    listener.stop()
