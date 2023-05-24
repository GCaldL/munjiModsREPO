from ahk import AHK
import time


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
    else:
        ahk.add_hotkey('.', callback=printLabel)


def printLabel():
    ahk.mouse_position = positions['printbtn']
    ahk.click()
    ahk.mouse_position = positions['searchbar']
    time.sleep(2)
    ahk.click()
    ahk.key_down('Control')
    ahk.key_press('a')
    ahk.key_up('Control')


def getOrder():
    ahk.mouse_position = positions['searchbar']
    ahk.click()
    time.sleep(1)
    ahk.key_press('BS')
    ahk.key_press('Enter')
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
ahk.add_hotkey("\\", callback=getOrder)
ahk.start_hotkeys()
ahk.block_forever()
