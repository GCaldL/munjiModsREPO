from pynput import keyboard


class BarcodeListener:
    def __init__(self):
        self.capture = False
        self.barcode = ''

    def on_press(self, key):
        try:
            if key.char == "\\":
                self.capture = True
                self.barcode = ''
            elif key.char == "/":
                self.capture = False
                # Here you can handle the captured barcode
                print(f'Barcode: {self.barcode}')
            elif self.capture:
                self.barcode += key.char
        except AttributeError:
            pass  # Non-character key pressed, we can ignore it

    def listen(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()


barcode_listener = BarcodeListener()
barcode_listener.listen()
