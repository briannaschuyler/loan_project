from flask import render_template, request
import pickle

import find_similar_loans
from recommender import app

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
Your username is listed in the "My Lender Profile" section.

<img src="static/kiva_username.png" alt="Kiva Username Location"><br><br>

At the bottom of the page, click "Make my page and loans public."<br><br>

More details can be found <a href="http://pages.kiva.org/kivablog/2013/08/08/your-kiva-account-settings-just-got-that-much-simpler">
here</a>.<br><br>

Once you're done, return to the <a href="index">Kiva Loan Recommender</a> to find the loans you'll likely be interested in!
'''

@app.route('/find_username')
def find_username():
  return find_username_message()

def set_to_string(input_set):
  output = ''
  for s in input_set:
    if s is not None:
      output = output + s + ', '
  return output[:-2]

@app.route('/best_loans')
def best_loans():
  username = str(request.args.get('username'))
  number_displayed = 10
  print('Username %s' % username)
  try:
    user_loans, best_loans = find_similar_loans.main(username, number_displayed)
  except:
    return redirect_message()

  # If username is in the system, return elements of user's previous loans and a list of similar
  # loans, from best to worst
  for element in user_loans:
    user_loans[element] = set_to_string(user_loans[element])

  return render_template("best_loans.html", user_loans=user_loans, best_loans=best_loans)
