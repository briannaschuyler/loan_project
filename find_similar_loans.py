import pandas as pd
import pickle
import requests

from country import country_to_continent
from utils import eval_string

path = '/Users/brianna/Dropbox/data_project/loan_project/data/'

def get_user_loan_elements(user):
    url = 'http://api.kivaws.org/v1/lenders/{user}/loans.json'.format(user=user)
    response = requests.get(url)
    lender = eval(response.content.replace('false', 'False').replace('true', 'True'))

    user_loan_elements = set()

    for loan in range(len(lender['loans'])):
        if 'country' in lender['loans'][loan]['location']:
            user_loan_elements.update([lender['loans'][loan]['location']['country']])
            user_loan_elements.update([country_to_continent.get(lender['loans'][loan]['location']['country'])])

        if 'sector'in lender['loans'][loan]:
            user_loan_elements.update([lender['loans'][loan]['sector']])

        if 'tags' in lender['loans'][loan]:
            tags = [k['name'].strip('#') for k in lender['loans'][loan]['tags']]
            user_loan_elements.update(tags)

        if 'themes' in lender['loans'][loan]:
            themes = lender['loans'][loan]['themes']
            user_loan_elements.update(themes)

    return user_loan_elements

def jaccard_distance(x, user_loan_elements):
    intersection = len(set.intersection(x, user_loan_elements))
    union = len(set.union(x, user_loan_elements))
    if union > 0:
        return intersection/float(union)
    else:
        return 0

def get_loans_to_display(loan_similarity, number_displayed):
    number_displayed = 10
    if number_displayed > len(loan_similarity):
        number_displayed = len(loan_similarity)

    loans_to_display = []
    for i in range(number_displayed):
        loans_to_display.append(loan_similarity.pop(max(loan_similarity)))

    return loans_to_display

def get_loan_details_from_api(loans_to_display):
    url = 'http://api.kivaws.org/v1/loans/'
    for loan_id in loans_to_display:
        url += '%s,' % loan_id
    url = url[:-1] + '.json'

    # Get the details for the loans from the API
    response = requests.get(url)
    loan = eval(response.content.replace('false', 'False').replace('true', 'True'))
    loan_details = {}

    # Put the details into a dictionary with each loan id as a key
    for n in range(len(loan['loans'])):
        loan_id = loan['loans'][n]['id']
        loan_details[loan_id] = loan['loans'][n]

    # Pick the values of that dictionary to be displayed on the main page
    loan_details_to_display = []
    for loan_id in loans_to_display:
	loan_link = 'https://www.kiva.org/lend/%s' % loan_id
	if loan_details[loan_id]['borrowers'][0]['pictured'] == True:
	    img = loan_details[loan_id]['image']['id']
	    loan_img = 'https://www.kiva.org/img/s400/%s.jpg' % img
	else:
	    loan_img = 'static/kiva.png'
	country = loan_details[loan_id]['location']['country']
	continent = country_to_continent.get(country, 'Unknown')
	text = loan_details[loan_id]['description']['texts']['en']
        loan_details_to_display.append({'loan_id': loan_id,
					'loan_link': loan_link,
					'loan_img': loan_img,
					'borrower_name': loan_details[loan_id]['borrowers'][0]['first_name'],
					'gender': loan_details[loan_id]['borrowers'][0]['gender'],
                                        'country': country,
					'continent': continent,
                                        'sector': loan_details[loan_id]['sector'],
					'text': text
					})
    return loan_details_to_display


def main(user, number_displayed):
    # Get loan elements
    loan_elements = pickle.load( open( "%sloan_elements.pickle" % path, "rb" ) )

    #user = 'brianna9306'
    user_loan_elements = get_user_loan_elements(user)

    # Find the similarity of every loan with the user's loans
    loan_similarity = {jaccard_distance(v['elements'], user_loan_elements): k for k, v in loan_elements.iteritems()}
    # Pick the currently active loans with the highest similarity to display
    loans_to_display = get_loans_to_display(loan_similarity, number_displayed)

    # Find details on the loans to be displayed
    loan_details_to_display = get_loan_details_from_api(loans_to_display)

    return loan_details_to_display
