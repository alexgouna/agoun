from tkinter import *
import random
import time
import sqlite3
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

global my_selection_question


def questions():
    # Θα βρούμε μια λίστα με όλες τις ερωτήσεις και απαντήσεις όπου θα μπορούμε να την επεξεργαστούμε
    root = Tk()
    root.geometry("1200x800")
    root.title("Ερωτήσεις παιχνιδιού")
    # root.resizable(False, False)

    tree_questions = ttk.Treeview(root)
    tree_questions['columns'] = (
        "question", "ansewera", "answerb", "answerc", "answerd", "correct_answer", "difficulty")
    tree_questions.column("#0", width=0, stretch=NO)
    tree_questions.column("question", width=120, minwidth=25)
    tree_questions.column("ansewera", width=120, minwidth=25)
    tree_questions.column("answerb", width=120, minwidth=25)
    tree_questions.column("answerc", width=120, minwidth=25)
    tree_questions.column("answerd", width=120, minwidth=25)
    tree_questions.column("correct_answer", width=120, minwidth=25)
    tree_questions.column("difficulty", width=120, minwidth=25)

    tree_questions.heading("#0", text="")
    tree_questions.heading("question", text="Ερώτηση")
    tree_questions.heading("ansewera", text="Απάντηση Α")
    tree_questions.heading("answerb", text="Απάντηση Β")
    tree_questions.heading("answerc", text="Απάντηση Γ")
    tree_questions.heading("answerd", text="Απάντηση Δ")
    tree_questions.heading("correct_answer", text="Σωστή απάντηση")
    tree_questions.heading("difficulty", text="Δυσκολία")

    global i
    i = 0

    def question_tree_refresh():
        global i
        conn = sqlite3.connect('millionerdb.db')
        c = conn.cursor()
        c.execute("SELECT *  FROM questions_table ")
        questions = c.fetchall()
        for question in questions:
            tree_questions.insert(parent='', index='end', iid=str(i), text="", values=(question))
            i += 1
        tree_questions.grid(row=0, columnspan=10)
        conn.commit()
        conn.close()

    question_tree_refresh()

    lbl_question = Label(root, text="Ερώτηση:")
    lbl_answer_a = Label(root, text="Απάντηση Α:")
    lbl_answer_b = Label(root, text="Απάντηση Β:")
    lbl_answer_c = Label(root, text="Απάντηση Γ:")
    lbl_answer_d = Label(root, text="Απάντηση Δ:")
    lbl_correct_answer = Label(root, text="Σωστή απάντηση:")
    lbl_difficulty = Label(root, text="Δυσκολία:")

    lbl_question.grid(row=1, column=0, sticky=W)
    lbl_answer_a.grid(row=2, column=0, sticky=W)
    lbl_answer_b.grid(row=3, column=0, sticky=W)
    lbl_answer_c.grid(row=4, column=0, sticky=W)
    lbl_answer_d.grid(row=5, column=0, sticky=W)
    lbl_correct_answer.grid(row=6, column=0, sticky=W)
    lbl_difficulty.grid(row=7, column=0, sticky=W)

    e_question = Entry(root)
    e_answer_a = Entry(root)
    e_answer_b = Entry(root)
    e_answer_c = Entry(root)
    e_answer_d = Entry(root)
    e_correct_answer = Entry(root)
    e_difficulty = Entry(root)

    e_question.grid(row=1, column=1, columnspan=6, pady=4, sticky=W+E)
    e_answer_a.grid(row=2, column=1, columnspan=6, pady=4, sticky=W+E)
    e_answer_b.grid(row=3, column=1, columnspan=6, pady=4, sticky=W+E)
    e_answer_c.grid(row=4, column=1, columnspan=6, pady=4, sticky=W+E)
    e_answer_d.grid(row=5, column=1, columnspan=6, pady=4, sticky=W+E)
    e_correct_answer.grid(row=6, column=1, columnspan=6, pady=4, sticky=W+E)
    e_difficulty.grid(row=7, column=1, columnspan=6, pady=4, sticky=W+E)

    def test_if_question_exist(my_question):
        conn = sqlite3.connect('millionerdb.db')
        c = conn.cursor()
        c.execute("SELECT * FROM questions_table")
        questions = c.fetchall()
        for question in questions:
            if question[0] == my_question:
                conn.commit()
                conn.close()
                return True
        conn.commit()
        conn.close()
        return False

    def clear_entries():
        e_question.delete(0, END)
        e_answer_a.delete(0, END)
        e_answer_b.delete(0, END)
        e_answer_c.delete(0, END)
        e_answer_d.delete(0, END)
        e_correct_answer.delete(0, END)
        e_difficulty.delete(0, END)

    def clear():
        for record in tree_questions.get_children():
            tree_questions.delete(record)
        clear_entries()
        question_tree_refresh()


    def add():
        if not (test_if_question_exist(str(e_question.get()))):
            conn = sqlite3.connect('millionerdb.db')
            c = conn.cursor()
            c.execute("INSERT INTO questions_table VALUES (?,?,?,?,?,?,?)",
                      (e_question.get(), e_answer_a.get(), e_answer_b.get(), e_answer_c.get(), e_answer_d.get(),
                       e_correct_answer.get(), e_difficulty.get()))
            conn.commit()
            conn.close()
        else:
            messagebox.showerror("Error", "Η ερώτηση υπάρχει ήδη!!")
        clear()

    def save():
        if test_if_question_exist(str(e_question.get())):
            conn = sqlite3.connect('millionerdb.db')
            c = conn.cursor()
            c.execute("UPDATE questions_table SET question='" + e_question.get() + "' , answera='" + e_answer_a.get() +
                      "', answerb='" + e_answer_b.get() + "', answerc='" + e_answer_c.get() + "', answerd='" + e_answer_d.get() +
                      "', correct_answer='" + e_correct_answer.get() + "', difficulty='" + e_difficulty.get() +
                      "' WHERE question='" + my_selection_question + "'")
            conn.commit()
            conn.close()
        else:
            add()
        clear()

    def select_record(event):
        global my_selection_question
        my_selection = tree_questions.focus()
        selected_values = tree_questions.item(my_selection, "values")
        my_selection_question = selected_values[0]
        clear_entries()
        e_question.insert(0, selected_values[0])
        e_answer_a.insert(0, selected_values[1])
        e_answer_b.insert(0, selected_values[2])
        e_answer_c.insert(0, selected_values[3])
        e_answer_d.insert(0, selected_values[4])
        e_correct_answer.insert(0, selected_values[5])
        e_difficulty.insert(0, selected_values[6])

    def delete(line):
        conn = sqlite3.connect('millionerdb.db')
        c = conn.cursor()
        if line != "ALL":
            my_selection = tree_questions.focus()
            selected_values = tree_questions.item(my_selection, "values")
            for record in selected_values:
                c.execute("DELETE FROM questions_table WHERE question='" + record + "'")
        else:
            c.execute("DELETE FROM questions_table")
        conn.commit()
        conn.close()
        clear()

    def reset():
        # Γεμίζει τη λίστα με προσωρινές ερωτήσεις
        conn = sqlite3.connect('millionerdb.db')
        c = conn.cursor()
        difficulties = ["easy", "medium", "hard"]
        for difficulty in difficulties:
            for j in range(10):
                c.execute("INSERT INTO questions_table VALUES (?,?,?,?,?,?,?)",
                          ("Ερώτηση δυσκολίας: " + str(difficulty) + " σειρά: " + str(j), "Α", "Β", "Γ", "Δ",
                           random.choice(["Α", "Β", "Γ", "Δ"]), difficulty))
        conn.commit()
        conn.close()
        clear()

    btn_add = Button(root, text="Add", command=add, width=15)
    btn_save = Button(root, text="Save", command=save, width=15)
    btn_delete_one = Button(root, text="Delete", command=lambda: delete("SELECTED"), width=15)
    btn_delete_all = Button(root, text="Delete all", command=lambda: delete("ALL"), width=15)
    btn_reset = Button(root, text="Reset", command=reset, width=15)

    btn_add.grid(row=1, column=8)
    btn_save.grid(row=2, column=8)
    btn_delete_one.grid(row=3, column=8)
    btn_delete_all.grid(row=4, column=8)
    btn_reset.grid(row=5, column=8)

    tree_questions.bind("<Double-1>", select_record)

    mainloop()
