"""
the file manager is in charged of knowing
where the things should and are stored.

all is read from and stored to a file
"""
import os, json
from shutil import rmtree

# return the joint path for a specific folder
# and a doc name
def get_complete_path(folder, name):
    if folder == 'index':
        return os.path.join(index_path(), name)
    elif folder == 'data':
        return os.path.join(data_path(), name)
    else:
        raise AttributeError('The folder must be either "data" or "index"')

# read from paths
def read_path(key):
    with open("./docs/paths.json", 'r') as f:
        path = json.load(f)

        return path[key]

# return index path
def index_path():
   return read_path('index')

# return path from which 
# the data should be read
def data_path():
    return read_path('data')

# return index path
def setup():
    index = "./docs/index"
    data = "./docs/data"
    paths = "./docs/paths.json"

    # if the folder doesn't exist, then create it
    # index
    if not os.path.exists(index):
        os.makedirs(index)

    # data
    if not os.path.exists(data):
        os.makedirs(data)

    # write the paths to the path 
    if not os.path.exists(paths):
        p = {'index': index, 'data': data}
        with open(paths, 'w', errors='ignore') as f:
            json.dump(p, f)

# delete all files from data and index
def clean_up():
    # remove complete directories
    if os.path.exists(index_path()):
        rmtree(index_path(), ignore_errors=True)

    if os.path.exists(data_path()):
        rmtree(data_path(), ignore_errors=True)

    # create them again
    setup()

def main_test():
    from time import sleep

    setup()
    print(index_path())
    print(data_path())
    index_p = get_complete_path('index', 'my.txt')
    data_p = get_complete_path('data', 'my.txt')

    try:
        print(get_complete_path('jj', 'my.txt'))
    except AttributeError as e:
        print(e)

    print(index_p)
    print(data_p)
    with open(index_p, 'w') as f:
        f.write('hello index')

    with open(data_p, 'w') as f:
        f.write('hello data')

    sleep(5)

    clean_up()

if __name__ == '__main__':
    main_test()