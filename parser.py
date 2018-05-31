"""
the string parser takes the normal string of text
(query or searchable)
and creates terms or n-grams

this terms are stored, if they come from the searchable data,
in files that then can be easily searched by the engine

if they come from a query, only the terms are returned

"""

import json, string, re
from file_manager import get_complete_path, index_path

# unnecesary words
STOP_WORDS = set([
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by',
        'for', 'if', 'in', 'into', 'is', 'it',
        'no', 'not', 'of', 'on', 'or', 's', 'such',
        't', 'that', 'the', 'their', 'then', 'there', 'these',
        'they', 'this', 'to', 'was', 'will', 'with'
    ])

# retrun clean string
def cln_string(stri):
    w = re.sub('[' + string.punctuation + ']', '', stri).lower().rstrip()    
    return w

# make terms from text
def text_2_terms(text, min_gram=1, max_gram=6, position=True):
    if not position:
        terms = []
        # return only the terms without 
        # position (used for queries)
        for word in text.split():
            if not word in STOP_WORDS:
                for window in range(min_gram, min(max_gram + 1, len(word) + 1)):
                    w = cln_string(word)
                    term = w[:window]

                    if not term in terms:
                        terms.append(term)
        
        return terms
    # ---------------------------------------------------------
    terms = {}
    # for every word in the text, save the position
    for pos, word in enumerate(text.split()):
        if not word in STOP_WORDS:
            for window in range(min_gram, min(max_gram + 1, len(word) + 1)):
                w = cln_string(word)
                term = w[:window]

                # if the term isn't in the dictionary,
                # then set the default as an array for the positions
                terms.setdefault(term, [])

                if not pos in terms[term]:
                    terms[term].append(pos)
    
    return terms

# get text appearances
def term_appearance(doc):
    # create the terms for every document
    # save them in the index
    title = doc['title']
    text = doc['text']
    page = doc['page']

    terms = text_2_terms(text)

    return {'title': title, 'page': page, 'terms': terms}

# return the index from term appearances
def make_index(term_appearances):
    # uses the term as key
    # the value is a dictionary of documents with the 
    # positions of the term as an array
    index = {}
    # for every document
    for doc_app in term_appearances:
        t = doc_app['title']
        te = doc_app['terms']
        p = doc_app['page']

        # for every term
        for k in te:
            # use the term as key
            # set dictionary
            index.setdefault(k, {})
            # use document title + page as key
            # store appearances
            index[k][t + '_' + str(p)] = (te[k])
    
    return index

# writes terms from a data file into another one
def parse_from_json(file):
    d_p = get_complete_path('data', file)
    i_p = index_path() + 'index.json'
    # open file
    with open(d_p, 'r', errors='ignore') as f:
        data = json.load(f)
        term_appearances = []

        # for every document stored in the json array
        for doc in data:
            term_appearances.append(term_appearance(doc))
    
    # inverted index
    index = make_index(term_appearances)

    
    # write to new file
    with open(i_p, 'w', errors="ignore") as index_doc:
        json.dump(index, index_doc)
