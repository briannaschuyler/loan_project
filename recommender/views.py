from flask import render_template, request
import json
import logging
import pickle

import find_similar_loans
from recommender import app
from utils import set_to_string

logging.basicConfig(filename='usage.log', format='%(asctime)s %(message)s', level=logging.INFO)

@app.route('/')
@app.route('/index')
def index():
  return render_template("index.html",
                         title = "Kiva Loan Recommender")

@app.route('/get_best_loans/<username>')
def get_best_loans(username):
  logging.info('Username: %s' % username)
  number_displayed = 15
  try:
    user_loans, best_loans = find_similar_loans.main(username, number_displayed)
  except:
    return json.dumps([])

  return json.dumps([user_loans, best_loans])

