import random
import tkinter as tk

# Define the questions and answers
questions = {
    "What is the capital of France?": {
        "options": ["A. Berlin", "B. Paris", "C. Madrid", "D. Rome"],
        "answer": "B"
    },
    "What is the largest planet in our solar system?": {
        "options": ["A. Jupiter", "B. Saturn", "C. Uranus", "D. Neptune"],
        "answer": "A"
    },
    "What is the highest mountain in the world?": {
        "options": ["A. Mount Everest", "B. Mount Kilimanjaro", "C. Mount Fuji", "D. Mount Denali"],
        "answer": "A"
    },
    "What is the smallest country in the world?": {
        "options": ["A. Vatican City", "B. Monaco", "C. Liechtenstein", "D. San Marino"],
        "answer": "A"
    }
}


# Define the main function for the game
def millionaire_game():
    # Create the GUI window
    root = tk.Tk()
    root.title("Who Wants to be a Millionaire?")
    root.geometry("500x400")

    # Initialize the score and question index
    score = 0
    q_index = 0

    # Define the function to display the next question
    def display_question():
        nonlocal q_index, score

        # If all questions have been answered, display the final score
        if q_index >= len(questions):
            question_label.config(text=f"Game over! Your final score is: {score}")
            return

        # Otherwise, display the next question and options
        question, info = list(questions.items())[q_index]
        question_label.config(text=f"Question {q_index + 1}: {question}")
        for i, option in enumerate(info["options"]):
            option_buttons[i].config(text=option)
        q_index += 1

    # Define the function to check the user's answer
    def check_answer(answer):
        nonlocal score
        info = list(questions.values())[q_index - 1]
        if answer == info["answer"]:
            score += 1
            score_label.config(text=f"Score: {score}")
            result_label.config(text="Correct!")
        else:
            result_label.config(text="Incorrect.")
            display_question()

    # Define the function to display the audience vote
    def display_vote():
        info = list(questions.values())[q_index - 1]
        vote = {}
        for option in info["options"]:
            vote[option] = random.randint(0, 100)
        vote_label.config(text=f"Audience Vote: {vote}")

    # Create the GUI widgets
    question_label = tk.Label(root, text="", font=("Arial", 16))
    question_label.pack(pady=20)

    option_buttons = []
    for i in range(4):
        option_button = tk.Button(root, text="", font=("Arial", 12), width=50,
                                  command=lambda i=i: check_answer(chr(ord("A") + i)))
        option_button.pack(pady=10)
        option_buttons.append(option_button)

    result_label = tk.Label(root, text="", font=("Arial", 14))
    result_label.pack(pady=10)

    score_label = tk.Label(root, text=f"Score: {score}", font=("Arial", 14))
    score_label.pack(pady=10)

    vote_label