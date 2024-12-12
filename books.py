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
    
def get_recommendation(title):
    index = np.where(pivot_table.index == title[0])[0][0]
    sim_score = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)

    return books.iloc[[i[0] for i in sim_score]][['Book-Title', 'Book-Author', 'Image-URL-M']].copy()

@app.route('/search', methods=['post'])
def searchPage():
    # Get User Input
    user_input = request.form.get('user-input')
    
    # Search through book's data
    starts_with = books[books['Book-Title'].str.startswith(user_input, na=False)][:6]
    contains = books[books['Book-Title'].str.contains(user_input, case=False, na=False) & 
                ~books['Book-Title'].str.startswith(user_input, na=False)][:12]

    search_result = pd.concat([starts_with, contains]).drop_duplicates(subset='Book-Title')
    
    if user_input == '' or search_result.empty:
        return render_template('search_result.html',
                                data=['Not Found'])

    elif search_result.iloc[0]['Book-Title'] in pivot_table.index.values:
        recommendations = get_recommendation(search_result.iloc[0]['Book-Title'])
    
    else:
        recommendations = popular_books[popular_books['Avg-Ratings'] > 4].sample(frac=1)
    
    return render_template('search_result.html',
                                book_title=list(search_result['Book-Title'].values),
                                book_author=list(search_result['Book-Author'].values),
                                book_cover=list(search_result['Image-URL-M'].values),
                                recomend_title=list(recommendations['Book-Title'].values),
                                recomend_author=list(recommendations['Book-Author'].values),
                                recomend_cover=list(recommendations['Image-URL-M'].values),
                                )
    
if __name__ == '__main__':
    app.run(debug=True)