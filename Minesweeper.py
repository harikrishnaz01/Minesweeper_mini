import tkinter as tk
from tkinter import messagebox
import random as rn

# ---------------- game logic (your code) ----------------
directions = ["left", "right", "upwards", "downwards"]
downvalues = []
upvalues = []
rightvalues = []
leftvalues = []
done_values = []          # every cell that has been selected so far


def bomb_value():
    bomb_value_i = rn.randint(0, 3)
    bomb_value_j = rn.randint(0, 3)
    return [bomb_value_i, bomb_value_j]


# i = row, j = column
def down_of_selected_position(i, j):
    for row in range(i + 1, 4):
        downvalues.append([row, j])


def up_of_selected_position(i, j):
    for row in range(i - 1, -1, -1):
        upvalues.append([row, j])


def right_of_selected_position(i, j):
    for col in range(j + 1, 4):
        rightvalues.append([i, col])


def left_of_selected_position(i, j):
    for col in range(j - 1, -1, -1):
        leftvalues.append([i, col])


def cardinal_values(i, j):
    # start fresh every round, otherwise old cells pile up
    downvalues.clear()
    upvalues.clear()
    rightvalues.clear()
    leftvalues.clear()

    down_of_selected_position(i, j)
    up_of_selected_position(i, j)
    right_of_selected_position(i, j)
    left_of_selected_position(i, j)

    return {
        "downwards": downvalues,
        "upwards": upvalues,
        "right": rightvalues,
        "left": leftvalues,
    }


bombValue = bomb_value()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("MINESWEEPER")

vars = []        # one IntVar per cell (0 = not selected, 1 = selected)
buttons = []     # the Checkbutton widgets, so we can disable them


def disable_all():
    for b in buttons:
        b.config(state="disabled")


def select_cell(cell):
    """Mark one cell as selected and lock it."""
    index = cell[0] * 4 + cell[1]        # row, col -> 0..15
    done_values.append(cell)
    vars[index].set(1)
    buttons[index].config(state="disabled")


def on_click(index):
    """Runs every time the user clicks a cell (replaces your while loop)."""
    user_input_cell = list(divmod(index, 4))     # [row, col]

    if user_input_cell == bombValue:
        vars[index].set(0)
        buttons[index].config(text="BOMB")
        disable_all()
        messagebox.showinfo("Game over", "BOOM! You picked the bomb.")
        return

    adjacent = cardinal_values(user_input_cell[0], user_input_cell[1])
    valid_directions = [d for d in directions if adjacent[d]]
    chosen_directions = rn.sample(valid_directions, 2)

    new_cells = [user_input_cell]
    for d in chosen_directions:
        new_cells.append(adjacent[d][0])

    # auto-selected cells skip the bomb
    new_cells = [cell for cell in new_cells if cell != bombValue]

    for cell in new_cells:
        if cell not in done_values:
            select_cell(cell)

    if len(done_values) == 15:       # 16 cells - 1 bomb
        disable_all()
        messagebox.showinfo("You win!", "You avoided the bomb everywhere!")


for i in range(16):
    var = tk.IntVar()                # note the () - creates the variable
    vars.append(var)
    row, col = divmod(i, 4)
    b = tk.Checkbutton(root, variable=var, command=lambda i=i: on_click(i))
    b.grid(row=row, column=col, sticky=tk.W)
    buttons.append(b)

root.mainloop()