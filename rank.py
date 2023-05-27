from tkinter import *
import random
import time
import sqlite3
from tkinter import messagebox
from PIL import ImageTk, Image
import settings
global my_selection_question

def new_rank(counter):
    toplevel_rank = Toplevel()
    toplevel_rank.geometry("400x400")
    toplevel_rank.title("My rank")

    my_canvas = Canvas(toplevel_rank, width=400, height=400)

    img = Image.open('assets\millioner_logo.jpg').resize((400, 400))

    transparency=60
    img_transparent = img.copy()
    img_transparent.putalpha(int(255*(transparency/100)))


    img = ImageTk.PhotoImage(img_transparent)

    toplevel_rank.resizable(False, False)
    my_canvas.pack(fill="both", expand=True)
    my_canvas.create_image(0, 0, image=img, anchor="nw")

    def close():
        settings.open_window = 0
        toplevel_rank.destroy()
    toplevel_rank.protocol("WM_DELETE_WINDOW", close)

    def submit(name,counter):
        conn = sqlite3.connect('millionerdb.db')
        c = conn.cursor()
        c.execute(f"INSERT INTO rank_table (name,score) VALUES ('{name}','{counter}')")
        conn.commit()
        conn.close()
        close()


    # lbl_main = Label(toplevel_rank,text=f"Congratulation!! \nYour score is {counter}")
    # lbl_name = Label(toplevel_rank,text="Name: ")
    # e = Entry(toplevel_rank)
    # e.insert(0, "")
    # btn_submit = Button(toplevel_rank, text="Submit", command=lambda:submit(e.get(), counter), width =50, font=("Arial",12))

    # lbl_main.grid(row=0, column=0, columnspan=2)
    # lbl_name.grid(row=1,column=0)
    # e.grid(row=1,column=1)
    # btn_submit.grid(row=2,column=0,columnspan=2)

    canvas_main = my_canvas.create_text(85, 20, text=f"Game over!!!", anchor='nw', fill='black',font=("Arial",30,'bold'))
    canvas_main = my_canvas.create_text(85, 70, text=f"Your score is {counter}", anchor='nw', fill='black', font=("Arial", 20, 'bold'))
    canvas_name = my_canvas.create_text(85, 155, text=f"Name:  ", anchor='nw', fill='black',font=("Arial",20,'bold'))

    e = Entry(my_canvas)
    e.insert(0, "")
    btn_submit = Button(my_canvas, text="Submit", command=lambda:submit(e.get(), counter), width =25, font=("Arial",12))
    my_canvas.create_window(195, 160, anchor="nw", window=e)
    my_canvas.create_window(85, 195, anchor="nw", window=btn_submit)



    toplevel_rank.mainloop()
