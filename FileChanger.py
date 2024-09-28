# rename(), move()
import os
import math

def moveFile(src, dst):
    for i in range (math.inf):
        try:
            os.rename(src, dst)
            break
        except OSError as e:
            text = os.path.splitext(".")
            dst = text[0] + '(' + i + ')' + text[1]
            