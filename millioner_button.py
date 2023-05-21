from tkinter import *
import random
import time
import sqlite3
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import settings
global my_selection_question


def millioner():


    # Εισάγω νέα ερώτηση στο παιχνίδι!
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
    def help5050(question):
        # Παίρνεις μία λίστα question.
        # Επιλέγεις δύο τυχαίες από τις λάθος απαντήσεις και επιστρέφεις την ίδια λίστα με 0 στην θέση αυτών των απαντήσεων
        # ΠΧ. από ('Ερώτηση δυσκολίας: easy σειρά: 5', 'Α', 'Β', 'Γ', 'Δ', 'Β', 'easy')
        # επιστρέφεις ('Ερώτηση δυσκολίας: easy σειρά: 5', 'Α', 'Β', 0, 0, 'Β', 'easy')
        pass


    # help2 PC propose an answer
    def helppc(question):
        # Δώσε μία πιθανή απάντηση με ποσοστό επιτυχίας.
        # Δεν είναι υποχρεωτικό να επιστρέψει τη σωστή απάντηση
        # Αν είναι εύκολη δώσε ένα πλεονέκτημα στη σωστή απάντηση 35%
        # Αν είναι μεσαία δώσε ένα πλεονέκτημα στη σωστή απάντηση 25%
        # Αν είναι δύσκολη δώσε ένα πλεονέκτημα στη σωστή απάντηση 15%
        # Πχ με σωστή τη Β θα έχουμε:
        # Α = 21%
        # Β = 18% + 35%(πλεονέκτημα) = 53%
        # Γ = 12%
        # Δ = 14%
        pass

    def helpchange(question):
        # Αλλάζει την ερώτηση με μία νέα του ίδιου επιπέδου
        pass



    # Συνολικός χρόνος παιχνιδιού
    total_time = 0
    # Συνολικό score παίχτη
    total_score = 0
    # Τρέχουσα σειράερώτησης
    position = 1

    # Έχω δημιουργήσει μία βάση δεδομένων millionerdb.db που περιέχει δύο πίνακες
    # Πίνακας questions_table (question, ansewera, answerb, answerc, answerd, correct_answer, difficulty)
    # Πίνακας rank_table (name, score)


def my_questions():
    # Από τη βάση δεδομένων φτιάχνω τρεις λίστες ανάλογα τη δυσκολία των ερωτήσεων
    conn = sqlite3.connect('millionerdb.db')
    c = conn.cursor()
    c.execute("SELECT *  FROM questions_table WHERE difficulty = 'easy'")
    questions_easy = c.fetchall()
    c.execute("SELECT *  FROM questions_table WHERE difficulty = 'medium'")
    questions_medium = c.fetchall()
    c.execute("SELECT *  FROM questions_table WHERE difficulty = 'hard'")
    questions_hard = c.fetchall()
    conn.commit()
    conn.close()

    questions_temp1 = []
    questions_temp2 = []
    questions_temp3 = []
    # 5 τυχαίες ερωτήσεις από τη βάση δεδομένων + 1 επιπλέον για περίπτωση βοήθειας αλλαγής ερώτησης
    for i in range(6):
        random_num1 = random.randrange(0, len(questions_easy) - 1)
        random_num2 = random.randrange(0, len(questions_easy) - 1)
        random_num3 = random.randrange(0, len(questions_easy) - 1)
        questions_temp1.append(questions_easy[random_num1])
        questions_temp2.append(questions_medium[random_num2])
        questions_temp3.append(questions_hard[random_num3])
        questions_easy.pop(random_num1)
        questions_medium.pop(random_num2)
        questions_hard.pop(random_num3)

    settings.questions_easy = questions_temp1
    settings.questions_medium = questions_temp2
    settings.questions_hard = questions_temp3


