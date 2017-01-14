from datetime import datetime
import logging
import pandas as pd
import pickle
from pprint import pprint
import requests

from country import country_to_continent
from utils import eval_string, get_date

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

path = '/Users/brianna/Dropbox/data_project/loan_project/data/'

# Extract a set of elements that we care about
def get_loan_elements(k):
    loan_elements = set([k['location']['country'],
                         country_to_continent.get(k['location']['country'], 'Unknown'),
                         k['sector']])

    # Add tags and themes if they exist
    if 'tags' in k:
        loan_elements.update([j['name'].strip('#') for j in newest_loans[0]['tags']])
    if 'themes' in k:
        loan_elements.update(k['themes'])

    return loan_elements

# Get the 500 most recent loans (the max I can get with this API call) with "fundraising" status
url = 'http://api.kivaws.org/v1/loans/search.json?status=fundraising&per_page=500'
response = requests.get(url)
newest_loans = eval(response.content.replace('false', 'False').replace('true', 'True'))['loans']

# Get a list of important elements for each loan
loan_details = [get_loan_elements(k) for k in newest_loans]

# Load the most recent update of the element sets for currently available loans
try:
    loan_elements = pickle.load( open( "%sloan_elements.pickle" % path, "rb" ) )
    logging.info('%s loans before updating' % len(loan_elements))
except:
    logging.warning('Error loading file, creating an empty dict')
    loan_elements = {}

# Add the most recent loans and their elements to the dictionary
for i in range(len(newest_loans)):
    loan_elements[newest_loans[i]['id']] = {'elements': loan_details[i],
                                            'expired_at': get_date(newest_loans[i]['planned_expiration_date'])}

# Remove all expired loans
num_removed = 0
for loan_id in loan_elements.keys():
    if loan_elements[loan_id]['expired_at'] < datetime.today().date():
        loan_elements.pop(loan_id)
        num_removed +=1

# Save the updated dictionary with elements of currently available loans.
logging.info('%s loans removed' % num_removed)
logging.info('%s loans in current record' % len(loan_elements))
pickle.dump(loan_elements, open( "%sloan_elements.pickle" % path, "wb" ))
