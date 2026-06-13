import tkinter as tk
from tkinter import scrolledtext
import nltk
import numpy as np
import random
import datetime
import webbrowser

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')

corpus = [
    "hi",
    "how are you",
    "what is your name",
    "Where are you studying.",
    "Where are you from.",
    "How was you life.",
    "When I will see you.",
    "Ok bye"
]

responses = [
    "Hi how can I help you",
    "Iam fine!",
    "My Name is Aishwarya.",
    "Iam Studying Krishna Institutions",  
    "Iam coming from Attur",  
    "My life is Good", 
    "See you soon.",
    "Goodbye!"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)


def chatbot_response(user_input):
    user_input = user_input.lower()

    if "time" in user_input:
        return "Current time is " + datetime.datetime.now().strftime("%H:%M:%S")

    elif "open google" in user_input:
        webbrowser.open("https://www.google.com")
        return "Opening Google..."

    elif "open youtube" in user_input:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube..."

    elif "bye" in user_input:
        root.quit()
        return "Goodbye!"

    user_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, X)
    index = np.argmax(similarity)

    if similarity[0][index] < 0.3:
        return "Sorry, I didn't understand that."

    return responses[index]

def send_message():
    user_message = entry_box.get()
    if user_message.strip() == "":
        return

    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "You: " + user_message + "\n")

    response = chatbot_response(user_message)
    chat_window.insert(tk.END, "Bot: " + response + "\n\n")

    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)
    entry_box.delete(0, tk.END)

root = tk.Tk()
root.title("AI Personal Assistant Chatbot")
root.geometry("500x600")
root.configure(bg="Yellow")

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=("Times new roman", 16))
chat_window.place(x=10, y=10, width=480, height=450)

entry_box = tk.Entry(root, font=("Times new roman", 14))
entry_box.place(x=10, y=470, width=370, height=40)

send_button = tk.Button(root, text="Send", command=send_message, bg="Yellow", fg="Pink")
send_button.place(x=390, y=470, width=100, height=40)

root.mainloop()
