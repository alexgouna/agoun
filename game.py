import tkinter as tk
from PIL import Image, ImageTk

import millioner_button
import settings

# "question" is a list with the attributes of the current question
question =[]

class MillionaireGame(tk.Toplevel):
    def __init__(self, master):
        # super().__init__()
        # set 5 random question from DB for each lvl
        question = millioner_button.my_questions()
        tk.Toplevel.__init__(self, master)
        self.title("Who Wants to Be a Millionaire")
        self.geometry('1280x720')
        self.configure(background='black')
        # this doesn't update sidebar width for now
        self.main_width = 900
        self.sidebar_width = 1280 - self.main_width
        self.setup_main_screen()
        self.setup_sidebar_screen()
        # bind close
        self.protocol("WM_DELETE_WINDOW", self.close)

    def setup_main_screen(self):
        self.main_frame = tk.Frame(self, bg="gray")
        self.main_frame.pack(side="left", fill="both", expand=True)
        self.setup_main_screen_with_prompt()
        self.setup_answers()


    def setup_main_screen_with_prompt(self):
        self.main_logo_frame = tk.Frame(self.main_frame, bg="purple")
        self.main_logo_frame.pack(fill="both", expand=True)
        img = Image.open('assets/center.png')
        img = img.resize((250, 250))
        self.logo_image = ImageTk.PhotoImage(img)
        self.logo_button = tk.Button(self.main_logo_frame, image=self.logo_image, bg="black", bd=0)
        self.logo_button.pack(fill="both", expand=True)
        self.setup_question_prompt("question")

    def setup_answers(self):
        self.main_questions_frame = tk.Frame(self.main_frame, bg="yellow")
        self.main_questions_frame.pack(fill="both", expand=True)
        # TODO: Add questions widget
        self.setup_answer(1, "answer 1")
        self.setup_answer(2, "answer 2")
        self.setup_answer(3, "answer 3")
        self.setup_answer(4, "answer 4")

    def setup_answer(self, index, answer_label):
        self.dada = tk.Frame(self.main_questions_frame, bg="green")
        # TODO determine side
        label = tk.Label(self.main_questions_frame, text=answer_label, bg="blue",
                         fg="white", font=("Helvetica", 14))
        label.pack(fill="both", expand=True)

    def setup_question_prompt(self, question):
        label = tk.Label(self.main_frame, text=question, bg="red",
                         fg="white", font=("Helvetica", 14))
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


    def setup_5050_button(self):
        self.button_5050_frame = tk.Frame(self.options_frame, bg="green")
        self.button_5050_frame.pack(side="left", fill="both", expand=True)
        img = Image.open('assets/Classic5050.png')
        img = img.resize((62, 48))
        self.button_5050_image = ImageTk.PhotoImage(img)
        self.button_5050 = tk.Button(
            self.button_5050_frame, bg="red", image=self.button_5050_image, bd=0)
        self.button_5050.pack(fill="both", expand=True)

    def setup_ata_button(self):
        self.button_ata_frame = tk.Frame(self.options_frame, bg="yellow")
        self.button_ata_frame.pack(side="left", fill="both", expand=True)
        img = Image.open('assets/ClassicATA.png')
        img = img.resize((62, 48))
        self.button_ata_image = ImageTk.PhotoImage(img)
        self.button_ata = tk.Button(self.button_ata_frame, bg="yellow",
                                    image=self.button_ata_image, bd=0)
        self.button_ata.pack(fill="both", expand=True)

    def setup_paf_button(self):
        self.button_paf_frame = tk.Frame(self.options_frame, bg="purple")
        self.button_paf_frame.pack(side="left", fill="both", expand=True)
        img = Image.open('assets/ClassicPAF.png')
        img = img.resize((62, 48))
        self.button_paf_image = ImageTk.PhotoImage(img)
        self.button_paf = tk.Button(self.button_paf_frame, bg="purple",
                                    image=self.button_paf_image, bd=0)
        self.button_paf.pack(fill="both", expand=True)

    def setup_sidebar_prizes(self):
        self.prizes_frame = tk.Frame(self.sidebar_frame, bg="blue")
        self.prizes_frame.pack(side="bottom", fill="both", expand=True)

        self.prize_labels = []
        prizes = ['$1,000,000', '$500,000', '$250,000', '$100,000', '$50,000',
                  '$25,000', '$10,000', '$5,000', '$1,000', '$500', '$300',
                  '$200', '$100', '$50', '$0']
        for prize in prizes:
            label = tk.Label(self.prizes_frame, text=prize, bg="blue",
                             fg="white", font=("Helvetica", 14))
            label.pack(fill="both", expand=True)
            self.prize_labels.append(label)

    def start(self):
        """
        Start the game.
        """
        self.mainloop()

    def close(self):
        print('close')
        settings.counter_game = 0
        self.destroy()


def start_game(root):
    app = MillionaireGame(root)
    app.start()
