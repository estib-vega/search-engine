# search-engine
simple python implementation for a search engine

The frontend was now updated using the Inferno JS framework. This is an expansion on React JS, while remaining with the same programming aproach and style. All of the frontend is in the carpet 'front-end'


As stated in the short description, this is a very simple implementation for a search engine.
It receives a PDF document and parses and indexes it so that it can be searched.

This implementation is based in microsearch by toastdriven:
https://www.youtube.com/watch?v=cY7pE7vX6MU

This search engine assumes only front n-grams with a maximal length of 6 characters.
It only returns the 10 most common page-results. And if the word isn't found, then it returns 2 n-grams max,
that can be made from the word that is being searched:

search('unappearing')

- 0 results for 'unappearing'
- max 10 page-results for 'u'
- max 10 page-results for 'un'

Dependencies:
- PyPDF2 for extracting the raw text from supported PDF files.
- flask and flask_restful for serving the UI as a local web app and API comunication.

The program is started from the Terminal (Command Line) as:
  python main.py
  
- It opens a browser and the app hosted at 'localhost:1234'
- Select a file by clicking the 'Choose a pdf file' button
- Clicking the 'upload' button will start parsing and indexing the file 
- After it's done, the site is redirected to the search bar, there you can start typing the 
    word you want to look for. The results will be displayed under the search bar
    You also have the option to click the 'new file search' button and parse another file.
- By terminating the programm from the Terminal with Ctrl+C, the uploaded file, the parsed data, and the
    index are deleted.
