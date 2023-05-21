from tkinter import *
import random
import time
import sqlite3
from PIL import ImageTk, Image
from question_button import questions as question_button_questions
from game import start_game
import settings
from tkinter import messagebox

# Εδώ αρχίζει το παιχνίδι!!


def millioner():
    settings.counter_game += 1
    # Θα βρούμε μια λίστα με όλες τις ερωτήσεις και απαντήσεις όπου θα μπορούμε να την επεξεργαστούμε
    if settings.counter_game > 1:
        messagebox.showinfo("Προσοχή!!", "Είναι ήδη ανοιχτό!!! millioner")
    else:
        start_game(root)
        # test.start_game()
        # millioner_button()


def rank():
    # Δημιουργεί ένα Toplevel που εμφανίζει από τον πίνακα rank_table το όνομα και τουσ βαθμούς όπως έχουν καταγραφεί
    # έως τώρα.
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
root.resizable(False, False)
settings.counter_question = 0
settings.counter_game = 0

# Κουμπί για νέο παιχνίδι
btn_new_game = Button(root, text="New Game", command=millioner)
# Κουμπί για εμφάνιση του πίνακα κατάταξης
btn_rank = Button(root, text="Rank", command=rank)
# Κουμπί για επεξεργασία ερωτήσεων
btn_questions = Button(root, text="Game questions", command=questions)

btn_new_game.grid(row=0, column=0)
btn_rank.grid(row=1, column=0)
btn_questions.grid(row=2, column=0)

mainloop()
