from tkinter import *
import random
import time
import sqlite3
from PIL import ImageTk, Image


def millioner():
    global image_num
    global timer
    global lbl_timer
    global lbl_help2_answer
    global btn_answer_a
    global btn_answer_b
    global btn_answer_c
    global btn_answer_d
    global question
    global questions_easy
    global questions_medium
    global questions_hard
    global position
    global btn_help_1
    global btn_help_2
    global btn_help_3
    global total_time
    global kerdismeno_poso

    total_time = 1
    kerdismeno_poso = 1

    conn = sqlite3.connect('millionerdb.db')
    c = conn.cursor()
    c.execute("SELECT *  FROM questions_table WHERE dificulty = 'easy'")
    questions_easy = c.fetchall()
    c.execute("SELECT *  FROM questions_table WHERE dificulty = 'medium'")
    questions_medium = c.fetchall()
    c.execute("SELECT *  FROM questions_table WHERE dificulty = 'hard'")
    questions_hard = c.fetchall()
    conn.commit()
    conn.close()

    random_num = random.randrange(0, len(questions_easy) - 1)
    question = questions_easy[random_num]
    questions_easy.pop(random_num)
    timer = 600
    position = 1

    # Εισάγω νέα ερώτηση στο παιχνίδι
    def new_question():
        global question
        global questions_easy
        global questions_medium
        global questions_hard

        if position < 5:
            random_num = random.randrange(0, len(questions_easy) - 1)
            question = questions_easy[random_num]
            questions_easy.pop(random_num)
        elif position < 10:
            random_num = random.randrange(0, len(questions_medium) - 1)
            question = questions_medium[random_num]
            questions_medium.pop(random_num)
        else:
            random_num = random.randrange(0, len(questions_hard) - 1)
            question = questions_hard[random_num]
            questions_hard.pop(random_num)

    def next_amount():
        print("Επόμενο ποσό")
        global image_num
        image_num = image_num + 1
        label_all[image_num].grid(row=0, column=1)

    def whrong_answer():
        global total_time
        global kerdismeno_poso

        def submit():
            print(total_time)
            print(kerdismeno_poso)
            print(vathmoi)
            conn = sqlite3.connect('millionerdb.db')
            c = conn.cursor()
            c.execute("INSERT INTO rank_table VALUES (?,?)", (str(name.get()), vathmoi))
            conn.commit()
            conn.close()
            rank_root.destroy()
            rank_root.update()
            top_root.destroy()
            top_root.update()
            root.deiconify()

        rank_root = Toplevel()
        rank_root.title("")
        vathmoi = int(kerdismeno_poso / total_time)
        lbl_point = Label(rank_root, text="Κέρδισες " + str(vathmoi) + " βαθμούς")
        lbl_name = Label(rank_root, text="Όνομα: ")
        name = Entry(rank_root)
        btn_submit = Button(rank_root, text="Submit", command=submit)
        lbl_point.grid(row=0, column=0, columnspan=2)
        lbl_name.grid(row=1, column=0)
        name.grid(row=1, column=1)
        btn_submit.grid(row=2, column=0, columnspan=2)
        mainloop()
        print("Whrong answer...")

    def game_over():
        print("game over!!!")
        top_root.quit()

    def correct_answer():
        global question
        global position
        global kerdismeno_poso
        global lbl_help2_answer
        print("correct!! go to next...")
        next_amount()
        new_question()
        kerdismeno_poso = position * 10
        position = position + 1
        lbl_question.config(text=question[0])
        btn_answer_a.config(text=question[1], state=NORMAL)
        btn_answer_b.config(text=question[2], state=NORMAL)
        btn_answer_c.config(text=question[3], state=NORMAL)
        btn_answer_d.config(text=question[4], state=NORMAL)
        lbl_timer.config(padx=211)
        lbl_help2_answer.destroy()

    def give_answer(answer):
        global timer
        global total_time
        global lbl_help2_answer

        if position == 15:
            game_over()
        else:
            if question[5] != answer:
                whrong_answer()
            else:
                correct_answer()
                total_time = total_time + int((600 - timer) / 10)
                timer = 600

    # help 50/50
    def help1():
        global btn_help_1
        global btn_answer_a
        global btn_answer_b
        global btn_answer_c
        global btn_answer_d

        if question[5] == "A":
            num1 = 1
            num2 = random.choice([2, 3, 4])
        elif question[5] == "B":
            num1 = 2
            num2 = random.choice([1, 3, 4])
        elif question[5] == "C":
            num1 = 3
            num2 = random.choice([1, 2, 4])
        else:
            num1 = 4
            num2 = random.choice([1, 2, 3])
        print(num1, num2)
        if not (num1 == 1 or num2 == 1):
            btn_answer_a.config(state=DISABLED)
        if not (num1 == 2 or num2 == 2):
            btn_answer_b.config(state=DISABLED)
        if not (num1 == 3 or num2 == 3):
            btn_answer_c.config(state=DISABLED)
        if not (num1 == 4 or num2 == 4):
            btn_answer_d.config(state=DISABLED)
        btn_help_1.config(command="", state=DISABLED)

    def pc_answer(bonus):
        num = (random.random(), random.random(), random.random(), random.random())
        num1 = (num[0] / (num[0] + num[1] + num[2] + num[3])) * (100 - bonus)
        num2 = (num[1] / (num[0] + num[1] + num[2] + num[3])) * (100 - bonus)
        num3 = (num[2] / (num[0] + num[1] + num[2] + num[3])) * (100 - bonus)
        num4 = (num[3] / (num[0] + num[1] + num[2] + num[3])) * (100 - bonus)
        if question[5] == "A":
            num1 = num1 + bonus
        if question[5] == "B":
            num2 = num2 + bonus
        if question[5] == "C":
            num3 = num3 + bonus
        if question[5] == "D":
            num4 = num4 + bonus
        max = [num1, "A"]
        if max[0] < num2:
            max[0] = num2
            max[1] = "B"
        if max[0] < num3:
            max[0] = num3
            max[1] = "C"
        if max[0] < num4:
            max[0] = num4
            max[1] = "D"
        return max

    # help2 PC propose an answer
    def help2():
        global btn_help_2
        global lbl_help2_answer

        print("help2")
        if position <= 5:
            my_pc_answer = pc_answer(30)
        elif position <= 10:
            my_pc_answer = pc_answer(20)
        else:
            my_pc_answer = pc_answer(15)

        lbl_help2_answer = Label(mid_l_frame , text="Με ποσοστό " + str(int(my_pc_answer[0])) + "% δίνεται η απάντηση: \n" + str(my_pc_answer[1]),
                            font=("Arial", 10), width= 30, pady=30, bg="black", fg="white")
        lbl_help2_answer.grid(row=0,column=1)
        lbl_timer.config(padx=88)
        btn_help_2.config(state=DISABLED)

    def help3():
        global btn_help_3

        print("help3")
        new_question()
        lbl_question.config(text=question[0])
        btn_answer_a.config(text=question[1], state=NORMAL)
        btn_answer_b.config(text=question[2], state=NORMAL)
        btn_answer_c.config(text=question[3], state=NORMAL)
        btn_answer_d.config(text=question[4], state=NORMAL)
        btn_help_3.config(state=DISABLED)

    def start_game():
        global lbl_timer
        global timer
        global lbl_help2_answer

        lbl_question.place(x=100, y=100)
        btn_answer_a.place(x=100, y=200)
        btn_answer_b.place(x=100, y=300)
        btn_answer_c.place(x=200, y=200)
        btn_answer_d.place(x=200, y=300)
        btn_help_1.config(state=NORMAL)
        btn_help_2.config(state=NORMAL)
        btn_help_3.config(state=NORMAL)

        while True:
            if timer > 0:
                lbl_timer.config(text=int(timer / 10))
                lbl_timer.grid(row=0, column=0)
                timer = timer - 1
                top_root.update()
                time.sleep(0.1)
            else:
                lbl_timer.config(text="00")
                game_over()
                break

    root.withdraw()
    top_root = Toplevel()
    top_root.geometry("800x600")
    top_root.title("Millioner")
    top_root.config(bg="black")
    # top_root.resizable(False, False)
    l_frame = Frame(top_root)
    r_frame = Frame(top_root)
    l_frame.grid(row=0, column=0)
    r_frame.grid(row=0, column=1)

    # l_frame
    top_l_frame = Frame(l_frame, bg="black")
    mid_l_frame = Frame(l_frame, bg="blue")
    bot_l_frame = Frame(l_frame, bg="red")
    top_l_frame.grid(row=0, column=0)
    mid_l_frame.grid(row=1, column=0)
    bot_l_frame.grid(row=2, column=0)

    # top_l_frame
    lbl_bg_top_l = Label(top_l_frame, bg="black", text="", padx=248, pady=40)
    lbl_bg_top_l.grid(row=0, column=0, columnspan=3)
    btn_help_1 = Button(top_l_frame, text="50", bg="red", bd=0, activebackground="black", padx=50, pady=20,
                      command=help1, state=DISABLED)
    btn_help_1.grid(row=0, column=0)
    btn_help_2 = Button(top_l_frame, text="percent", bg="red", bd=0, activebackground="black", padx=50, pady=20,
                      command=help2, state=DISABLED)
    btn_help_2.grid(row=0, column=1)
    btn_help_3 = Button(top_l_frame, text="change", bg="red", bd=0, activebackground="black", padx=50, pady=20,
                      command=help3, state=DISABLED)
    btn_help_3.grid(row=0, column=2)

    # mid_l_frame
    mid_l_frame.config(width=500, height=150)
    lbl_timer = Label(mid_l_frame, text="00", font=("Arial", 50), padx=211, pady=30, bg="black", fg="white")
    lbl_timer.grid(row=0, column=0)

    # bot_l_frame
    bot_l_frame.config(width=500, height=350)
    lbl_question = Label(bot_l_frame, text=question[0], bg="black", fg="white")
    btn_answer_a = Button(bot_l_frame, text=question[1], bg="black", fg="white", command=lambda: give_answer("A"))
    btn_answer_b = Button(bot_l_frame, text=question[2], bg="black", fg="white", command=lambda: give_answer("B"))
    btn_answer_c = Button(bot_l_frame, text=question[3], bg="black", fg="white", command=lambda: give_answer("C"))
    btn_answer_d = Button(bot_l_frame, text=question[4], bg="black", fg="white", command=lambda: give_answer("D"))

    # r_frame
    padx = 145
    pady = 290
    label1 = Label(r_frame, text="1", padx=padx, pady=pady, bg="blue")
    label2 = Label(r_frame, text="2", padx=padx, pady=pady, bg="blue")
    label3 = Label(r_frame, text="3", padx=padx, pady=pady, bg="blue")
    label4 = Label(r_frame, text="4", padx=padx, pady=pady, bg="blue")
    label5 = Label(r_frame, text="5", padx=padx, pady=pady, bg="blue")
    label6 = Label(r_frame, text="6", padx=padx, pady=pady, bg="blue")
    label7 = Label(r_frame, text="7", padx=padx, pady=pady, bg="blue")
    label8 = Label(r_frame, text="8", padx=padx, pady=pady, bg="blue")
    label9 = Label(r_frame, text="9", padx=padx, pady=pady, bg="blue")
    label10 = Label(r_frame, text="10", padx=padx, pady=pady, bg="blue")
    label11 = Label(r_frame, text="11", padx=padx, pady=pady, bg="blue")
    label12 = Label(r_frame, text="12", padx=padx, pady=pady, bg="blue")
    label13 = Label(r_frame, text="13", padx=padx, pady=pady, bg="blue")
    label14 = Label(r_frame, text="14", padx=padx, pady=pady, bg="blue")
    label15 = Label(r_frame, text="15", padx=padx, pady=pady, bg="blue")

    label_all = [label1, label2, label3, label4, label5, label6, label7, label8, label9, label10, label11, label12,
                 label13, label14, label15]
    image_num = 0
    label_all[image_num].grid(row=0, column=1)
    try:
        start_game()
    except:
        root.deiconify()
        mainloop()
    mainloop()


def rank():
    top_lvl = Toplevel()
    top_lvl.title("Rank Table")
    top_lvl.geometry("400x400")
    top_lvl.resizable(False, False)
    conn = sqlite3.connect('millionerdb.db')
    c = conn.cursor()
    my_ranks = c.execute("SELECT * FROM rank_table")
    lbl_name_title = Label(top_lvl, text="Όνομα")
    lbl_point_title = Label(top_lvl, text="Βαθμοί")
    lbl_name_title.grid(row=0, column=0)
    lbl_point_title.grid(row=0, column=1)
    my_row = 1

    for rank in my_ranks:
        lbl_name = Label(top_lvl, text=rank[0])
        lbl_point = Label(top_lvl, text=rank[1])
        lbl_name.grid(row=my_row, column=0)
        lbl_point.grid(row=my_row, column=1)
        my_row = my_row + 1
    conn.commit()
    conn.close()
    mainloop()


def edit_questions():
    top_lvl = Toplevel()
    top_lvl.title("Edit questions")
    top_lvl.geometry("800x400")
    # top_lvl.resizable(False, False)

    lbl_question = Label(top_lvl, text="Ερώτηση")
    lbl_answer_a = Label(top_lvl, text="Απάντηση Α")
    lbl_answer_b = Label(top_lvl, text="Απάντηση Β")
    lbl_answer_c = Label(top_lvl, text="Απάντηση Γ")
    lbl_answer_d = Label(top_lvl, text="Απάντηση Δ")
    lbl_answer_correct = Label(top_lvl, text="Σωστή απάντηση")
    lbl_dificulty = Label(top_lvl, text="Δυσκολία")
    lbl_question.grid(row=0, column=0)
    lbl_answer_a.grid(row=0, column=1)
    lbl_answer_b.grid(row=0, column=2)
    lbl_answer_c.grid(row=0, column=3)
    lbl_answer_d.grid(row=0, column=4)
    lbl_answer_correct.grid(row=0, column=5)
    lbl_dificulty.grid(row=0, column=6)
    conn = sqlite3.connect('millionerdb.db')
    c = conn.cursor()
    questions = c.execute("SELECT * FROM questions_table")
    my_row = 1
    my_entries = []
    for question in questions:
        e1 = Entry(top_lvl)
        e2 = Entry(top_lvl)
        e3 = Entry(top_lvl)
        e4 = Entry(top_lvl)
        e5 = Entry(top_lvl)
        e6 = Entry(top_lvl)
        e7 = Entry(top_lvl)
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        e7.delete(0, END)
        e1.insert(0, question[0])
        e2.insert(0, question[1])
        e3.insert(0, question[2])
        e4.insert(0, question[3])
        e5.insert(0, question[4])
        e6.insert(0, question[5])
        e7.insert(0, question[6])
        e1.grid(row=my_row, column=0)
        e2.grid(row=my_row, column=1)
        e3.grid(row=my_row, column=2)
        e4.grid(row=my_row, column=3)
        e5.grid(row=my_row, column=4)
        e6.grid(row=my_row, column=5)
        e7.grid(row=my_row, column=6)
        my_entries.append([e1, e2, e3, e4, e5, e6, e7])
        my_row = my_row + 1
    conn.commit()
    conn.close()

    def save():
        conn = sqlite3.connect('millionerdb.db')
        c = conn.cursor()
        c.execute("DELETE FROM questions_table")
        for entry in my_entries:
            c.execute("INSERT INTO questions_table VALUES (?,?,?,?,?,?,?)",
                      (entry[0].get(), entry[1].get(), entry[2].get(), entry[3].get(), entry[4].get(), entry[5].get(),
                       entry[6].get()))
        conn.commit()
        conn.close()

    btn_save = Button(top_lvl, text="Save", command=save)
    btn_save.grid(row=my_row, column=0, columnspan=2)
    mainloop()


root = Tk()
root.geometry("400x400")
root.title("Main")
root.resizable(False, False)

btn_new_game = Button(root, text="New Game", command=millioner)
btn_rank = Button(root, text="Rank", command=rank)

btn_new_game.grid(row=0, column=0)
btn_rank.grid(row=1, column=0)

mainloop()
