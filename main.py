import random
from tkinter import *
from tkinter import messagebox
import pandas

BACKGROUND_COLOR = "#B1DDC6"
words = pandas.read_csv('./data/french_words.csv')
try:
    known_words = pandas.read_csv('./data/known_words.csv')
except FileNotFoundError:
    with open('./data/known_words.csv', mode='w', encoding='utf-8') as file:
        file.write('French,English\n')
    known_words = pandas.read_csv('./data/known_words.csv')


with open('./data/unknown_words.csv', mode='w', encoding='utf-8') as file:
    file.write('French,English\n')


def start():
    global flip_timer
    global french_word
    known_words = pandas.read_csv('./data/known_words.csv')
    ready_button.grid_forget()
    english.grid_forget()
    english_text.grid_forget()
    canvas.create_image(450, 300, image=card_front)
    french_text['text'] = random.choice(words['French'].tolist())
    i = 0
    while french_text['text'] in known_words['French'].tolist():
        french_text['text'] = random.choice(words['French'].tolist())
        i += 1
        if i > 10000:
            messagebox.showinfo(title='Congratulations', message='You learned all the words!')
            window.quit()
            break

    french_word = french_text['text']
    french.grid(column=0, row=1, columnspan=2)
    french_text.grid(column=0, row=2, columnspan=2)
    canvas.grid(column=0, row=0, columnspan=2, rowspan=5)
    wrong_button.grid(column=0, row=5)
    right_button.grid(column=1, row=5)
    flip_timer = window.after(3000, flip_to_english)

def flip_to_english():
    global french_word
    french.grid_forget()
    french_text.grid_forget()
    english_text['text'] = words['English'].tolist()[words['French'].tolist().index(french_word)]
    canvas.create_image(450, 300, image=card_back)
    english.grid(column=0, row=1, columnspan=2)
    english_text.grid(column=0, row=2, columnspan=2)

def right_answer():
    global french_word
    global flip_timer
    window.after_cancel(flip_timer)
    english_text['text'] = words['English'].tolist()[words['French'].tolist().index(french_word)]
    with open('./data/known_words.csv', mode='a', encoding='utf-8') as known_file:
        known_file.write(f"{french_text['text']},{english_text['text']}\n")
    start()

def wrong_answer():
    global french_word
    global flip_timer
    window.after_cancel(flip_timer)
    english_text['text'] = words['English'].tolist()[words['French'].tolist().index(french_word)]
    with open('./data/unknown_words.csv', mode='a', encoding='utf-8') as known_file:
        known_file.write(f"{french_text['text']},{english_text['text']}\n")
    start()


window = Tk()
window.title('French to English Flashcards')
window.config(background=BACKGROUND_COLOR, pady=30, padx=30)
canvas = Canvas()
canvas.config(width=900, height=600, background=BACKGROUND_COLOR, highlightthickness=0)
card_back = PhotoImage(file='./images/card_back.png')
card_front = PhotoImage(file='./images/card_front.png')
right = PhotoImage(file='./images/right.png')
wrong = PhotoImage(file='./images/wrong.png')
french = Label(text='French', font=('Arial', 24, 'italic'), background='white')
french_text = Label(text='', font=('Arial', 36, 'bold'), background='white')
english = Label(text='English', font=('Arial', 24, 'italic'), background='#91c2af', foreground='white')
english_text = Label(text='', font=('Arial', 36, 'bold'), background='#91c2af', foreground='white')
right_button = Button(image=right, highlightthickness=0, command=right_answer)
wrong_button = Button(image=wrong, highlightthickness=0, command=wrong_answer)
ready_button = Button(image=right, highlightthickness=0, command=start)


ready_button.grid(column=0, row=0, columnspan=2, rowspan=5)


window.mainloop()