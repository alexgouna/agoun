from tkinter import *
import random
import time
import sqlite3
from PIL import ImageTk, Image

def questions():
    # Θα βρούμε μια λίστα με όλες τις ερωτήσεις και απαντήσεις όπου θα μπορούμε να την επεξεργαστούμε
    root = Tk()
    #root.geometry("400x400")
    root.title("Ερωτήσεις παιχνιδιού")
    #root.resizable(False, False)

    # Εμφάνιση λίστας ερωτήσεων
    e_question = Entry(root)
    e_answer_a = Entry(root)
    e_answer_b = Entry(root)
    e_answer_c = Entry(root)
    e_answer_d = Entry(root)
    e_answer_correct = Entry(root)
    e_dificulty = Entry(root)

    e_question.insert(0, "Ερώτηση")
    e_answer_a.insert(0, "Απάντηση Α")
    e_answer_b.insert(0, "Απάντηση Β")
    e_answer_c.insert(0, "Απάντηση Γ")
    e_answer_d.insert(0, "Απάντηση Δ")
    e_answer_correct.insert(0, "Σωστή Απάντηση")
    e_dificulty.insert(0, "Δυσκολία")

    e_question.grid(row=0, column=0)
    e_answer_a.grid(row=0, column=1)
    e_answer_b.grid(row=0, column=2)
    e_answer_c.grid(row=0, column=3)
    e_answer_d.grid(row=0, column=4)
    e_answer_correct.grid(row=0, column=5)
    e_dificulty.grid(row=0, column=6)


    conn = sqlite3.connect('millionerdb.db')
    c = conn.cursor()
    c.execute("SELECT *  FROM questions_table ")
    questions = c.fetchall()
    my_row=1
    for question in questions:
        e_question = Entry(root)
        e_answer_a = Entry(root)
        e_answer_b = Entry(root)
        e_answer_c = Entry(root)
        e_answer_d = Entry(root)
        e_answer_correct = Entry(root)
        e_difficulty = Entry(root)

        e_question.insert(0, question[0])
        e_answer_a.insert(0, question[1])
        e_answer_b.insert(0, question[2])
        e_answer_c.insert(0, question[3])
        e_answer_d.insert(0, question[4])
        e_answer_correct.insert(0, question[5])
        e_difficulty.insert(0, question[6])

        e_question.grid(row=my_row, column=0)
        e_answer_a.grid(row=my_row, column=1)
        e_answer_b.grid(row=my_row, column=2)
        e_answer_c.grid(row=my_row, column=3)
        e_answer_d.grid(row=my_row, column=4)
        e_answer_correct.grid(row=my_row, column=5)
        e_difficulty.grid(row=my_row, column=6)

        my_row = my_row + 1

    conn.commit()
    conn.close()

    def save():
        # Αποθήκευση αλλαγών της λίστας ερωτήσεων
        conn = sqlite3.connect('millionerdb.db')
        c = conn.cursor()
        c.execute("DELETE FROM questions_table ")
        conn.commit()
        conn.close()

    def add_new():
        # Δημιουργία νέας ερώτησης
        pass

    def remove():
        # Διαγραφή μίας ερώτησης
        pass

    def reset():
        # Γεμίζει τη λίστα με προσωρινές ερωτήσεις
        conn = sqlite3.connect('millionerdb.db')
        c = conn.cursor()
        difficulties=["easy","medium","hard"]
        for difficulty in difficulties:
            for j in range(10):
                c.execute("INSERT INTO questions_table VALUES (?,?,?,?,?,?,?)",
                          ("Ερώτηση δυσκολίας: " + str(difficulty) + " σειρά: " + str(j), "Α", "Β", "Γ", "Δ", random.choice(["Α", "Β", "Γ", "Δ"]), difficulty))
        conn.commit()
        conn.close()

    btn_save = Button(root, text="Save", command=save)
    btn_add_new = Button(root, text="Add new", command=add_new)
    btn_remove = Button(root, text="Remove", command=remove)
    btn_reset_temp = Button(root, text="Reset temp", command=reset)

    btn_save.grid(row=my_row,column=0,columnspan=2)
    btn_add_new.grid(row=my_row, column=2, columnspan=2)
    btn_remove.grid(row=my_row, column=4, columnspan=2)
    btn_reset_temp.grid(row=my_row, column=6, columnspan=2)

    mainloop()