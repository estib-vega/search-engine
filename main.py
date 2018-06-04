"""
the main file is the one that should be always started on

-sets up the files and the file manager
-parses the data and stores it
-starts the query loop
-in the end, it cleans up

"""

import file_manager, engine, parser, sys, server

# main if it's using the terminal as an interface
def terminal_main():
    while True:
        data = input('data file to be indexed: ')
        
        if data == 'e':
            print('exiting programm')
            # delete all
            file_manager.clean_up()
            sys.exit(1)

        # create file environment
        file_manager.setup()
        try:
            # copy the data into the directory
            file_manager.copy_data(data)
        except IOError as e:
            continue
        except RuntimeError as e:
            print(e, '\nending progroamm')
            file_manager.clean_up()
            sys.exit(1)
        break

    print('readying the data to be parsed from', data)
    # parse data to index
    data_json = data.split('.')[0] + '.json'
    parser.parse_from_json(data_json)

    # start search
    try:
        engine.qry_loop()
    except Exception as e:
        print('Error:', e, '\nexiting programm')
        file_manager.clean_up()


    # delete all
    file_manager.clean_up() 


# main if it's using browser user interface
def browser_main():
    # set up file environment
    file_manager.setup()

    # run ui
    server.start(1234)

    # delete all
    file_manager.clean_up() 

def main():
    args = sys.argv

    # if the length of the args,
    # is 1, then do the browser ui
    if len(args) == 1:
        browser_main()
    elif len(args) == 2:
        if args[1] == "-t":
            # open terminal ui
            terminal_main()



if __name__ == '__main__':
    main()    