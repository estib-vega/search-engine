"""
the engine receives the parsed query
and returns the all matching documents.

it should also be able to correctly rank the matches.

later some personalization, nob dialing, and filtering will
be implemented
"""

import json
from pprint import pprint
from parser import text_2_terms

# given a query, search the index
def search(qry):
    matches = {}

    with open('sample_index.json', 'r', errors='ignore') as f:
        index = json.load(f)

        # create terms out of the query
        qry_terms = text_2_terms(qry, position=False)
                
        # search the terms in the index and append the results to the dictionary
        for t in qry_terms:
            if t in index:
                for doc in index[t]:
                    if not doc in matches:
                        matches[doc] = index[t][doc]

    return matches


# query input loop
def qry_loop():
    while True:
        # wait for input
        qry = input('search: ')

        # exit
        if qry == 'e':
            print('exiting programm')
            break
            
        # matches
        m = search(qry)

        pprint(m)



def main_test():
    qry_loop()

if __name__ == '__main__':
    main_test()