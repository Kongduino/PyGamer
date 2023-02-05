import time, board, sys, keypad
from adafruit_button import Button
from adafruit_bitmap_font import bitmap_font
import displayio
import neopixel
from adafruit_cursorcontrol.cursorcontrol import Cursor
from adafruit_cursorcontrol.cursorcontrol_cursormanager import DebouncedCursorManager
from adafruit_display_text import label

Label = label.Label

# Create the display
display = board.DISPLAY
splashes = [None, None]
buttons = []
menus = []
mouse_cursor = None
cursor = None

def createMenu0():
    global splashes, display, buttons, menus, mouse_cursor, cursor
    # Create the display context
    splash = displayio.Group()
    color_bitmap = displayio.Bitmap(160, 128, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
    feed1_label = Label(GoMonoBold18, text="Menu 0", color=0xE39300)
    feed1_label.x = 5
    feed1_label.y = 20
    splash.append(feed1_label)
    feed2_label = Label(GoMonoBold18, text="First item", color=0x000000)
    feed2_label.x = 5
    feed2_label.y = 50
    splash.append(feed2_label)
    splashes[1] = splash


def createMainMenu():
    global splashes, display, buttons, menus, mouse_cursor, cursor
    # Create the display context
    splash = displayio.Group()
    color_bitmap = displayio.Bitmap(160, 128, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
    numMenuItems = len(menus)
    print(f"numMenuItems: {numMenuItems}")
    px = 2
    py = 0
    fc = PEARL
    oc = DARKGREY
    lc = GREY
    startIndex = 0
    selectedIndex = 0
    menuHeight = 20
    for i in range(0, numMenuItems):
        b = menus[i]
        nm = b["label"]
        #print(f"fc = {fc}")
        #print(f"oc = {oc}")
        #print(f"lc = {lc}")
        button = Button(
            x=px, y=py, width=76, height=menuHeight, style=Button.SHADOWRECT,
            fill_color=fc, outline_color=oc, name=nm, label_font=GoMonoBold12,
            label_color=lc, label=nm)
        py += menuHeight + 1
        if (py+menuHeight) > display.height:
            py = 0
            px = 82
        if selectedIndex == i:
            button.selected = True
        splash.append(button)
        buttons.append(button)
    splashes[0] = splash

def mainMenu():
    global splashes, display, buttons, menus, mouse_cursor, cursor
    if splashes[0] == None:
        createMainMenu()
    if splashes[1] == None:
        createMenu0()
    # Show splash group
    splash = splashes[0]
    splashes[0].hidden = False
    splashes[1].hidden = True
    display.show(splash)
    # initialize the mouse cursor object
    if mouse_cursor == None:
        mouse_cursor = Cursor(display, display_group=splash)
    # initialize the cursormanager
    if cursor == None:
        cursor = DebouncedCursorManager(mouse_cursor)
    cursor.update()

def testNewScreen():
    splashes[1].hidden = False
    splashes[0].hidden = True
    display.show(splashes[1])
    cursor.update()
    while cursor.is_clicked == False:
        time.sleep(0.1)
        cursor.update()
    mainMenu()

def makecolor(r, g, b):
    clr = r*65536 + g*256 +b
    return clr

ff = "fonts/GoMono-Bold-12.bdf"
GoMonoBold12 = bitmap_font.load_font(ff)
ff = "fonts/GoMono-Bold-18.bdf"
GoMonoBold18 = bitmap_font.load_font(ff)
# colors
RED = makecolor(255, 0, 0)
ORANGE = makecolor(255, 34, 0)
YELLOW = makecolor(255, 170, 0)
GREEN = makecolor(0, 255, 0)
CYAN = makecolor(0, 255, 255)
BLUE = makecolor(0, 0, 255)
VIOLET = makecolor(153, 0, 255)
MAGENTA = makecolor(255, 0, 51)
PINK = makecolor(255, 51, 119)
AQUA = makecolor(85, 125, 255)
LIME = makecolor(102, 255, 0)
GREY = 0x666666
PEARL = 0xEAE0C8
WHITE = 0xFFFFFF
DARKGREY = 0x444444
BLACK = 0x000000

def cback(i):
    print(f"You clicked on button {i}")
    if i == 8:
        sys.exit()
    if i == 0:
        testNewScreen()

for i in range(0,9):
    s = f"menu {i}"
    m = {"label" : s, "num" : i, "fun":cback}
    menus.append(m)

mainMenu()

prev_btn = buttons[0]
while True:
    cursor.update()
    if cursor.is_clicked is True:
        numMenuItems = len(buttons)
        for i in range(0, numMenuItems):
            b = buttons[i]
            if b.contains((mouse_cursor.x, mouse_cursor.y)):
                b.selected = True
                x = menus[i]
                if prev_btn is not None:
                    if prev_btn != b:
                        prev_btn.selected = False
                prev_btn = b
                x["fun"](i)
                i = numMenuItems
    time.sleep(0.1)
