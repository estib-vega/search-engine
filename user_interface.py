"""
    the user interface communicates between the
    server requests and the search engine

    it is started in server.py

    -processes queries and gives them to the engine
    -returns response for the frontend
"""

import file_manager, parser, engine, sys


# when the file is succesfully uploaded
# the data needs to be parsed from it
def parse_data(file):
    from time import sleep

    sleep(1)
    

    filepath = file_manager.uploads_path() + file
    name = file.split('.')[0]
    print("parsing file", filepath)
    # parse to data json
    try:
        # copy the data into the directory
        file_manager.copy_data(filepath)
    except IOError as e:
        print(e)
        file_manager.clean_up()
    except RuntimeError as e:
        print(e, '\nending progroamm')
        file_manager.clean_up()
        sys.exit(1)

    # from json, to index json
    parser.parse_from_json(name + ".json")

# search query
def search(qry):
    resp = engine.qry_2_string(qry)

    return resp