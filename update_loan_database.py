from datetime import datetime
import logging
import pandas as pd
import pickle
from pprint import pprint
import requests
import time

from config import PATH
from country import country_to_continent
from utils import eval_string, get_date

logging.basicConfig(filename='{}loan_update.log'.format(PATH),
                    format='%(asctime)-15s %(message)s', level=logging.INFO)

MAX_LOANS = 20000

# Extract a set of elements that we care about
def get_loan_elements(k):
  loan_elements = set([k['location']['country'],
                       country_to_continent.get(k['location']['country'], 'Unknown'),
                       k['sector']])

  # Add tags and themes if they exist
  if 'tags' in k:
    loan_elements.update([j['name'].strip('#') for j in k['tags']])
  if 'themes' in k:
    loan_elements.update(k['themes'])

  return loan_elements

def remove_funded_loans(loan_elements):
  # Make a list of the current loans in loan elements and grab from the API to find out which ones are
  # funded to remove them from the pile.
  current_loans = list(loan_elements.keys())

  for i in range(0, len(current_loans) + 1, 50):

    # Construct the url to get details for 50 loans from the API
    url = 'http://api.kivaws.org/v1/loans/'
    for loan_id in current_loans[i: i + 50]:
      url += '%s,' % loan_id
    url = url[:-1] + '.json'

    # Get the details for the 50 loans
    response = requests.get(url)
    loan = eval(response.content.decode('utf8').replace('false', 'False').replace('true', 'True'))

    # Loop over the 50 loans and if any are funded, pop them out of the loan_elements_dictionary
    for n in range(len(loan['loans'])):
      if loan['loans'][n]['status'] == 'funded':
        if loan['loans'][n]['id'] in loan_elements:
          loan_elements.pop(loan['loans'][n]['id'])

    # Sleep for 1 sec to not overload the API
    time.sleep(1)

  return loan_elements


def main():
  # Get the 500 most recent loans (the max I can get with this API call) with "fundraising" status
  logging.info('Accessing 500 most recent loans')
  url = 'http://api.kivaws.org/v1/loans/search.json?status=fundraising&per_page=500'
  response = requests.get(url)
  newest_loans = eval(response.content.decode('utf8').replace('false', 'False').replace('true', 'True'))['loans']

  # Get a list of important elements for each loan
  loan_details = [get_loan_elements(k) for k in newest_loans]

  # Load the most recent update of the element sets for currently available loans
  try:
    loan_elements = pickle.load( open( "%sloan_elements.pickle" % PATH, "rb" ) )
    logging.info('%s loans before updating' % len(loan_elements))
  except:
    logging.warning('Error loading file, creating an empty dict')
    loan_elements = {}

  # To keep the size of this object reasonable (for speed and storage purposes,
  # limit the number of loans.
  if len(loan_elements) < MAX_LOANS:
    # Add the most recent loans and their elements to the dictionary
    for i in range(len(newest_loans)):
      loan_elements[newest_loans[i]['id']] = {'elements': loan_details[i],
                                              'expired_at': get_date(newest_loans[i]['planned_expiration_date']),
                                              'updated_at': datetime.today()}
  else:
    logging.info('Number of loans is %s, which exceeds max of %s.  No new loans have been added.' %
            (len(loan_elements), MAX_LOANS))

  # Remove all expired loans
  num_removed_expired = 0
  loan_ids = loan_elements.copy().keys()
  for loan_id in loan_ids:
    if loan_elements[loan_id]['expired_at'] < datetime.today().date():
      loan_elements.pop(loan_id)
      num_removed_expired +=1
  logging.info('%s loans removed due to expiration' % num_removed_expired)

  # Remove all funded loans
  num_loans = len(loan_elements)
  loan_elements_unfunded = remove_funded_loans(loan_elements)
  num_removed_funded = num_loans - len(loan_elements_unfunded)

  # Save the updated dictionary with elements of currently available loans.
  logging.info('%s loans removed due to being funded' % num_removed_funded)
  logging.info('%s loans in current record' % len(loan_elements_unfunded))
  pickle.dump(loan_elements_unfunded, open( "%sloan_elements.pickle" % PATH, "wb" ))

if __name__ == "__main__":
  main()
