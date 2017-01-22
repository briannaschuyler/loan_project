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
  user = {'nickname': 'Miguel'}
  return render_template("index.html",
                         title = "Kiva Loan Recommender",
                         user = user)

def redirect_message():
  username_DNE = "<b>This username does not exist in the Kiva database or is not public!</b> <br><br>"
  return username_DNE + find_username_message()

def find_username_message():
  return '''
To find your username (and make your account public), go to <a href="https://www.kiva.org/settings/account"
target="_blank">Kiva Account Settings</a>.<br><br>

(Make sure you're signed in.)<br><br>
Your username is listed in the "My Lender Profile" section.<br>

<img src="static/kiva_username.png" alt="Kiva Username Location"><br><br>

At the bottom of the page, click "Make my page and loans public."<br><br>

More details can be found
<a href="http://pages.kiva.org/kivablog/2013/08/08/your-kiva-account-settings-just-got-that-much-simpler">
here</a>.<br><br>

Once you're done, return to the <a href="index">Kiva Loan Recommender</a> to find the loans you'll
likely be interested in!
'''

@app.route('/find_username')
def find_username():
  return find_username_message()

@app.route('/best_loans')
def best_loans():
  username = str(request.args.get('username'))
  logging.info('Username: %s' % username)
  number_displayed = 15
  try:
    user_loans, best_loans = find_similar_loans.main(username, number_displayed)
  except:
    return redirect_message()

  # If username is in the system, return elements of user's previous loans and a list of similar
  # loans, from best to worst
  for element in user_loans:
    user_loans[element] = set_to_string(user_loans[element])

  return render_template("best_loans.html", username=json.dumps(username), user_loans=user_loans, best_loans=best_loans)

@app.route('/countries_pie')
def countries_pie():
    #username = str(request.args.get('username'))
    countries_data = [
    { 'name': 'Microsoft Internet Explorer', 'y': 6, 'color': 'blue' },
    { 'name': 'Chrome', 'y': 10 , 'color': 'blue' },
    { 'name': 'Firefox', 'y': 1 , 'color': 'blue' }
    ]

    return json.dumps([countries_data, 'Countries AYAYAY', username])

