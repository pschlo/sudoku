from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from .solver import SudokuError, solve_sudoku

root = Tk()  # create tkinter window
root.title("Sudoku Solver")
bg = root["bg"]  # get background of window (=default background color)
font = ("Verdana", 20)


def error(msg):
    messagebox.showerror("Error", msg)
    print("ERROR:", msg)


def solve():  # called when button "solve" is clicked
    sudoku = read_sudoku()  # read current GUI grid and put into 2d sudoku array
    try:
        solved = solve_sudoku(sudoku)
    except SudokuError as exception:
        error(str(exception))
        return
    insert_sudoku(solved)  # insert the solved sudoku into the GUI grid


def reset():  # called when button "reset" is clicked
    global sel
    for i in list_input:  # list_input is a 2d array containing all the text fields
        for j in i:
            j.config(text="")  # set every text field to empty string
    sel = None
    update_sel()


def insert_sudoku(sudoku):  # inserts a 2d sudoku array into the GUI grid
    for i in range(9):
        for j in range(9):
            value = sudoku[i][j]  # current value in die 2d sudoku array
            if value == 0:
                value = ""  # replace all "0" with empty string
            list_input[i][j].config(text=str(value))  # set text for every text field


def import_sudoku():  # called when button "open" is clicked
    files = (("sudoku-files", "*.sd"), ("all files", "*.*"))
    file = filedialog.askopenfile(
        mode="r", initialdir="/", title="Sudoku auswählen", filetypes=files
    )
    if file is None:  # if user did not select any file
        return
    sudoku = []
    for line in file.readlines():  # read file and put into 2d sudoku array
        if "\n" in line:
            sudoku.append(list(map(int, line[:-1].replace(" ", ""))))
        else:
            sudoku.append(list(map(int, line.replace(" ", ""))))
    file.close()
    insert_sudoku(sudoku)  # insert sudoku into GUI grid


def export_sudoku():  # called when button "export" is clicked
    files = (("sudoku-files", "*.sd"), ("all files", "*.*"))
    file = filedialog.asksaveasfile(
        mode="w+", initialdir="/", title="Sudoku speichern", filetypes=files, defaultextension=".sd"
    )  # opens selected file in write mode
    if file is None:  # if user did not select any file
        return
    sudoku = read_sudoku()  # read current GUI grid and put into 2d sudoku array
    for line in sudoku:
        file.write(
            " ".join(map(str, line))
        )  # convert every line in sudoku to string with spaces between every field
        file.write("\n")
    file.close()


def read_sudoku():  # read current GUI grid and put into 2d sudoku array
    sudoku = []
    for i in range(9):
        sudoku.append([])
        for j in range(9):
            value = list_input[i][j]["text"]  # read value of each text field
            if value == "":
                value = 0  # replace all emtpy strings with 0
            sudoku[i].append(int(value))
    return sudoku


def move_left():
    global sel  # needs to be global because value of sel is changed
    if sel is None:  # if cursor is not set
        return
    if sel[0] == 0 and sel[1] == 0:  # top left field
        return
    elif sel[1] > 0:
        sel = (sel[0], sel[1] - 1)
    else:
        sel = (sel[0] - 1, 8)
    update_sel()  # update GUI so that the new selection is shown


def move_right():
    global sel
    if sel is None:
        return
    if sel[0] == 8 and sel[1] == 8:  # bottom right field
        return
    elif sel[1] < 8:
        sel = (sel[0], sel[1] + 1)
    else:
        sel = (sel[0] + 1, 0)
    update_sel()


def move_up():
    global sel
    if sel is None:
        return
    if sel[0] == 0:
        pass
    else:
        sel = (sel[0] - 1, sel[1])
    update_sel()


def move_down():
    global sel
    if sel is None:
        return
    if sel[0] == 8:
        pass
    else:
        sel = (sel[0] + 1, sel[1])
    update_sel()


def update_sel():
    for i in list_frame_input:  # reset all selections
        for j in i:
            j.config(
                highlightcolor="grey", highlightbackground="grey"
            )  # change border back to grey
    if sel is not None:
        list_frame_input[sel[0]][sel[1]].config(
            highlightcolor="red", highlightbackground="red"
        )  # change border to red


def click(event):  # called upon every mouse click
    global sel
    for i in range(9):  # get selection coordinates
        for j in range(9):
            if list_input[i][j] == event.widget:
                sel = (i, j)
    print("clicked at", sel)  # debug
    update_sel()


def key_press(event):  # called upon every key press except for the keys on the bottom of this code
    if sel is not None and event.char in map(
        str, list(range(1, 10))
    ):  # if pressed key is number 1 to 9
        list_input[sel[0]][sel[1]].config(
            text=event.char
        )  # insert number into the selected text field


def clear_selected():
    if sel is not None:
        list_input[sel[0]][sel[1]].config(text="")


sel = None
frame_sudoku = Frame(
    root, highlightcolor="black", highlightbackground="black", highlightthickness=1
)
# main frame that will contain the sudoku
frame_sudoku.pack(padx=20, pady=20)

list_input = []  # 2d array containing all the text fields
list_frame_input = []  # 2d array containing all the frames that surround the text fields (1 frame per text field)
# every text field is wrapped in a frame because the frame border can easily be adjusted when selected
list_frame_block = []  # 2d array containing all of the frames that represent the 9 big blocks

for i in range(3):  # create list_frame_block (3x3 array)
    list_frame_block.append([])
    for j in range(3):
        frame = Frame(
            frame_sudoku, highlightcolor="black", highlightbackground="black", highlightthickness=1
        )
        list_frame_block[i].append(frame)
        frame.grid(row=i, column=j)

for i in range(9):  # create list_input and list_frame_input (both 9x9 arrays)
    list_input.append([])
    list_frame_input.append([])
    for j in range(9):
        # put text field frame into one of the big 9 frames
        frame = Frame(list_frame_block[i // 3][j // 3], highlightthickness=2)
        list_frame_input[i].append(frame)
        # place text field frame inside of it's bigger frame
        frame.grid(row=i % 3, column=j % 3)
        # put text field inside of the smaller text field frame that was just created
        entry = Label(frame, width=2, font=font, justify=CENTER, text="")
        list_input[i].append(entry)
        entry.pack()

update_sel()  # call update_sel so that there is grey grid at the beginning

frame_btn = Frame(root, pady=15)  # frame containing all buttons
frame_btn.pack()
btn_solve = Button(frame_btn, padx=15, pady=5, text="Solve", command=solve)
btn_solve.pack(side=LEFT, padx=10)
btn_reset = Button(frame_btn, padx=15, pady=5, text="Reset", command=reset)
btn_reset.pack(side=LEFT, padx=10)
btn_import = Button(frame_btn, padx=15, pady=5, text="Open", command=import_sudoku)
btn_import.pack(side=LEFT, padx=10)
btn_export = Button(frame_btn, padx=15, pady=5, text="Export", command=export_sudoku)
btn_export.pack(side=LEFT, padx=10)

# bind functions to key press
root.bind("<Up>", lambda x: move_up())
root.bind("<Down>", lambda x: move_down())
root.bind("<Left>", lambda x: move_left())
root.bind("<Right>", lambda x: move_right())
root.bind("<Button-1>", click)
root.bind("<Return>", lambda x: solve())
root.bind("<BackSpace>", lambda x: clear_selected())
root.bind("<Delete>", lambda x: clear_selected())
root.bind("<Escape>", lambda x: clear_selected())
root.bind("r", lambda x: reset())
root.bind("<KeyPress>", key_press)


def main():
    root.mainloop()
