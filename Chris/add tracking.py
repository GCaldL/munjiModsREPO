from ahk import AHK
import time


def stripCode():
    start = "019931265099999891"
    end = "42030828008230524015439"
    for char in end:
        ahk.key_press('BS')
    ahk.key_press('Home')
    for char in start:
        ahk.key_press('Del')


def getOrder():
    ahk.key_press('Enter')
    time.sleep(1)
    ahk.mouse_position = positions['orderpos']
    ahk.click()


positions = {
    "searchbar": 0,
    "orderpos": 0,
}

ahk = AHK()
ahk.add_hotkey('/', callback=getOrder)
ahk.add_hotkey('.', callback=stripCode)
ahk.start_hotkeys()
ahk.block_forever()
