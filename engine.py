"""
the engine receives the parsed query
and returns the all matching documents.

it should also be able to correctly rank the matches.

later some personalization, nob dialing, and filtering will
be implemented
"""

import json
from pprint import pprint
from parser import text_2_terms, cln_string
from file_manager import index_path, data_path

# given a term and an index
# it returns matches
def match(qry, index):
    matches = {}
    if qry in index:
        # for every doc in the index-term
        for doc in index[qry]:
            # if the document doesn't already exists
            # store it
            if not doc in matches:
                matches[doc] = index[qry][doc]
    
    return matches


# given a query, search the index
def search(qry, max_alts=5, max_pages=2):
    matches = {}
    i_p = index_path() + 'index.json'
    with open(i_p, 'r', errors='ignore') as f:
        index = json.load(f)

        # search the terms in the index and append 
        # the results to the dictionary
        cln_q = cln_string(qry)
        
        # matches for the exact query
        e_m = match(cln_q, index)
        exact_matches = {}
        for k in list(e_m.keys())[:max_pages]:
            exact_matches[k] = e_m[k]


        if len(exact_matches) == 0:
            # create terms out of the query
            qry_terms = text_2_terms(qry, position=False)

            # matches for all generated terms
            for t in qry_terms[:max_alts]:

                al_matches = match(t, index)
                for key in list(al_matches.keys())[:max_pages]:
                    matches.setdefault(t, {})
                    matches[t][key] = al_matches[key]


            return None, matches
        

    return exact_matches, None

# get the surrounding text for the display of text snippets
# p -surround is the number of words aside of the match that is displayed
def get_snippets(positions, file, page):
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
    last = len(text_list) - 1
    
    surround = 4

    # for every position 
    for pos in positions:
        # print the surrounding text
        sur = 0
        snipp = ""
        
        # start the index 
        # 2 words before the matching word
        # check if the index is out of range
        if pos <= last - 2:
            # the position is at least third to last
            # index starts 2 positions before the word
            i = pos - 2
            
            # if the index is less than 0 the set to 0
            if i < 0:
                i = 0
        else:
            diff = 5 - (last - pos)
            i = last - diff + 1

        
        while sur <= surround:
            if i > last: break

            # if the index is the position 
            # of the matching word, mark it
            if i == pos:
                snipp += '|-> '

            # append the word to the text snippet
            snipp += text_list[i] + " "
            
            # if the index is the position 
            # of the matching word, mark it
            if i == pos:
                snipp += '<-| '
            
            # iterate
            i += 1
            sur += 1

        print('\t\t', snipp)
        print('\t\t--------------------------------------\n')


# display answers in terminal with nice text snippets
def display_matches(matches):
    for doc_page in matches:
        title = doc_page.split('_')[0]
        page = doc_page.split('_')[1]

        print('\n\t-', title, '- page:', page, '\n')
        get_snippets(matches[doc_page], title, page)
        

# query input loop
def qry_loop():
    while True:
        # wait for input
        qry = input('\n\nsearch: ')

        # exit
        if qry == 'e':
            print('exiting programm')
            break

        # matches
        e, m = search(qry)

        if e: 
            print(len(e), "results being displayed")
            display_matches(e)
        
        if m: 
            print('found 0 page results for', qry, '\nmaybe you were looking for this...\n')

            for alt in m:
                alt_dict = m[alt]
                d_l = len(alt_dict)
                
                if d_l != 0: 
                    print(d_l, "page results displayed for", alt)
                    display_matches(alt_dict)


