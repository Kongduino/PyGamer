import board
from i2cperipheral import I2CPeripheral
from termio import cls as cls
from termio import printat as printat
from termio import rect as rect
from termio import fillrect as fillrect
import time
strLen = 0

cls()
# set cursor at x=5 and y=4 (from top left of screen) and write TEST
printat(5, 2, "BastaGamah!")

with I2CPeripheral(board.SCL, board.SDA, (8, 9)) as device:
    while True:
        r = device.request()
        if not r:
            # Maybe do some housekeeping
            continue
        with r:  # Closes the transfer if necessary by sending a NACK or feeding dummy bytes
            if r.address == 8:
                if not r.is_read:  # Main write which is Selected read
                    n = r.read(1)
                    strLen = int(n[0])
                    #print(f"Incoming on port 8: {strLen}")
                    cls()
                    printat(1, 3, f"Incoming: {strLen} b")
            elif r.address == 9:
                if not r.is_read:
                    b = r.read(strLen).decode()
                    #print(b)
                    printat(1, 4, "Message:")
                    printat(1, 5, b)
