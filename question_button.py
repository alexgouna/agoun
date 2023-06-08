from tkinter import *
import sqlite3
from tkinter import ttk
from tkinter import messagebox
import settings

global my_selection_question


def questions():
    # Θα βρούμε μια λίστα με όλες τις ερωτήσεις και απαντήσεις όπου θα μπορούμε να την επεξεργαστούμε
    root_questions = Toplevel()
    root_questions.geometry("1200x800")
    root_questions.title("Ερωτήσεις παιχνιδιού")
    root_questions.resizable(False, False)

    def close():
        settings.open_window = 0
        root_questions.destroy()

    root_questions.protocol("WM_DELETE_WINDOW", close)

    tree_scrollbar = Scrollbar(root_questions)
    tree_scrollbar.grid(row=0, column=11, sticky=N + S)

    tree_questions = ttk.Treeview(root_questions, yscrollcommand=tree_scrollbar.set, height=25)
    tree_scrollbar.config(command=tree_questions.yview)
    tree_questions['columns'] = (
        "question", "ansewera", "answerb", "answerc", "answerd", "correct_answer", "difficulty")
    tree_questions.column("#0", width=0, stretch=NO)
    tree_questions.column("question", width=236)
    tree_questions.column("ansewera", width=175)
    tree_questions.column("answerb", width=175)
    tree_questions.column("answerc", width=175)
    tree_questions.column("answerd", width=175)
    tree_questions.column("correct_answer", width=175)
    tree_questions.column("difficulty", width=70)

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

    lbl_question = Label(root_questions, text="   Ερώτηση:")
    lbl_answer_a = Label(root_questions, text="   Απάντηση Α:")
    lbl_answer_b = Label(root_questions, text="   Απάντηση Β:")
    lbl_answer_c = Label(root_questions, text="   Απάντηση Γ:")
    lbl_answer_d = Label(root_questions, text="   Απάντηση Δ:")
    lbl_correct_answer = Label(root_questions, text="   Σωστή απάντηση:")
    lbl_difficulty = Label(root_questions, text="   Δυσκολία:")

    lbl_question.grid(row=1, column=0, sticky=W)
    lbl_answer_a.grid(row=2, column=0, sticky=W)
    lbl_answer_b.grid(row=3, column=0, sticky=W)
    lbl_answer_c.grid(row=4, column=0, sticky=W)
    lbl_answer_d.grid(row=5, column=0, sticky=W)
    lbl_correct_answer.grid(row=6, column=0, sticky=W)
    lbl_difficulty.grid(row=7, column=0, sticky=W)

    e_question = Entry(root_questions)
    e_answer_a = Entry(root_questions)
    e_answer_b = Entry(root_questions)
    e_answer_c = Entry(root_questions)
    e_answer_d = Entry(root_questions)
    e_correct_answer = Entry(root_questions)
    combo = ttk.Combobox(root_questions, state="readonly", values=["easy", "medium", "difficult"])


    e_question.grid(row=1, column=1, columnspan=6, pady=4, sticky=W + E)
    e_answer_a.grid(row=2, column=1, columnspan=6, pady=4, sticky=W + E)
    e_answer_b.grid(row=3, column=1, columnspan=6, pady=4, sticky=W + E)
    e_answer_c.grid(row=4, column=1, columnspan=6, pady=4, sticky=W + E)
    e_answer_d.grid(row=5, column=1, columnspan=6, pady=4, sticky=W + E)
    e_correct_answer.grid(row=6, column=1, columnspan=6, pady=4, sticky=W + E)
    combo.grid(row=7, column=1, columnspan=6, pady=4, sticky=W + E)
    combo.set("easy")

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
        combo.set("easy")

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
                       e_correct_answer.get(), combo.get()))
            conn.commit()
            conn.close()
        else:
            messagebox.showerror("Error", "Η ερώτηση υπάρχει ήδη!!")
        clear()

    def save():
        if test_if_question_exist(str(e_question.get())):
            if messagebox.askyesno("Προσοχή!!", "Η ερώτηση υπάρχει ήδη!!\n Να αντικατασταθεί;"):
                conn = sqlite3.connect('millionerdb.db')
                c = conn.cursor()
                c.execute(
                    "UPDATE questions_table SET question='" + e_question.get() + "' , answera='" + e_answer_a.get() +
                    "', answerb='" + e_answer_b.get() + "', answerc='" + e_answer_c.get() + "', answerd='" + e_answer_d.get() +
                    "', correct_answer='" + e_correct_answer.get() + "', difficulty='" + combo.get() +
                    "' WHERE question='" + str(e_question.get()) + "'")
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
        combo.set(selected_values[6])


    def delete(line):
        conn = sqlite3.connect('millionerdb.db')
        c = conn.cursor()
        if line == "ALL":
            c.execute("DELETE FROM questions_table")
        else:
            my_selection = tree_questions.selection()
            for item in my_selection:
                c.execute("DELETE FROM questions_table WHERE question='" + tree_questions.item(item, "values")[0] + "'")
        conn.commit()
        conn.close()
        clear()



    btn_new = Button(root_questions, text="New", command=clear_entries, width=15)
    btn_save = Button(root_questions, text="Save", command=save, width=15)
    btn_delete_one = Button(root_questions, text="Delete", command=lambda: delete("SELECTED"), width=15)
    btn_delete_all = Button(root_questions, text="Delete all", command=lambda: delete("ALL"), width=15)

    btn_new.grid(row=1, column=8)
    btn_save.grid(row=2, column=8)
    btn_delete_one.grid(row=3, column=8)
    btn_delete_all.grid(row=4, column=8)


    tree_questions.bind("<Double-1>", select_record)

    mainloop()
