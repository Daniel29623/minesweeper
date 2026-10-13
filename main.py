import tkinter as tk
from tkinter import messagebox as msgbox
import create
from zlib import decompress as dcomp
from base64 import b85decode as b85

width = 0
height = 0
mines = 0

def small_field() -> None:
    global width, height, mines
    width = 9
    height = 9
    mines = 10
    root.destroy()
def medium_field() -> None:
    global width, height, mines
    width = 16
    height = 16
    mines = 40
    root.destroy()
def large_field() -> None:
    global width, height, mines
    width = 30
    height = 16
    mines = 99
    root.destroy()
def cust() -> None:
    global width, height, mines
    width = int(entries["width"].get())
    height = int(entries["height"].get())
    mines = int(entries["mines"].get())
    if width < height:
        msgbox.showwarning("Rossz mezőméret", "Az aknamező nem lehet magasabb, mint amennyire széles!")
        return
    if mines / (width * height) > .3:
        msgbox.showwarning("Túl sok akna", "Az aknák száma nem haladhatja meg az összes mező 30%-át!")
        return
    if width > 40 or height > 20:
        msgbox.showwarning("Túl nagy mező", "Az aknamező nem lehet 40 x 20-nál nagyobb!")
    root.destroy()
def custom_size() -> None:
    def validate_size(value: str) -> bool:
        if not value:
            return True
        if value.isdigit() and len(value) <= 2:
            return True
        return False
    def validate_mines(value: str) -> bool:
        if not value:
            return True
        if value.isdigit() and len(value) <= 3:
            return True
        return False

    global root, entries
    root.destroy()
    root = tk.Tk()
    root.title("Aknakereső")
    root.resizable(False, False)

    root.protocol("WM_DELETE_WINDOW", on_close)
    valid_size = (root.register(validate_size), "%P")
    valid_mines = (root.register(validate_mines), "%P")

    root.rowconfigure([0, 1], weight=1)
    root.columnconfigure([0, 1, 2, 3], weight=1)
    
    tk.Label(root, text="Szélesség: ", font=("Times New Roman", 12)).grid(row=0, column=0)
    tk.Label(root, text="Magasság: ", font=("Times New Roman", 12)).grid(row=0, column=2)
    tk.Label(root, text="Aknák: ", font=("Times New Roman", 12)).grid(row=1, column=0)

    entries = {
        "width": tk.Entry(root, width=8, validate="key", validatecommand=valid_size),
        "height": tk.Entry(root, width=8, validate="key", validatecommand=valid_size),
        "mines": tk.Entry(root, width=8, validate="key", validatecommand=valid_mines)
    }
    c = 0
    for ent in entries.values():
        ent.grid(row=c if c == 0 else c - 1, column=1 if c % 2 == 0 else 3)
        c += 1

    tk.Button(root, text="OK", font=("Times New Roman", 12), command=cust).grid(row=1, column=2, columnspan=2)

    root.mainloop()


def on_close() -> None:
    exit()

root = tk.Tk()
root.title("Aknakereső")
root.resizable(False, False)

root.protocol("WM_DELETE_WINDOW", on_close)

root.rowconfigure([0, 1], weight=1)
root.columnconfigure([0, 1, 2, 3], weight=1)

tk.Label(root, text="Válaszd ki a nehézségi szintet:", font=("Times New Roman", 48)).grid(row=0, columnspan=4, padx=20, pady=20)
tk.Button(root, text="Könnyű", font=("Times New Roman", 20), command=small_field).grid(row=1, column=0, padx=20, pady=20)
tk.Button(root, text="Közepes", font=("Times New Roman", 20), command=medium_field).grid(row=1, column=1, padx=20, pady=20)
tk.Button(root, text="Nehéz", font=("Times New Roman", 20), command=large_field).grid(row=1, column=2, padx=20, pady=20)
tk.Button(root, text="Saját nehézség", font=("Times New Roman", 20), command=custom_size).grid(row=1, column=3, padx=20, pady=20)

root.mainloop()

create.main(width, height, mines)
with open("game.mines", "rb") as file:
    field = dcomp(b85(file.read())).decode().strip("\n").split("\n")
for i in range(len(field)):
    field[i] = list(field[i])


visited: set[str] = set()
nVisit = 0

def change(ix: int, iy: int) -> None:
    global nVisit
    if f"{ix}x{iy}" in visited:
        return
    if f"{ix}x{iy}" in mined:
        return

    visited.add(f"{ix}x{iy}")
    nVisit += 1
    if nVisit == width * height - mines:
        msgbox.showinfo("Nyertes", "Kinyitottad az összes nem aknát tartalmazó mezőt.\nNyertél! Ügyes vagy!")
        root.quit()
        return

    if field[iy][ix] == "X":
        msgbox.showinfo("Vesztes", "Rákattintottál egy aknára.\nSajnos vesztettél!")
        root.quit()
        return

    fields[f"{ix}x{iy}"].config(text=field[iy][ix])

    if field[iy][ix] == "0":
        for jx in range(ix - 1, ix + 2):
            for jy in range(iy - 1, iy + 2):
                if ix == jx and iy == jy:
                    continue
                if f"{jx}x{jy}" in fields:
                    change(jx, jy)

mined = set()

def mine(event: tk.Event) -> None:
    btn = event.widget

    if fieldsR[btn] in mined:
        btn.config(bg="SystemButtonFace")
        mined.remove(fieldsR[btn])
        return
    if fieldsR[btn] in visited:
        return

    btn.config(bg="red")
    mined.add(fieldsR[btn])

root = tk.Tk()
root.resizable(width=False, height=False)
root.title("Aknakereső")

root.rowconfigure(list(range(width)), weight=1)
root.columnconfigure(list(range(height)), weight=1)

fields: dict[str, tk.Button] = {}

for y in range(height):
    for x in range(width):
        fields[f"{x}x{y}"] = tk.Button(root, width=2)
for key, value in fields.items():
    x = int(key.split("x")[0])
    y = int(key.split("x")[1])
    value.grid(row=y, column=x)
    value.config(command=lambda x=x, y=y: change(x, y))
    value.bind("<Button-3>", mine)

fieldsR = {v: k for k, v in fields.items()}

root.mainloop()