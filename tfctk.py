import tkinter as tk
from tkinter import ttk, messagebox, Menu
from PIL import Image, ImageTk

pbl = [0, 0, 0]
pbl2 = []
lstp = [2, 7, 13, 16]
lstn = [-3, -6, -9, -15]
newlst = []
queued_images = []

images = {
    "Light Hit": "assets/light_hit.png",
    "Medium Hit": "assets/medium_hit.png",
    "Heavy Hit": "assets/heavy_hit.png",
    "Draw": "assets/draw.png",
    "Punch": "assets/punch.png",
    "Bend": "assets/bend.png",
    "Upset": "assets/upset.png",
    "Shrink": "assets/shrink.png",
}


def closest(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


def update_pbl(value):
    global pbl
    pbl = [value] + pbl[:2]
    update_label()
    add_image_to_queue(value)


def update_pbl2(value):
    global pbl2
    pbl2.append(value)
    update_label2()
    add_image_to_queue(value)


def update_label():
    global pressedL
    pressedL.config(text=pbl)


def update_label2():
    global pressedL2
    pressedL2.config(text=pbl2)


def add_image_to_queue(value):
    action_name = next(
        (name for name, val in images.items() if val == value), None
    )
    if action_name and action_name in images:
        img = ImageTk.PhotoImage(
            Image.open(images[action_name]).resize((30, 30))
        )
        queued_images.append(img)
        display_queue()


def display_queue():
    for widget in queue_frame.winfo_children():
        widget.destroy()
    for img in queued_images:
        lbl = tk.Label(queue_frame, image=img)
        lbl.image = img
        lbl.pack(side=tk.LEFT, padx=5)


def reset_queue():
    global queued_images
    queued_images = []
    display_queue()
    reset_path()
    clear_result()


def reset_path():
    global pbl, pbl2
    pbl = [0, 0, 0]
    pbl2 = []
    update_label()
    update_label2()


def clear_result():
    for widget in result_frame.winfo_children():
        widget.destroy()


def calce():
    global pbl2
    global pressedL2
    coord = sum(pbl2)
    pressedL2.config(text=f"The end coordinate is {coord}")


def calculatepath():
    global resultP
    global pbl
    global cente
    newlst = []
    a = pbl[2]
    b = pbl[1]
    c = pbl[0]
    cn = cente.get()
    try:
        cn = int(cn)
        bf = ((cn - a) - b) - c
        fs = 0
    except:
        resultP.config(text="Error! Put end coordinate in the entrybox!")
        return

    while fs != bf:
        x = bf - fs
        if x > 0:
            dif = closest(lstp, x)
            fs += dif
            newlst.append(dif)
        if x < 0:
            dif = closest(lstn, x)
            fs += dif
            newlst.append(dif)

    newlst.append(c)
    newlst.append(b)
    newlst.append(a)

    for widget in result_frame.winfo_children():
        widget.destroy()

    result_frame.columnconfigure(0, weight=1)
    result_frame.rowconfigure(0, weight=1)

    container = tk.Frame(result_frame)
    container.grid(row=0, column=0, sticky="nsew")
    container.columnconfigure(0, weight=1)

    for index, action in enumerate(newlst):
        action_name = None
        if action == 2:
            action_name = "Punch"
        elif action == 7:
            action_name = "Bend"
        elif action == 13:
            action_name = "Upset"
        elif action == 16:
            action_name = "Shrink"
        elif action == -3:
            action_name = "Light Hit"
        elif action == -6:
            action_name = "Medium Hit"
        elif action == -9:
            action_name = "Heavy Hit"
        elif action == -15:
            action_name = "Draw"

        if action_name in images:
            img = ImageTk.PhotoImage(
                Image.open(images[action_name]).resize((30, 30))
            )
            lbl = tk.Label(
                container, text=action_name, compound=tk.TOP, image=img
            )
            lbl.image = img
            lbl.grid(row=0, column=index, padx=5, sticky="w")


def about():
    tk.messagebox.showinfo(
        title="About",
        message="""This is a program to help with anvil minigame in TerraFirmaCraft, a Minecraft mod made by Robert "Bioxx" Anthony, Amanda "Kittychanley" Halek, and others.

Program author: dzhemvrot (enhanced by Taeko-ar)
Program version: 2.0
Program restributed using GPL-3.0 license""",
    )


def quitting():
    root.destroy()


root = tk.Tk()
root.title("Tab Widget")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

tabControl = ttk.Notebook(root)
tabControl.grid(row=0, column=0, sticky="nsew")

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text="Path")
tabControl.add(tab2, text="End")

tab1.rowconfigure(0, weight=1)
tab1.columnconfigure(0, weight=1)
tab2.rowconfigure(0, weight=1)
tab2.columnconfigure(0, weight=1)

menubar = Menu(root)
root.config(menu=menubar)

file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Exit", command=quitting)
menubar.add_cascade(label="File", menu=file_menu)
menubar.add_command(label="About", command=about)

ttk.Label(tab1, text="Calculate the path").grid(
    column=2, row=0, padx=30, pady=0
)
pressedL = ttk.Label(tab1, text=pbl)
pressedL.grid(column=2, row=1, padx=0, pady=0)

queue_frame = ttk.Frame(tab1)
queue_frame.grid(column=2, row=6, padx=10, pady=10, sticky="nsew")

result_frame = ttk.Frame(tab1)
result_frame.grid(column=2, row=8, padx=10, pady=10, sticky="nsew")

for i in range(5):
    tab1.columnconfigure(i, weight=1)
    tab1.rowconfigure(i, weight=1)

ttk.Button(tab1, text="Light Hit", command=lambda: update_pbl(-3)).grid(
    column=0, row=2, padx=10, pady=10
)
ttk.Button(tab1, text="Medium Hit", command=lambda: update_pbl(-6)).grid(
    column=1, row=2, padx=10, pady=10
)
ttk.Button(tab1, text="Heavy Hit", command=lambda: update_pbl(-9)).grid(
    column=0, row=3, padx=10, pady=10
)
ttk.Button(tab1, text="Draw", command=lambda: update_pbl(-15)).grid(
    column=1, row=3, padx=10, pady=10
)
ttk.Button(tab1, text="Punch", command=lambda: update_pbl(2)).grid(
    column=3, row=2, padx=10, pady=10
)
ttk.Button(tab1, text="Bend", command=lambda: update_pbl(7)).grid(
    column=4, row=2, padx=10, pady=10
)
ttk.Button(tab1, text="Upset", command=lambda: update_pbl(13)).grid(
    column=3, row=3, padx=10, pady=10
)
ttk.Button(tab1, text="Shrink", command=lambda: update_pbl(16)).grid(
    column=4, row=3, padx=10, pady=10
)

cente = ttk.Entry(tab1)
cente.grid(column=2, row=3)
ttk.Button(tab1, text="Calculate", command=calculatepath).grid(
    column=2, row=4, padx=10, pady=10
)
ttk.Button(tab1, text="Reset Queue", command=reset_queue).grid(
    column=2, row=5, padx=10, pady=10
)

resultP = ttk.Label(tab1, text="")
resultP.grid(column=2, row=7, padx=0, pady=0)

# Tab 2 (End)
ttk.Label(tab2, text="Calculate the end coordinate").grid(
    column=2, row=0, padx=30, pady=0
)
pressedL2 = ttk.Label(tab2, text="")
pressedL2.grid(column=2, row=1, padx=0, pady=0)

tab2.columnconfigure(0, weight=1)
tab2.rowconfigure(0, weight=1)
tab2.columnconfigure(4, weight=1)

ttk.Button(tab2, text="Light Hit", command=lambda: update_pbl2(-3)).grid(
    column=0, row=2, padx=10, pady=10
)
ttk.Button(tab2, text="Medium Hit", command=lambda: update_pbl2(-6)).grid(
    column=1, row=2, padx=10, pady=10
)
ttk.Button(tab2, text="Heavy Hit", command=lambda: update_pbl2(-9)).grid(
    column=0, row=3, padx=10, pady=10
)
ttk.Button(tab2, text="Draw", command=lambda: update_pbl2(-15)).grid(
    column=1, row=3, padx=10, pady=10
)
ttk.Button(tab2, text="Punch", command=lambda: update_pbl2(2)).grid(
    column=3, row=2, padx=10, pady=10
)
ttk.Button(tab2, text="Bend", command=lambda: update_pbl2(7)).grid(
    column=4, row=2, padx=10, pady=10
)
ttk.Button(tab2, text="Upset", command=lambda: update_pbl2(13)).grid(
    column=3, row=3, padx=10, pady=10
)
ttk.Button(tab2, text="Shrink", command=lambda: update_pbl2(16)).grid(
    column=4, row=3, padx=10, pady=10
)

resetB = ttk.Button(tab2, text="Reset", command=lambda: reset_path()).grid(
    column=2, row=5, padx=10, pady=10
)
calceB = ttk.Button(tab2, text="Calculate", command=calce).grid(
    column=2, row=4, padx=10, pady=10
)

root.mainloop()
