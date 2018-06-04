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

# get the last index and the list of words for a file
def get_text_list_and_last(file, page):
    with open(file, 'r') as f:
        data_file = json.load(f)

         # look for the correct page
        for p in data_file:
            if p['page'] == int(page):
                text = p['text']
                break
    # make it a list
    text_list = text.split()
    last = len(text_list) - 1

    return text_list, last


# get the surrounding text for the display of text snippets
# p -surround is the number of words aside of the match that is displayed
def get_snippets(positions, file, page, returnstr=False):
    # get the raw text from the data file
    data = data_path() + file.split('.')[0] + '.json'

    text_list, last = get_text_list_and_last(data, page)
    
    # total surrounding words
    surround = 4

    result = ""
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
                if not returnstr:
                    snipp += '|-> '
                else:
                    snipp += '<span> '

            # append the word to the text snippet
            snipp += text_list[i] + " "
            
            # if the index is the position 
            # of the matching word, mark it
            if i == pos:
                if not returnstr:
                    snipp += '<-| '
                else:
                    snipp += '</span>'
            # iterate
            i += 1
            sur += 1
        
        result += '"[...] ' + str(snipp) + ' [...]"<br><br>'
        
         # return resulst as str
        if not returnstr:
            print('\t\t', snipp)
            print('\t\t--------------------------------------\n')
    if returnstr:
        return result
        


# display answers in terminal with nice text snippets
def display_matches(matches, returnstr=False):
    result = ""
    for doc_page in matches:
        title = doc_page.split('_')[0]
        page = doc_page.split('_')[1]
        
        # return resulst as str
        if returnstr:
            result += '<div class="page-result"><br><h3>page: ' + str(page) + '</h3><br><br>'
            result += get_snippets(matches[doc_page], title, page, True) + '</div>'
        else:
            print('\n\t-', title, '- page:', page, '\n')
            get_snippets(matches[doc_page], title, page)

    if returnstr: return result
        

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

# for the browser, ask query
# return string
def qry_2_string(qry, pages=10):
    e, m = search(qry, max_pages=pages)

    if e: 
        result = str(len(e)) + " results being displayed___"
        result += display_matches(e, True)
        return result
        
    if m: 
        result = 'found 0 page results for: ' + qry + '<br><br>maybe you were looking for this...<br><br>___'

        for alt in m:
            alt_dict = m[alt]
            d_l = len(alt_dict)
            
            if d_l != 0: 
                result += "<div><h4>" + str(d_l) + " page results displayed for: " + str(alt) + "</h4></div>"
                result += display_matches(alt_dict, True)

        return result

