from ahk import AHK
import pyautogui as autogui
import time


def findHighlighted(color):
    s = autogui.screenshot(region=(labelpos[0], 0, 1, 1080))
    for x in range(s.width):
        for y in range(s.height):
            if s.getpixel((x, y)) == color:
                return (checkpos[0], y+10)


def select_order_no(order):
    print("huh?")
    autogui.keyDown('ctrlleft')
    autogui.press('f')
    autogui.keyUp('ctrlleft')

    autogui.press('enter')

    try:
        # pos = autogui.locateOnScreen('find.png')
        # pos = autogui.locateOnScreen(
        #    'find.png2', region=(200, 0, 300, 1080), confidence=0.9)
        color = (255, 150, 50)
        pos = findHighlighted(color)
        autogui.moveTo(pos)
        autogui.click(pos)
        print(pos)
    except Exception as e:
        print(e)
        print('Order: ' + order + " not found :")


def select_order():
    autogui.press('enter')
    time.sleep(0.5)

    try:
        color = (255, 150, 50)
        pos = findHighlighted(color)
        autogui.moveTo(pos)
        autogui.click(pos)
        print(pos)
    except Exception as e:
        print(e)
        print('Order not found :')
    autogui.keyDown('ctrlleft')
    autogui.press('f')
    autogui.keyUp('ctrlleft')


def setLocations():
    global labelpos
    global checkpos
    if labelpos == 0:
        labelpos = autogui.position()
        ahk.show_tooltip(
            "label position set", x=ahk.mouse_position[0], y=ahk.mouse_position[1])
    elif checkpos == 0:
        checkpos = autogui.position()
        ahk.show_tooltip(
            "checkbox position set", x=ahk.mouse_position[0], y=ahk.mouse_position[1])
        time.sleep(2)
        ahk.hide_tooltip()
    else:
        labelpos = 0
        checkpos = 0


labelpos = 0
checkpos = 0
ahk = AHK()

ahk.add_hotkey('.', callback=setLocations)
ahk.add_hotkey('/', callback=select_order)
ahk.start_hotkeys()
ahk.block_forever()
