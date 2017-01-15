from flask import render_template, request
import pickle

import find_similar_loans
from recommender import app

path = '/Users/brianna/Dropbox/data_project/loan_project/data/'

@app.route('/')
@app.route('/index')
def index():
  user = {'nickname': 'Miguel'}
  return render_template("index.html",
                         title = "Kiva Loan Recommender",
                         user = user)


@app.route('/best_loans')
def best_loans():
  #user = 'brianna9306'

  user_name = request.args.get('user_name')
  print(user_name)
  number_displayed = 10
  best_loans= find_similar_loans.main(user_name, number_displayed)
  # Display the most similar loans, from best to worst
  return render_template("best_loans.html", best_loans=best_loans)
