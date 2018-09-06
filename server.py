"""
    the server module is in charge of opening the 
    browser and serving the ui html

    -it communicates to the model through the user interface
    -it receives the GET and POST requests
    -it saves the file in the uploads
    -it responds to the queries with the answers given from the user_interface
"""

from flask import Flask, render_template, send_from_directory, request, jsonify
import webbrowser, threading, user_interface
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# the file has been indexed
ready = False
shouldRedirectHome = False

# parse the file
def parse_file(file):
    # start parsing the file and when
    # notify when done
    # global ready, shouldRedirectHome
    try:
        return user_interface.parse_data(file)
    except Exception as e:
        print(e)
        # ready = True
        # shouldRedirectHome = True
        return False
    

# class for query processing
class QueryApi(Resource):
     def get(self, qry):
        response = user_interface.search(qry)

        if not response == None:
            # found something
            status = response.split('___')[0]
            results = response.split('___')[1]
            return jsonify({'status': status, 'results': results})
        else:
            # found nothing 
            return jsonify({'status': 'nothing found', 'results': ''})

# api
api.add_resource(QueryApi, "/query/api/<string:qry>")

# home
@app.route("/")
def hello():
    user_interface.reset()
    return render_template("inferno/index.html")
    # params = request.args.get('input_file', default="-", type=str)
    # if params == "-":
    #     user_interface.reset()
    #     # global ready, shouldRedirectHome
    #     # ready = False
    #     # shouldRedirectHome = False
    #     return render_template("inferno/index.html")
    # else:
    #     # if there is a file query, it means it is the redirection
    #     # after the successful posting of the file
        
    #     # --- wait until the file is parsed
    #     while not ready:
    #         pass
    #     if not shouldRedirectHome:
    #         return render_template("search.html")
    #     else:
    #         ready = False
    #         shouldRedirectHome = False
    #         return render_template("index.html", error_msg="Couldn't parse PDF, please try other")

# static files - css
@app.route("/static/css/<path:path>")
def send_css(path):
    return send_from_directory("./templates/inferno/static/css", path)

@app.route("/static/js/<path:path>")
def send_js(path):
    return send_from_directory("./templates/inferno/static/js", path)

# posting file
@app.route("/fileupload", methods=['POST'])
def upload_file():
    if request.method == 'POST':
        print('post received')
        # save the file locally
        file = request.files['file']
        file.save('./uploads/file.pdf')

        # start parsing file, and return succes or failure
        success = parse_file('file.pdf')

        if success: return jsonify({'msg': 'succesfull'})

        return jsonify({'msg': 'failed'})

# start flask server
def run(p):
    app.run(host='localhost', port=p)

# open web browser window
def open_browser(port):
    from time import sleep
    
    # wait a bit so that the server can start
    # before the browser opens
    sleep(0.25)
    # browser = webbrowser.get()
    # run in local host
    url = '127.0.0.1:' + str(port)

    webbrowser.open_new(url)

# start serving and open page
def start(p):
    PORT = p
    # open browser in a separate thread
    # so that it can wait a bit for the server to start running
    t = threading.Thread(target=open_browser, args=(PORT,), daemon=True)
    t.start()
    # run server
    run(PORT)
