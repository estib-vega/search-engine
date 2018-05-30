"""
the main file is the one that should be always started on

-sets up the files and the file manager
-parses the data and stores it
-starts the query loop

"""

import file_manager, engine, parser, sys

def main():
    
    while True:
        data = input('data file to be indexed: ')
        
        if data == 'e':
            print('exiting programm')
            sys.exit(1)
        # create file environment
        file_manager.setup()
        try:
            # copy the data into the directory
            file_manager.copy_data(data)
        except IOError as e:
            print(e)
            continue
        break

    print('readying the data to be parsed from', data)
    # parse data to index
    parser.parse_from_json(data)

    engine.qry_loop()

    file_manager.clean_up()



if __name__ == '__main__':
    main()    