from tkinter import *
import random
import time
import sqlite3
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import settings
global my_selection_question
import matplotlib.pyplot as plt



# help 50/50
def help5050(self_question):
    # Παίρνεις μία λίστα question.
    # Επιλέγεις δύο τυχαίες από τις λάθος απαντήσεις και επιστρέφεις την ίδια λίστα με 0 στη θέση αυτών των απαντήσεων
    # ΠΧ. από ('Ερώτηση δυσκολίας: easy σειρά: 5', 'Α', 'Β', 'Γ', 'Δ', 'Β', 'easy')
    # επιστρέφεις ('Ερώτηση δυσκολίας: easy σειρά: 5', 'Α', 'Β', 0, 0, 'Β', 'easy')
    ans=[1,2,3,4]
    question =[]
    for i in self_question:
        question.append(i)
    for i in range(1,5):
        if question[i]==question[5]:
            ans.pop(i-1)
            ans.pop(random.randrange(len(ans)))
            break
    for i in ans:
        question[i] = ""
    return question


# help2 PC propose an answer
def helppc(self_question):
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
    percent_list=[]
    total = 0
    if self_question[6]=="easy":
        adv = 40
    elif self_question[6]=="medium":
        adv = 30
    else:
        adv = 15
    for correct_answer in range(1,5):
        if self_question[correct_answer]==self_question[5]:
            break
    for i in range(4):
        percent_list.append(random.randrange(0, 100))
        if len(self_question[i+1]) == 0:
            percent_list[i] = 0
        total = total + percent_list[i]
    for i in range(4):
        percent_list[i] = round((percent_list[i]*(100-adv))/(total), 2)
    percent_list[correct_answer-1] = percent_list[correct_answer-1] + adv

    plt.title(self_question[0])
    plt.bar(("A","B","C","D"),percent_list)
    plt.show()

def helpchange(self_question):
    # Αλλάζει την ερώτηση με την επόμενη από την ίδια λίστα επιπέδου δυσκολίας
    if self_question[6]=="easy":
        return settings.questions_easy[5]
    elif self_question[6]=="medium":
        return settings.questions_medium[5]
    else:
        return settings.questions_hard[5]




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
    return settings.questions_easy[0]


