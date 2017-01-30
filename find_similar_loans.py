import pandas as pd
import pickle
import random
import requests

import colors as pie_chart_colors
from config import PATH
from country import country_to_continent
from utils import eval_string

###########################################################################
# Get all of the elements of the specified user's loans
###########################################################################

# To speed up computing time, if a user has had more than 50 loans only take
# the 50 most recent
max_loans = 50

def add_element(category, element):
    if element not in category:
        category[element] = 1
    else:
        category[element] += 1

    return category

def transform_for_pie_charts(user_loan_elements):
    # Put this information in the way that highcharts pie charts wants it (ie. for each category
    # make a list of dicts with keys = (name, y, color)
    categories = {'user_countries': pie_chart_colors.oranges,
                  'user_continents': pie_chart_colors.blues,
                  'user_sectors': pie_chart_colors.reds,
                  'user_tags': pie_chart_colors.greens,
                  'user_themes': pie_chart_colors.purples}
    user_loan_elements_transformed = {}
    for category in categories:
        colors = categories[category]
        user_loan_elements_transformed[category] = []
        i = 0
        for element in user_loan_elements[category]:
            user_loan_elements_transformed[category].append({'name': element.replace(' ', '<br>').replace('_', '<br>'),
                                                             'y': user_loan_elements[category][element],
                                                             'color': colors[i % len(colors)]})
    return user_loan_elements_transformed

def get_user_loan_elements(user):
    url = 'http://api.kivaws.org/v1/lenders/{user}/loans.json'.format(user=user)
    response = requests.get(url)
    lender = eval(response.content.replace('false', 'False').replace('true', 'True'))

    # To speed up computing time, if a user has a ton of loans only use the 10 most recent.
    if len(lender['loans']) > max_loans:
        lender['loans'] = lender['loans'][-max_loans:]

    # Make dictionaries of each of these important categories of the user's loans,
    # where the key is the category (ex. "Woman Owned Biz") and the value is the number
    # of times it's appeared in this user's loans
    countries, continents, sectors, tags, themes = {}, {}, {}, {}, {}

    for loan in range(len(lender['loans'])):
        if 'country' in lender['loans'][loan]['location']:
            country = lender['loans'][loan]['location']['country']
            countries = add_element(countries, country)
            continent = country_to_continent.get(country, 'Unknown')
            continents = add_element(continents, continent)

        if 'sector'in lender['loans'][loan]:
            sector = lender['loans'][loan]['sector']
            sectors = add_element(sectors, sector)

        if 'tags' in lender['loans'][loan]:
            loan_tags = [k['name'].strip('#') for k in lender['loans'][loan]['tags']]
            for t in loan_tags:
                tags = add_element(tags, t)

        if 'themes' in lender['loans'][loan]:
            loan_themes = lender['loans'][loan]['themes']
            for th in loan_themes:
                themes = add_element(themes, th)

        user_loan_elements = {'user_countries': countries,
                              'user_continents': continents,
                              'user_sectors': sectors,
                              'user_tags': tags,
                              'user_themes': themes}

    return user_loan_elements

def get_user_loan_elements_and_counts(user_loan_elements):
    # Combine elements from each category into a single set to calculate similarity
    user_loan_elements_set = {}
    for category in user_loan_elements:
        for element in user_loan_elements[category]:
            user_loan_elements_set.update(user_loan_elements[category])
    return user_loan_elements_set

def get_user_loan_elements_categories_only(user_loan_elements):
    # Combine elements from each category into a single set to calculate similarity
    user_loan_elements_set = set()
    for category in user_loan_elements:
        user_loan_elements_set.update(user_loan_elements[category])
    return user_loan_elements_set

###########################################################################
# Jaccard distance - intersection of two sets over the union of the sets
###########################################################################

def jaccard_distance(x, user_loan_elements):
    user_loan_elements_set = get_user_loan_elements_categories_only(user_loan_elements)
    intersection = len(set.intersection(x, user_loan_elements_set))
    union = len(set.union(x, user_loan_elements_set))
    if union > 0:
        return intersection/float(union)
    else:
        return 0

###########################################################################
# Dot Product Similarity - similarity weighted by instance of each category
###########################################################################

def get_max_instance(user_loan_elements, category):
    # Get the maximm number of instances of a particular category (country, continent, sector)
    instances = {v: k for k,v in user_loan_elements[category].iteritems()}
    return max(instances)

def get_sum_of_instances(user_loan_elements, category):
    # Get the maximm number of instances of a particular category (country, continent, sector)
    total_instances = 0
    for k in user_loan_elements[category]:
        total_instances += user_loan_elements[category][k]
    return total_instances

def max_dp_similarity(user_loan_elements):
    # The maximum "similarity score" would be:
    #    - a match with the most common country, continent, and sector
    #    - all tags and themes shared
    dp_max = 0
    for category in ['user_countries', 'user_continents', 'user_sectors']:
        dp_max += get_max_instance(user_loan_elements, category)
    for category in ['user_tags', 'user_themes']:
        dp_max += get_sum_of_instances(user_loan_elements, category)
    return dp_max

def dp_similarity(candidate_loan_elements, user_loan_elements):
    user_loan_elements_set = get_user_loan_elements_and_counts(user_loan_elements)
    candidate_loan_elements = list(candidate_loan_elements)

    dot_product = sum([user_loan_elements_set.get(k, 0) for k in candidate_loan_elements])

    # Normalize by the maximum dot product of the most ideal loan (which is not the same as sharing
    # every element since a loan can in theory share all tags and themes but can only have one
    # country, continent, and sector
    return dot_product * 1.0 / max_dp_similarity(user_loan_elements)

###########################################################################
# Find and display loans
###########################################################################

def get_loans_to_display(loan_similarity, number_displayed):
    # Return a list of tuples (loand_id, similarity_score) sorted by similarity
    if number_displayed > len(loan_similarity):
        number_displayed = len(loan_similarity)

    loans_to_display = []
    for i in range(number_displayed):
        next_max_sim = max(loan_similarity)
        loans_to_display.append((loan_similarity[next_max_sim], next_max_sim))
        loan_similarity.pop(max(loan_similarity))

    return loans_to_display

def get_percent(x):
    return str('%s%%' % int(round(x * 100)))

def to_unicode(x):
    return x.decode('unicode-escape')

def get_loan_details_from_api(loans_to_display):
    url = 'http://api.kivaws.org/v1/loans/'
    for loan_sim in loans_to_display:
        loan_id = loan_sim[0]
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
    for loan_sim in loans_to_display:
        loan_id = loan_sim[0]

        # Image and link to loan
        loan_link = 'https://www.kiva.org/lend/%s' % loan_id
        if loan_details[loan_id]['borrowers'][0]['pictured'] == True:
            img = loan_details[loan_id]['image']['id']
            loan_img = 'https://www.kiva.org/img/s400/%s.jpg' % img
        else:
            loan_img = 'static/kiva.png'

        # Borrower details
        borrower_name = to_unicode(loan_details[loan_id]['borrowers'][0]['first_name'])
        if len(loan_details[loan_id]['borrowers']) > 1:
            gender = 'Group'
        else:
            gender = loan_details[loan_id]['borrowers'][0]['gender']

        # Loan details
        country = to_unicode(loan_details[loan_id]['location']['country'])
        continent = to_unicode(country_to_continent.get(country, 'Unknown'))
        sector = to_unicode(loan_details[loan_id]['sector'])
        text = to_unicode(loan_details[loan_id]['description']['texts']['en']).\
                 replace('<br \/>', '\n\n')

        # Send details to website to display
        loan_details_to_display.append({'loan_id': loan_id,
                                        'similarity': get_percent(loan_sim[1]),
                                        'loan_link': loan_link,
                                        'loan_img': loan_img,
                                        'borrower_name': borrower_name,
                                        'gender': gender,
                                        'country': country,
                                        'continent': continent,
                                        'sector': sector,
                                        'text': text
                                        })
    return loan_details_to_display


def main(user, number_displayed):
    # Get loan elements
    loan_elements = pickle.load( open( "%sloan_elements.pickle" % PATH, "rb" ) )

    #user = 'brianna9306'
    user_loan_elements = get_user_loan_elements(user)

    # Find the similarity of every loan with the user's loans
    #similarity_scores = {k: jaccard_distance(v['elements'], user_loan_elements) for k, v in loan_elements.iteritems()}
    similarity_scores = {k: dp_similarity(v['elements'], user_loan_elements) for k, v in loan_elements.iteritems()}

    # Get list of tuples (loan_id, similarity_score) sorted by similarity score
    loans_to_display = sorted(similarity_scores.items(), key=lambda tup: tup[1], reverse=True)
    loans_to_display = loans_to_display[:number_displayed]

    # Find details on the loans to be displayed
    loan_details_to_display = get_loan_details_from_api(loans_to_display)

    return transform_for_pie_charts(user_loan_elements), loan_details_to_display
