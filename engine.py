"""
the engine receives the parsed query
and returns the all matching documents.

it should also be able to correctly rank the matches.

later some personalization, nob dialing, and filtering will
be implemented
"""

import json
from pprint import pprint

# given a query, search the index
def search(qry):
    matches = {}

    with open('sample_index.json', 'r', errors='ignore') as f:
        index = json.load(f)

        # create terms out of the query
         # length of terms
        min_gram = 3
        max_gram = 6

        qry_terms = []

        # for every word in the text, save the position
        for word in qry.split():
            for window in range(min_gram, min(max_gram + 1, len(word) + 1)):
                term = word[:window]

                qry_terms.append(term)
                
        # search the terms in the index and append the results to the dictionary
        for t in qry_terms:
            if t in index:
                for doc in index[t]:
                    if not doc in matches:
                        matches[doc] = index[t][doc]

        pprint(matches)

        



def main_test():
    while True:
        qry = input('search: ')
        if qry == 'e':
            print('exiting programm')
            break
        search(qry)

if __name__ == '__main__':
    main_test()