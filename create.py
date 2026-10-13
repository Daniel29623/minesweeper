from random import randint
from base64 import b85encode as b85
from zlib import compress as comp

def main(width: int, height: int, mines: int) -> None:
    mineList: list[tuple[int]] = list()
    mine: tuple[int] = tuple()
    for m in range(mines):
        mine = (randint(0, width - 1), randint(0, height - 1))
        while mine in mineList:
            mine = (randint(0, width - 1), randint(0, height - 1))
        mineList.append(mine)
    with open("game.mines", "wb") as file:
        data: str = str()
        for y in range(height):
            for x in range(width):
                if (x, y) in mineList:
                    data += "X"
                else:
                    c = 0
                    if x == 0:
                        if y == 0:
                            for ix in range(x, x + 2):
                                for iy in range(y, y + 2):
                                    if (ix, iy) in mineList:
                                        c += 1
                        elif y == height - 1:
                            for ix in range(x, x + 2):
                                for iy in range(y - 1, y + 1):
                                    if (ix, iy) in mineList:
                                        c += 1
                        else:
                            for ix in range(x, x + 2):
                                for iy in range(y - 1, y + 2):
                                    if (ix, iy) in mineList:
                                        c += 1
                    elif x == width - 1:
                        if y == 0:
                            for ix in range(x - 1, x + 1):
                                for iy in range(y, y + 2):
                                    if (ix, iy) in mineList:
                                        c += 1
                        elif y == height - 1:
                            for ix in range(x - 1, x + 1):
                                for iy in range(y - 1, y + 1):
                                    if (ix, iy) in mineList:
                                        c += 1
                        else:
                            for ix in range(x - 1, x + 1):
                                for iy in range(y - 1, y + 2):
                                    if (ix, iy) in mineList:
                                        c += 1
                    else:
                        if y == 0:
                            for ix in range(x - 1, x + 2):
                                for iy in range(y, y +2):
                                    if (ix, iy) in mineList:
                                        c += 1
                        elif y == height - 1:
                            for ix in range(x - 1, x + 2):
                                for iy in range(y - 1, y + 1):
                                    if (ix, iy) in mineList:
                                        c += 1
                        else:
                            for ix in range(x - 1, x + 2):
                                for iy in range(y - 1, y + 2):
                                    if (ix, iy) in mineList:
                                        c += 1
                    data += str(c)
            data += "\n"
        file.write(b85(comp(data.encode())))

if __name__ == "__main__":
    width = 30
    height = 16
    mines = 99
    main(width, height, mines)
