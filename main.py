from tkinter import *
import random
import time
import sqlite3
from PIL import ImageTk, Image


def millioner():
    global image_num
    global timer
    global lbl_timer
    global btnanswera
    global btnanswerb
    global btnanswerc
    global btnanswerd
    global question
    global questions_easy
    global questions_medium
    global questions_hard
    global position
    global btnhelp1
    global btnhelp2
    global btnhelp3
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
        print("correct!! go to next...")
        next_amount()
        new_question()
        kerdismeno_poso = position * 10
        position = position + 1
        lblquestion.config(text=question[0])
        btnanswera.config(text=question[1], state=NORMAL)
        btnanswerb.config(text=question[2], state=NORMAL)
        btnanswerc.config(text=question[3], state=NORMAL)
        btnanswerd.config(text=question[4], state=NORMAL)

    def give_answer(answer):
        global timer
        global total_time

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
        global btnhelp1
        global btnanswera
        global btnanswerb
        global btnanswerc
        global btnanswerd

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
            btnanswera.config(state=DISABLED)
        if not (num1 == 2 or num2 == 2):
            btnanswerb.config(state=DISABLED)
        if not (num1 == 3 or num2 == 3):
            btnanswerc.config(state=DISABLED)
        if not (num1 == 4 or num2 == 4):
            btnanswerd.config(state=DISABLED)
        btnhelp1.config(command="", image=img_help_50_x, padx=50, pady=20)

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

    # help propose an answer
    def help2():
        global position
        global btnhelp2

        print("help2")
        if position <= 5:
            my_pc_answer = pc_answer(25)
        elif position <= 10:
            my_pc_answer = pc_answer(20)
        else:
            my_pc_answer = pc_answer(15)
        print(my_pc_answer)
        btnhelp2.config(command="", image=img_help_percent_x, padx=50, pady=20)

    def help3():
        global btnhelp3

        print("help3")
        new_question()
        lblquestion.config(text=question[0])
        btnanswera.config(text=question[1], state=NORMAL)
        btnanswerb.config(text=question[2], state=NORMAL)
        btnanswerc.config(text=question[3], state=NORMAL)
        btnanswerd.config(text=question[4], state=NORMAL)
        btnhelp3.config(command="", image=img_help_change_x, padx=50, pady=20)

    def start_game():
        global lbl_timer
        global timer

        lblquestion.place(x=100, y=100)
        btnanswera.place(x=100, y=200)
        btnanswerb.place(x=100, y=300)
        btnanswerc.place(x=200, y=200)
        btnanswerd.place(x=200, y=300)
        btnhelp1.config(state=NORMAL)
        btnhelp2.config(state=NORMAL)
        btnhelp3.config(state=NORMAL)

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
    lframe = Frame(top_root)
    rframe = Frame(top_root)
    lframe.grid(row=0, column=0)
    rframe.grid(row=0, column=1)

    img_help_50 = ImageTk.PhotoImage(Image.open("images/50.png"))
    img_help_50_x = ImageTk.PhotoImage(Image.open("images/50_x.png"))
    img_help_change = ImageTk.PhotoImage(Image.open("images/change.png"))
    img_help_change_x = ImageTk.PhotoImage(Image.open("images/change_x.png"))
    img_help_percent = ImageTk.PhotoImage(Image.open("images/percent.png"))
    img_help_percent_x = ImageTk.PhotoImage(Image.open("images/percent_x.png"))
    img_answer = ImageTk.PhotoImage(Image.open("images/123.png"))
    img_questions = ImageTk.PhotoImage(Image.open("images/questions.png"))


    # lframe
    toplframe = Frame(lframe, bg="black")
    midlframe = Frame(lframe, bg="blue")
    botlframe = Frame(lframe, bg="red")
    toplframe.grid(row=0, column=0)
    midlframe.grid(row=1, column=0)
    botlframe.grid(row=2, column=0)

    # toplframe
    lbl_bg_top_l = Label(toplframe, bg= "black", text="",padx=248, pady=40)
    lbl_bg_top_l.grid(row=0,column=0,columnspan=3)
    btnhelp1 = Button(toplframe,bg="black", bd=0,activebackground="black",  image=img_help_50,width=150, height = 80, padx=100, pady=20, command=help1, state=DISABLED)
    btnhelp1.grid(row=0, column=0)
    btnhelp2 = Button(toplframe, image=img_help_percent,bg="black", bd=0,activebackground="black", width=150, height = 80, padx=50, pady=20, command=help2, state=DISABLED)
    btnhelp2.grid(row=0, column=1)
    btnhelp3 = Button(toplframe, image=img_help_change, bg="black", bd=0,activebackground="black", width=150, height = 80, padx=50, pady=20,command=help3, state=DISABLED)
    btnhelp3.grid(row=0, column=2)

    # midlframe
    midlframe.config(width=500, height=150)
    lbl_timer = Label(midlframe, text="00",font=("Arial",50),padx =211, pady = 30, bg="black",fg="white")
    lbl_timer.grid(row=0, column=0)

    # botlframe
    botlframe.config(width=500, height=350)
    lbl_img_questions = Label(botlframe,image=img_questions,padx=20,pady=50)
    # lbl_img_answer = Label(botlframe, image=img_answer,padx=20,pady=50)
    #
    # l_img_questions.grid(row=0,column=0)
    # lbl_img_answer.grid(row=1, column=0)

    lblquestion = Label(botlframe, text=question[0], bg="black", fg="white")
    btnanswera = Button(botlframe, text=question[1], bg="black", fg="white", command=lambda: give_answer("A"))
    btnanswerb = Button(botlframe, text=question[2], bg="black", fg="white", command=lambda: give_answer("B"))
    btnanswerc = Button(botlframe, text=question[3], bg="black", fg="white", command=lambda: give_answer("C"))
    btnanswerd = Button(botlframe, text=question[4], bg="black", fg="white", command=lambda: give_answer("D"))

    # rframe
    padx = 145
    pady = 290
    label1 = Label(rframe, text="1", padx=padx, pady=pady, bg="blue")
    label2 = Label(rframe, text="2", padx=padx, pady=pady, bg="blue")
    label3 = Label(rframe, text="3", padx=padx, pady=pady, bg="blue")
    label4 = Label(rframe, text="4", padx=padx, pady=pady, bg="blue")
    label5 = Label(rframe, text="5", padx=padx, pady=pady, bg="blue")
    label6 = Label(rframe, text="6", padx=padx, pady=pady, bg="blue")
    label7 = Label(rframe, text="7", padx=padx, pady=pady, bg="blue")
    label8 = Label(rframe, text="8", padx=padx, pady=pady, bg="blue")
    label9 = Label(rframe, text="9", padx=padx, pady=pady, bg="blue")
    label10 = Label(rframe, text="10", padx=padx, pady=pady, bg="blue")
    label11 = Label(rframe, text="11", padx=padx, pady=pady, bg="blue")
    label12 = Label(rframe, text="12", padx=padx, pady=pady, bg="blue")
    label13 = Label(rframe, text="13", padx=padx, pady=pady, bg="blue")
    label14 = Label(rframe, text="14", padx=padx, pady=pady, bg="blue")
    label15 = Label(rframe, text="15", padx=padx, pady=pady, bg="blue")

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
    #top_lvl.resizable(False, False)

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

#
# conn = sqlite3.connect('millionerdb.db')
# c = conn.cursor()
# c.execute("""CREATE TABLE questions_table (
#             question text,
#             answer_a text,
#             answer_b text,
#             answer_c text,
#             answer_d text,
#             answer_correct text,
#             dificulty text )""")
# conn.commit()
# conn.close()
#
# conn = sqlite3.connect('millionerdb.db')
# c = conn.cursor()
#
# for row in range(50):
#     sosto=random.choice(["A","B","C","D"])
#     diskolia = random.choice(["easy", "medium", "hard"])
#     c.execute("INSERT INTO questions_table VALUES (?,?,?,?,?,?,?)",
#           ("Answer "+ diskolia + " " + str(row + 1),
#            "A","B","C","D",sosto,diskolia))
# conn.commit()
# conn.close()
#
#
# conn = sqlite3.connect('millionerdb.db')
# c = conn.cursor()
# c.execute("""CREATE TABLE rank_table (
#             username text,
#             score integer )""")
# conn.commit()
# conn.close()


root = Tk()
root.geometry("400x400")
root.title("Main")
root.resizable(False, False)
#  demo game start
millioner()
btn_new_game = Button(root, text="New Game", command=millioner)
btn_rank = Button(root, text="Rank", command=rank)
btn_edit_questions = Button(root, text="Edit questions", command=edit_questions)
btn_exit = Button(root, text="EXIT", command=exit)
btn_new_game.grid(row=0, column=0)
btn_rank.grid(row=1, column=0)
btn_edit_questions.grid(row=2, column=0)
btn_exit.grid(row=3, column=0)
mainloop()