from PyQt5.QtGui import QColor
def coordinate(i, j, size):
    x = i * size + size // 2
    y = j * size + size // 2
    return x, y

def coordinate_t(x, y, size):
    i = x // size
    j = y // size
    return i, j

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_PINK = (255, 182, 193)
STEEL_BLUE = (70, 130, 180)
CRIMSON = (220, 20, 60)
VIOLET = (238, 130, 238)
SLATEBLUE = (106, 90, 205)
CYAN = (0, 255, 255)
AUQAMARIN = (127, 255, 170)
LIME = (0, 255, 0)
YELLOW = (255, 255, 0)
OLIVE = (128, 128, 0)
CORNISLK = (255, 248, 220)
ORANGE = (255, 165, 0)
CORAL = (255, 127, 80)
SKY_BLUE = (135, 206, 235)
GOLD = (255, 215, 0)
MAROON = (128, 0, 0)