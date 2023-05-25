from tkinter import *
import random
import time
import sqlite3
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import settings
global my_selection_question

def new_rank(counter):
    toplevel_rank = Toplevel()
    toplevel_rank.geometry("400x400")
    toplevel_rank.title("Main")

    settings.counter_toplevel_rank = 1
    settings.counter_game = 0

    def close():
        settings.counter_toplevel_rank = 0
        toplevel_rank.destroy()
    toplevel_rank.protocol("WM_DELETE_WINDOW", close)

    def submit(name,counter):
        conn = sqlite3.connect('millionerdb.db')
        c = conn.cursor()
        c.execute(f"INSERT INTO rank_table (name,score) VALUES ('{name}','{counter}')")
        conn.commit()
        conn.close()
        close()


    lbl_main = Label(toplevel_rank,text=f"Congratulation!! \nYour score is {counter}")
    lbl_name = Label(toplevel_rank,text="Name")
    e = Entry(toplevel_rank)
    e.insert(0, "")
    btn_submit = Button(toplevel_rank, text="Submit", command=lambda:submit(e.get(), counter))

    lbl_main.grid(row=0, column=0, columnspan=2)
    lbl_name.grid(row=1,column=0)
    e.grid(row=1,column=1)
    btn_submit.grid(row=2,column=0,columnspan=2)

    toplevel_rank.mainloop()

    print("my rank is,,, ")

