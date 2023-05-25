from tkinter import *

import random
import time
import sqlite3
from PIL import ImageTk, Image
from question_button import questions as question_button_questions
import rank_button
from game import start_game
import settings
from tkinter import messagebox

# Εδώ αρχίζει το παιχνίδι!!
def millioner():
    settings.counter_game += 1
    # Θα βρούμε μια λίστα με όλες τις ερωτήσεις και απαντήσεις όπου θα μπορούμε να την επεξεργαστούμε
    if settings.counter_game > 1:
        messagebox.showinfo("Προσοχή!!", "Το παιχνίδι είναι ήδη ανοιχτό!!!")
    else:
        start_game(root)

def rank():
    settings.counter_rank += 1
    if settings.counter_rank > 1:
        messagebox.showinfo("Προσοχή!!", "Η βαθμολογία είναι ήδη ανοιχτό!!!")
    else:
        rank_button.rank()
    pass


def questions():
    settings.counter_question += 1
    # Θα βρούμε μια λίστα με όλες τις ερωτήσεις και απαντήσεις όπου θα μπορούμε να την επεξεργαστούμε
    if settings.counter_question > 1:
        messagebox.showinfo("Προσοχή!!", "Είναι ήδη ανοιχτό!!!")
    else:
        question_button_questions()


# αρχική κεντρική οθόνη
root = Tk()
root.geometry("400x400")
root.title("Main")
my_canvas = Canvas(root, width = 400, height = 400)

img = Image.open('assets\millioner_logo.jpg').resize((400, 400))
img = ImageTk.PhotoImage(img)

root.resizable(False, False)
my_canvas.pack(fill = "both",expand = True)
my_canvas.create_image(0,0,image = img, anchor ="nw")

settings.counter_question = 0
settings.counter_game = 0
settings.counter_rank = 0

# Κουμπί για νέο παιχνίδι
btn_new_game = Button(root, text="New Game", command=millioner,height = 2, width = 20)
# Κουμπί για εμφάνιση του πίνακα κατάταξης
btn_rank = Button(root, text="Rank", command=rank, height = 2, width = 20)
# Κουμπί για επεξεργασία ερωτήσεων
btn_questions = Button(root, text="Game questions", command=questions, height = 2, width = 20)

my_canvas.create_window(20,20,anchor="nw",window = btn_new_game)
my_canvas.create_window(20,80,anchor="nw",window = btn_rank)
my_canvas.create_window(20,140,anchor="nw",window = btn_questions)

mainloop()
