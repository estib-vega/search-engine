"""
the file manager is in charged of knowing
where the things should and are stored.

all is read from and stored to a file
"""
import os, json
from shutil import rmtree, copy2
from pdf_parser import pdf_2_json

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

# return the joint path for a specific folder
# and a doc name
def get_complete_path(folder, name):
    if folder == 'index':
        return os.path.join(index_path(), name)
    elif folder == 'data':
        return os.path.join(data_path(), name)
    else:
        raise AttributeError('The folder must be either "data" or "index"')

# return index path
def setup():
    index = "./docs/index/"
    data = "./docs/data/"
    paths = "./docs/paths.json"

    # if the folder doesn't exist, then create it
    # index
    if not os.path.exists(index):
        os.makedirs(index)

    # data
    if not os.path.exists(data):
        os.makedirs(data)

    # write the paths to the path 
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

# copy the data file to the data directory
def copy_data(path):
    src = './' + path
    dst = data_path()
    suff = path.split('.')[-1]
    name = path.split('.')[0]

    if os.path.exists(src):
        if suff == 'pdf':
            d = dst + name + '.json'
            pdf_2_json(src, d)
        else:
            copy2(src, dst)
    else:
        raise IOError('File does not exist')
