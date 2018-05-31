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
from file_manager import index_path, data_path


# given a query, search the index
def search(qry):
    matches = {}
    i_p = index_path() + 'index.json'
    with open(i_p, 'r', errors='ignore') as f:
        index = json.load(f)

        # create terms out of the query
        qry_terms = text_2_terms(qry, position=False)
                
        # search the terms in the index and append 
        # the results to the dictionary
        for t in qry_terms:
            if t in index:
                # for every doc in the index-term
                for doc in index[t]:
                    # if the document doesn't already exists
                    # store it
                    if not doc in matches:
                        matches[doc] = index[t][doc]
    return matches

# get the surrounding text for the display of text snippets
# p -surround is the number of words aside of the match that is displayed
def get_snippets(positions, file, page, surround=4):
    # get the raw text from the data file
    data = data_path() + file.split('.')[0] + '.json'
    with open(data, 'r') as f:
        data_file = json.load(f)
        
        # look for the correct page
        for p in data_file:
            if p['page'] == int(page):
                text = p['text']
                break
    # make it a list
    text_list = text.split()

    # for every position 
    for pos in positions:
        # print the surrounding text
        sur = 0
        snipp = ""
        i = pos - 2
        if i < 0:
            i = 0
        while sur <= surround:
            if i == pos:
                snipp += '-> '
            snipp += text_list[i] + " "
            i += 1
            sur += 1
        print(snipp)
        print('--------------------------------------')


# display answers in terminal with nice text snippets
def display_matches(matches):
    m_num = len(matches)
    if m_num == 0:
        print("query returned 0 results")
    else:
        print(m_num, "results found:")
        for doc_page in matches:
            title = doc_page.split('_')[0]
            page = doc_page.split('_')[1]

            print('\n\t-', title, '- page:', page, '\n')
            get_snippets(matches[doc_page], title, page)

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

        display_matches(m)
