import tkinter as tk
from PIL import Image, ImageTk
import rank
import millioner_button as millioner_button

import settings


class MillionaireGame(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.my_timer = 6000
        self.lives = 3
        self.total_time = 0
        self.total_safe_time = 0
        self.question = millioner_button.my_questions()
        self.counter = 0
        self.title("Who Wants to Be a Millionaire")
        self.geometry('1280x720')
        self.configure(background='black')
        self.main_width = 900
        self.sidebar_width = 1280 - self.main_width
        self.setup_main_screen()
        self.setup_sidebar_screen()
        self.protocol("WM_DELETE_WINDOW", self.close)

    def setup_main_screen(self):
        self.main_frame = tk.Frame(self, bg="gray")
        self.main_frame.pack(side="left", fill="both", expand=True)
        self.setup_main_screen_with_prompt()
        self.setup_answers()

    def setup_main_screen_with_prompt(self):
        self.main_logo_frame = tk.Frame(self.main_frame, bg="black")
        self.main_logo_frame.pack(fill="both", expand=True)
        self.left_frame = tk.Frame(self.main_logo_frame, bg="black")
        self.right_frame = tk.Frame(self.main_logo_frame, bg="red")
        self.left_frame.pack(side="left", fill="both")
        self.right_frame.pack(side="right", fill="both")
        self.left_top_frame = tk.Frame(self.left_frame, bg="black")
        self.left_top_frame.pack(side="top", fill="both")
        img = Image.open('assets/center.png')
        img = img.resize((532, 399))
        self.logo_image = ImageTk.PhotoImage(img)
        self.logo_label = tk.Label(self.right_frame, image=self.logo_image, bg="black", bd=0)
        self.logo_label.pack(fill="both", expand=True)
        self.setup_question_prompt(self.question[0])
        self.set_timer()
        self.my_lives()
        self.stop_game()

    def stop_game(self):
        self.stop_game_button = tk.Button(self.left_top_frame, text="Stop game", fg="white", font=("Arial", 30),
                                          bg="grey", bd=2, command=lambda: self.game_over(self.counter))
        self.stop_game_button.pack(side="left")

    def my_lives(self):
        self.left_bottom_frame = tk.Frame(self.left_frame, bg="black")
        self.left_bottom_frame.pack(side="bottom", fill="both")
        self.live_text_label = tk.Label(self.left_bottom_frame, text="My lives", fg="red", bg="black",
                                        font=('Arial', 30))
        self.live_text_label.pack(side="top")
        img = Image.open('assets/live.png')
        img = img.resize((60, 60))
        self.live_image = ImageTk.PhotoImage(img)
        for i in range(self.lives):
            self.live_label = tk.Label(self.left_bottom_frame, image=self.live_image, bg="black", bd=0)
            self.live_label.pack(side="left")

    def set_timer(self):
        if self.counter == 5 or self.counter == 10 or self.counter == 15:
            self.total_safe_time = self.total_time

        def update():
            self.my_timer = self.my_timer - 1
            self.total_time = self.total_time + 1
            self.my_timer_lbl.configure(text=round(self.my_timer / 100))
            if self.my_timer > 0:
                self.my_timer_lbl.after(10, update)
            else:
                if self.counter < 15:
                    self.game_over(10)
                elif self.counter < 15:
                    self.game_over(5)
                else:
                    self.game_over(0)

        self.my_text_lbl = tk.Label(self.left_top_frame, text="Timer", font=('Arial', 40), bg='black', fg='white')
        self.my_timer_lbl = tk.Label(self.left_top_frame, text="60", font=('Arial', 60), bg='black', fg='white')
        self.my_text_lbl.pack(pady=20)
        self.my_timer_lbl.pack(pady=20)
        self.after(1, update)

    def setup_answers(self):
        self.main_questions_frame = tk.Frame(self.main_frame, bg="yellow")
        self.main_questions_frame.pack(fill="both", expand=True)
        self.setup_answer(1)
        self.setup_answer(2)
        self.setup_answer(3)
        self.setup_answer(4)

    def screen_reset(self):
        self.main_frame.destroy()
        self.setup_main_screen()
        self.prizes_frame.destroy()
        self.setup_sidebar_prizes()

    def correct_answer(self):
        if self.counter < 5:
            self.question = settings.questions_easy[self.counter]
        elif self.counter < 10:
            self.question = settings.questions_medium[self.counter - 5]
        elif self.counter < 15:
            self.question = settings.questions_hard[self.counter - 10]
        else:
            self.game_over(self.counter)
        self.screen_reset()
        self.my_timer = 6000

    def game_over(self, my_counter):
        prizes = [0, 25, 50, 100, 200, 300, 500, 1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
        settings.my_window = "βαθμολογίας "
        self.destroy()
        print(self.total_safe_time)
        if my_counter!=5 or my_counter!=10:
            self.total_safe_time = self.total_time


        if self.total_safe_time != 0 and my_counter!=0:
            my_score = round(prizes[my_counter] / (self.total_safe_time / 100))
            rank.new_rank(prizes[my_counter], round(self.total_safe_time / 100),
                          round(self.total_safe_time / my_counter) / 100, my_score)
        else:
            settings.open_window = 0

    def my_answer(self, answer):
        if answer == self.question[5]:
            self.counter = self.counter + 1
            self.correct_answer()
        else:
            self.lives = self.lives - 1
            self.left_bottom_frame.destroy()
            self.my_lives()
            if self.lives == 0:
                if self.counter < 15:
                    self.game_over(10)
                elif self.counter < 15:
                    self.game_over(5)
                else:
                    self.game_over(0)

    def setup_answer(self, index):
        self.dada = tk.Frame(self.main_questions_frame, bg="green")
        self.button = tk.Button(self.main_questions_frame, text=self.question[index], bg="blue", fg="white",
                                font=("Helvetica", 14), command=lambda: self.my_answer(self.question[index]))
        self.button.pack(fill="both", expand=True)

    def setup_question_prompt(self, question):
        label = tk.Label(self.main_frame, text=question, bg="red", fg="white", font=("Helvetica", 14))
        label.pack(fill="both", expand=True)

    def setup_sidebar_screen(self):
        self.sidebar_frame = tk.Frame(self, bg="red", width=self.sidebar_width)
        self.sidebar_frame.pack(side="right", fill="both")
        self.sidebar_frame.pack_propagate(0)
        self.setup_sidebar_options()
        self.setup_sidebar_prizes()

    def setup_sidebar_options(self):
        self.options_frame = tk.Frame(self.sidebar_frame, bg="red")
        self.options_frame.pack(side="top", fill="both", expand=True)
        self.setup_5050_button()
        self.setup_ata_button()
        self.setup_paf_button()

    def help5050(self):
        img = Image.open('assets/Classic5050X.png')
        img = img.resize((62, 48))
        self.button_5050_image = ImageTk.PhotoImage(img)
        self.button_5050.config(image=self.button_5050_image, state=tk.DISABLED)
        self.question = millioner_button.help5050(self.question)
        self.screen_reset()

    def setup_5050_button(self):
        self.button_5050_frame = tk.Frame(self.options_frame, bg="green")
        self.button_5050_frame.pack(side="left", fill="both", expand=True)
        img = Image.open('assets/Classic5050.png')
        img = img.resize((62, 48))
        self.button_5050_image = ImageTk.PhotoImage(img)
        self.button_5050 = tk.Button(self.button_5050_frame, bg="red", image=self.button_5050_image, bd=0,
                                     command=self.help5050)
        self.button_5050.pack(fill="both", expand=True)

    def helppc(self):
        img = Image.open('assets/ClassicATAx.png')
        img = img.resize((62, 48))
        self.button_ata_image = ImageTk.PhotoImage(img)
        self.button_ata.config(image=self.button_ata_image, state=tk.DISABLED)
        millioner_button.helppc(self.question)

    def setup_ata_button(self):
        self.button_ata_frame = tk.Frame(self.options_frame, bg="yellow")
        self.button_ata_frame.pack(side="left", fill="both", expand=True)
        img = Image.open('assets/ClassicATA.png')
        img = img.resize((62, 48))
        self.button_ata_image = ImageTk.PhotoImage(img)
        self.button_ata = tk.Button(self.button_ata_frame, bg="yellow", image=self.button_ata_image, bd=0,
                                    command=self.helppc)
        self.button_ata.pack(fill="both", expand=True)

    def helpchange(self):
        img = Image.open('assets/ClassicREPX.png')
        img = img.resize((62, 48))
        self.button_paf_image = ImageTk.PhotoImage(img)
        self.button_paf.config(image=self.button_paf_image, state=tk.DISABLED)
        self.question = millioner_button.helpchange(self.question)
        self.screen_reset()

    def setup_paf_button(self):
        self.button_paf_frame = tk.Frame(self.options_frame, bg="purple")
        self.button_paf_frame.pack(side="left", fill="both", expand=True)
        img = Image.open('assets/ClassicREP.png')
        img = img.resize((62, 48))
        self.button_paf_image = ImageTk.PhotoImage(img)
        self.button_paf = tk.Button(self.button_paf_frame, bg="purple", image=self.button_paf_image, bd=0,
                                    command=self.helpchange)
        self.button_paf.pack(fill="both", expand=True)

    def setup_sidebar_prizes(self):
        self.prizes_frame = tk.Frame(self.sidebar_frame, bg="blue")
        self.prizes_frame.pack(side="bottom", fill="both", expand=True)
        self.prize_labels = []
        prizes = ['1,000,000 €', '500,000 €', '250,000 €', '100,000 €',
                  '50,000 €', '25,000 €', '10,000 €', '5,000 €', '1,000 €',
                  '500 €', '300 €', '200 €', '100 €', '50 €', '25 €']
        my_counter = len(prizes)
        for prize in prizes:
            if my_counter == self.counter:
                label = tk.Label(self.prizes_frame, text=prize, bg="yellow3", fg="white", font=("Helvetica", 14))
            else:
                if my_counter == 5 or my_counter == 10:
                    label = tk.Label(self.prizes_frame, text=prize, bg="green4", fg="white", font=("Helvetica", 14))
                else:
                    label = tk.Label(self.prizes_frame, text=prize, bg="blue", fg="white", font=("Helvetica", 14))
            label.pack(fill="both", expand=True)
            self.prize_labels.append(label)
            my_counter = my_counter - 1

    def start(self):
        self.mainloop()

    def close(self):
        settings.open_window = 0
        self.destroy()


def start_game(root):
    app = MillionaireGame(root)
    app.start()
