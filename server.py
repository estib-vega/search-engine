"""
    the server module is in charge of opening the 
    browser and serving the ui html

"""

from flask import Flask, render_template, send_from_directory, request, jsonify
import webbrowser, threading, user_interface
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# class for query processing
class QueryApi(Resource):
     def get(self, qry):
        response = user_interface.search(qry)
        return jsonify({'results': response})

# api
api.add_resource(QueryApi, "/query/api/<string:qry>")

# home
@app.route("/")
def hello():
    params = request.args.get('input_file', default="-", type=str)
    if params == "-":
        return render_template("index.html")
    else:
        return render_template("search.html")

# static files - css
@app.route("/css/<path:path>")
def send_css(path):
    return send_from_directory("./templates/css", path)

# posting file
@app.route("/fileupload", methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check file...
        # TODO
        # save file
        file = request.files['file']
        file.save('./uploads/file.pdf')

        # parse it 
        t = threading.Thread(target=user_interface.parse_data, args=('file.pdf',), daemon=True)
        t.start()

        return jsonify({'msg': 'succesfull'})

# get results for query
@app.route("/qry")
def search_qry():
    query = request.args.get('query', "-", type=str)
    resp = user_interface.search(query)
    return jsonify(result=resp)


# start flask server
def run(p):
    app.run(host='localhost', port=p)

# open web browser window
def open_browser(port):
    from time import sleep
    
    # wait a bit so that the server can start
    # before the 
    sleep(0.25)
    browser = webbrowser.get('safari')
    # run in local host
    url = '127.0.0.1:' + str(port)

    browser.open_new(url)

# start serving and open page
def start(p):
    PORT = p
    # open browser in a separate thread
    # so that it can wait a bit for the server to start running
    t = threading.Thread(target=open_browser, args=(PORT,), daemon=True)
    t.start()
    # run server
    run(PORT)


if __name__ == "__main__":
    start(1234)