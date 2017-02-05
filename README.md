# Kiva Loan Recommender

This repo contains the code for a <a href="http://52.53.233.9:5000"> Kiva Loan Recommender</a> based on user loan history.  

## Jupyter notebooks:
- <b>Kiva Loans - Feature Selection.ipynb</b>: Initial analyses to find features that appeared to be more similar in loans given by a single user (ie. features that users showed a preference for).
- <b>Kiva Loans - Find Similar Loans.ipynb</b>: Calculations of two types of similarity score for comparison.

## Python scripts:
- <b>find_similar_loans.py</b>: Given a username as input, outputs loan details of the most similar loans for this user.
- <b>update_loan_database.py</b>: Periodically update the database with new loans and remove expired loans.  This is run as a cronjob once daily.  Calling it a "database" is a bit of a misnomer since it's stored as a pickled dictionary (data/loan_elements.pickle).

## Flask app:
- <b>recommender/</b>: Flask app that runs the website <a href="http://www.kivaloans4.me/">www.kivaloans4.me/</a>, using the environment detailed in <b>environment.yml</b>.
