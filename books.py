from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

popular_books = pickle.load(open('./result/popularity_based.pkl', 'rb'))
pivot_table = pickle.load(open('./result/pt.pkl', 'rb'))
books = pickle.load(open('./result/books.pkl', 'rb'))
similarity_scores = pickle.load(open('./result/sim_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def homePage():
    shuffled_books = popular_books[popular_books['Avg-Ratings'] > 4].sample(frac=1)
    return render_template('search_result.html',
                                book_title=list(shuffled_books['Book-Title'].values),
                                book_author=list(shuffled_books['Book-Author'].values),
                                book_cover=list(shuffled_books['Image-URL-M'].values),
                                )

if __name__ == '__main__':
    app.run(debug=True)