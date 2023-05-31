from tkinter import *
from PIL import ImageTk, Image
from question_button import questions as question_button_questions
import rank_button
from game import start_game
import settings
from tkinter import messagebox
import sqlite3

settings.open_window = 0


def test_questions():
    conn = sqlite3.connect('millionerdb.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions_table")
    my_questions = c.fetchall()
    conn.commit()
    conn.close()
    if len(my_questions) == 0:
        messagebox.showinfo(f"Προσοχή!!", "Δεν υπάρχουν ερωτήσεις στο παιχνίδι!!\nΦτιάξε τις δικές σου!!")
        questions()
        return False
    else:
        count_easy = 0
        count_medium = 0
        count_hard = 0
        for q in my_questions:
            if q[6] == "easy":
                count_easy += 1
            elif q[6] == "medium":
                count_medium += 1
            elif q[6] == "hard":
                count_hard += 1
        if count_easy < 7 or count_easy < 7 or count_easy < 7:
            messagebox.showinfo(f"Προσοχή!!", "Πρέπει να υπάρχουν τουλάχιστον 7 ερωτήσεις από κάθε κατηγορία!!")
            questions()
            return False
        else:
            return True


# Εδώ αρχίζει το παιχνίδι!!!!
def millioner():
    if test_questions():
        if settings.open_window == 1:
            messagebox.showinfo(f"Προσοχή!!",
                                f"Έχεις ανοιχτό το παράθυρο {settings.my_window}.. \nΚλείσε το παράθυρο για να ξεκινήσει το παιχνίδι!!")
        else:
            settings.my_window = "Millioner"
            settings.open_window = 1
            start_game(root)


def rank():
    if test_questions():
        if settings.open_window == 1:
            messagebox.showinfo(f"Προσοχή!!",
                                f"Έχεις ανοιχτό το παράθυρο {settings.my_window}.. \nΚλείσε το παράθυρο για να δεις τον πίνακα βαθμολογίας!!")
        else:
            settings.my_window = "βαθμολογίας"
            settings.open_window = 1
            rank_button.rank()


def questions():
    if settings.open_window == 1:
        messagebox.showinfo(f"Προσοχή!!",
                            f"Έχεις ανοιχτό το παράθυρο {settings.my_window}.. \nΚλείσε το παράθυρο για να επεξεργαστείς τις ερωτήσεις!!")
    else:
        settings.my_window = "ερωτήσεις"
        settings.open_window = 1
        question_button_questions()


# αρχική κεντρική οθόνη
root = Tk()
root.geometry("400x400")
root.title("Main")
my_canvas = Canvas(root, width=400, height=400)

img = Image.open('assets\millioner_logo.jpg').resize((400, 400))
img = ImageTk.PhotoImage(img)

root.resizable(False, False)
my_canvas.pack(fill="both", expand=True)
my_canvas.create_image(0, 0, image=img, anchor="nw")

# Κουμπί για νέο παιχνίδι
btn_new_game = Button(root, text="New Game", command=millioner, height=2, width=20)
# Κουμπί για εμφάνιση του πίνακα κατάταξης
btn_rank = Button(root, text="Rank", command=rank, height=2, width=20)
# Κουμπί για επεξεργασία ερωτήσεων
btn_questions = Button(root, text="Game questions", command=questions, height=2, width=20)

my_canvas.create_window(20, 20, anchor="nw", window=btn_new_game)
my_canvas.create_window(20, 80, anchor="nw", window=btn_rank)
my_canvas.create_window(20, 140, anchor="nw", window=btn_questions)

test_questions()

root.mainloop()
