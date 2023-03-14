from tkinter import *
import random
import time
import sqlite3
from PIL import ImageTk, Image


# Εδώ αρχίζει το παιχνίδι!!
def millioner():

     # Εισάγω νέα ερώτηση στο παιχνίδι.
    def new_question():
        # Εισάγω μία τυχαία ερώτηση στη λίστα question ανάλογα το επίπεδο δυσκολίας που βρίσκεται ο παίχτης
        pass

    def game_over():
        # Αν η απάντηση είναι λάθος τότε υπολογίζει τους βαθμούς σύμφωνα με τις οδηγίες, ζητάει ένα username και τα αποθηκεύει στον πίνακα rank_table
        pass

    def correct_answer():
        # Αν η απάντηση είναι σωστή τότε αλλάζει σε επόμενη ερώτηση με new_question()
        # Αλλάζει την εικόνα με τα ποσά
        # κρατάει στοιχεία όπως συνολικός χρόνος και κερδισμένο ποσό
        # αυξάνει το position κατά 1
        pass


    def give_answer(answer):
        # Αν το position είναι 15 σημαίνει ότι ολοκλήρωσε όλες τις ερωτήσεις επιτυχώς κλίνει το πρόγραμμα
        if position == 15:
            # Μύνημα ΣΥΓΧΑΡΗΤΗΡΙΑ κέρδισες το παιχνίδι
            game_over()
        else:
            if question[5] != answer: # Αν η απάντηση είναι λάθος κλίνει το πρόγραμμα
                game_over()
            else:
                correct_answer()


    # help 50/50
    def help1():
        # Απενεργοποίησε δύο κουμπιά με λανθασμένη απάντηση
        # Άλλαξε την εικόνα με την αντίστοιχη με Χ
        pass


    # help2 PC propose an answer
    def help2():
        # Δώσε μία πιθανή απάντηση με ποσοστό επιτυχίας.
        # Δεν είναι υποχρεωτικό να επιστρέψει την σωστή απάντηση
        pass

    def help3():
        # Αλλάζει την ερώτηση με μία νέα
        pass


    def start_game_gui():
        # Ξεκινάει το παιχνίδι και φτιάχνει το GUI.
        # Περιέχεται ένα κουμπί για κάθε βοήθεια
        # Περιέχονται 4 κουμπιά ένα για κάθε απάντηση. με εντολή give_answer(answer) όπου answer έιναι η απάντηση του κουμπιού
        # Προσοχή! Θέλουμε και ένα χρονόμετρο 60sec που θα χάνει ο παίχτης αν δεν απαντήσει εγκαίρως
        pass

        # Συνολικός χρόνος παιχνιδιού

    total_time = 0
    # Συνολικό score παίχτη
    total_score = 0
    # Τρέχουσα σειράερώτησης
    position = 1

    # Έχω δημιουργήσει μία βάση δεδομένων millionerdb.db που περιέχει δύο πίνακες
    # Πίνακας questions_table (question, ansewera, answerb, answerc, answerd, dificulty)
    # Πίνακας rank_table (name, score)

    # Από τη βάση δεδομένων φτιάχνω τρεις λίστες ανάλογα τη δυσκολία των ερωτήσεων
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

    # Στη λίστα question βάζω μία τυχαία ερώτηση από τις εύκολες ερωτήσεις
    random_num = random.randrange(0, len(questions_easy) - 1)
    question = questions_easy[random_num]
    questions_easy.pop(random_num)

    start_game_gui()


def rank():
    # Δημιουργεί ένα Toplevel που εμφανίζει από τον πίνακα rank_table το όνομα και τουσ βαθμούς όπως έχουν καταγραφεί έως τώρα.
    pass


# αρχική κεντρική οθόνη
root = Tk()
root.geometry("400x400")
root.title("Main")
root.resizable(False, False)

# Κουμπί για νέο παιχνίδι
btn_new_game = Button(root, text="New Game", command=millioner)
# Κουμπί για εμφάνιση του πίνακα κατάταξης
btn_rank = Button(root, text="Rank", command=rank)

btn_new_game.grid(row=0, column=0)
btn_rank.grid(row=1, column=0)

mainloop()
