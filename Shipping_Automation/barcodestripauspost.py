from ahk import AHK

# 019931265099999891
# 33W4P345499501000965104
# 42030828008230524015439


def stripCode():
    start = "019931265099999891"
    end = "42030828008230524015439"
    for char in end:
        ahk.key_press('BS')
    ahk.key_press('Home')
    for char in start:
        ahk.key_press('Del')


ahk = AHK()
ahk.add_hotkey('/', callback=stripCode)
ahk.start_hotkeys()
ahk.block_forever()
