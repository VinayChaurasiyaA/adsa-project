# import tkinter as tk
# from tkinter import scrolledtext

# def load_dictionary(file_path):
#     with open(file_path, 'r') as file:
#         return [line.strip() for line in file]

# def wagner_fischer(s1, s2):
#     len_s1, len_s2 = len(s1), len(s2)
#     if len_s1 > len_s2:
#         s1, s2 = s2, s1
#         len_s1, len_s2 = len_s2, len_s1

#     current_row = range(len_s1 + 1)
#     for i in range(1, len_s2 + 1):
#         previous_row, current_row = current_row, [i] + [0] * len_s1
#         for j in range(1, len_s1 + 1):
#             add, delete, change = previous_row[j] + 1, current_row[j-1] + 1, previous_row[j-1]
#             if s1[j-1] != s2[i-1]:
#                 change += 1
#             current_row[j] = min(add, delete, change)

#     return current_row[len_s1]

# def spell_check(word, dictionary):
#     suggestions = []

#     for correct_word in dictionary:
#         distance = wagner_fischer(word, correct_word)
#         suggestions.append((correct_word, distance))

#     suggestions.sort(key=lambda x: x[1])
#     return suggestions[:10]

# def on_submit():
#     misspelled_word = entry.get()
#     suggestions = spell_check(misspelled_word, dictionary)
#     print(suggestions)
#     output.delete(1.0, tk.END)  # Clear previous output
#     for word, distance in suggestions:
#         output.insert(tk.END, f"{word} (Distance: {distance})\n")

# # Example Usage
# dictionary = load_dictionary("words.txt")

# # Create the main window
# window = tk.Tk()
# window.title("Spell Checker")

# # Create and place widgets
# label = tk.Label(window, text="Enter a word:")
# label.pack(pady=10)

# entry = tk.Entry(window)
# entry.pack(pady=10)

# submit_button = tk.Button(window, text="Check Spelling", command=on_submit)
# submit_button.pack(pady=10)

# output = scrolledtext.ScrolledText(window, width=40, height=10, wrap=tk.WORD)
# output.pack(pady=10)

# # Start the Tkinter event loop
# window.mainloop()

from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)

# Load dictionary
def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Wagner-Fischer algorithm with dynamic programming
def wagner_fischer(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)
    dp = [[0] * (len_s1 + 1) for _ in range(len_s2 + 1)]

    for i in range(len_s2 + 1):
        dp[i][0] = i
    for j in range(len_s1 + 1):
        dp[0][j] = j

    for i in range(1, len_s2 + 1):
        for j in range(1, len_s1 + 1):
            if s1[j - 1] == s2[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1

    return dp[len_s2][len_s1]

# Spell check function using Wagner-Fischer algorithm
def spell_check(word, dictionary):
    suggestions = []

    for correct_word in dictionary:
        distance = wagner_fischer(word, correct_word)
        suggestions.append((correct_word, distance))

    suggestions.sort(key=lambda x: x[1])
    return suggestions[:10]

dictionary = load_dictionary("words.txt")

# Define functions
def on_submit():
    misspelled_word = request.form['word']
    suggestions = spell_check(misspelled_word, dictionary)
    output_text = ""
    for word, distance in suggestions:
        output_text += f"{word} (Distance: {distance})\n"
    return output_text

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spell_check', methods=['POST'])
def spell_check_handler():
    if request.method == 'POST':
        # Handle the POST request
        output_text = on_submit()
        return output_text

CORS(app)  # Enable CORS for all routes

if __name__ == '__main__':
    app.run(debug=True)
