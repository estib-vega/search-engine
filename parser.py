"""
the string parser takes the normal string of text
(query or searchable)
and creates terms or n-grams

this terms are stored, if they come from the searchable data,
in files that then can be easily searched by the engine

if they come from a query, only the terms are returned

"""

import json
from pprint import pprint

# make terms from text
def text_2_terms(text, min_gram=3, max_gram=6, position=True):
    if not position:
        terms = []
        # return only the terms without 
        # position (used for queries)
        for word in text.split():
            for window in range(min_gram, min(max_gram + 1, len(word) + 1)):
                term = word[:window]

                if not term in terms:
                    terms.append(term)
        
        return terms
    # ---------------------------------------------------------
    terms = {}
    # for every word in the text, save the position
    for pos, word in enumerate(text.split()):
        for window in range(min_gram, min(max_gram + 1, len(word) + 1)):
            term = word[:window]

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

    terms = text_2_terms(text)

    return {'title': title, 'terms': terms}

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

        # for every term
        for k in te:
            # use the term as key
            # set dictionary
            index.setdefault(k, {})
            # use document title as key
            # store appearances
            index[k][t] = (te[k])
    
    return index

# writes terms from a data file into another one
def parse_from_json(file):
    # open file
    with open(file, 'r', errors='ignore') as f:
        data = json.load(f)
        term_appearances = []

        # for every document stored in the json array
        for doc in data:
            term_appearances.append(term_appearance(doc))
    
    # inverted index
    index = make_index(term_appearances)

    # write to new file
    with open('sample_index.json', 'w', errors="ignore") as index_doc:
        json.dump(index, index_doc)


                    



def main_test():
    parse_from_json('sample_data.json')
    # pass


if __name__ == '__main__':
    main_test()