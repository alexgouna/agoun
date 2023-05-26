from tkinter import *
import random
import time
import sqlite3
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import settings

global my_selection_question


def rank():
    root_rank = Toplevel()
    root_rank.geometry("600x426")
    root_rank.title("Rank")

    def close():
        settings.open_window = 0
        # settings.counter_rank = 0
        root_rank.destroy()

    root_rank.protocol("WM_DELETE_WINDOW", close)

    tree_scrollbar = Scrollbar(root_rank)
    tree_scrollbar.grid(row=0, column=11, sticky=N + S)

    tree_rank = ttk.Treeview(root_rank, yscrollcommand=tree_scrollbar.set, height=20)
    tree_scrollbar.config(command=tree_rank.yview)
    tree_rank['columns'] = ("Rank", "Player", "Points")
    tree_rank.column("#0", width=0, stretch=NO)
    tree_rank.column("Rank", width=50, anchor ='c')
    tree_rank.column("Player", width=450, anchor ='c')
    tree_rank.column("Points", width=80, anchor ='c')

    tree_rank.heading("#0", text="Rank")
    tree_rank.heading("Rank", text="Rank")
    tree_rank.heading("Player", text="Player")
    tree_rank.heading("Points", text="Points")

    tree_rank.tag_configure('white',background="#cb71fb")
    tree_rank.tag_configure('light_blue', background="#836eff")
    i = 0
    conn = sqlite3.connect('millionerdb.db')
    c = conn.cursor()
    c.execute("SELECT *  FROM rank_table ORDER BY score DESC")
    my_rank = c.fetchall()
    for rank in my_rank:
        if i%2 ==1:
            tree_rank.insert(parent='', index='end', iid=str(i), text="234", values=(i + 1, rank[0], rank[1]),tags=("white"))
        else:
            tree_rank.insert(parent='', index='end', iid=str(i), text="234", values=(i + 1, rank[0], rank[1]),tags=("light_blue"))
        i += 1
    tree_rank.grid(row=0, columnspan=10)
    conn.commit()
    conn.close()
