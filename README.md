# Kiva Loan Recommender

## Jupyter Files
- <b>Kiva Loans - Feature Selection.ipynb</b> Analysis of features which show more similarity in loans by the same lender (ie. features that lenders appear to find important in choosing a loan.)
- <b>Kiva Loans - Find Similar Loans.ipynb</b> Calculation of two types of similarity metric, comparison of results.

## Python Scripts
- <b>find_similar_loans.py</b>Given a username as input, calculate the set of elements found in that user's past loans and return loans with highest similarity.
- <b>update_loan_database.py</b>Periodically ping the Kiva API for the most recent loans and remove loans when they expire.  This is currently run as a cronjob and "database" is a bit of a misnomber since output is stored in a pickled dataframe (<b>data/loan_elements.pickle</b>)

## Flask App
- <b>recommender/</b>Runs locally using "python run.py" in python environment specified by <b>environment.yml</b>
