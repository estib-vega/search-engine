"""
the pdf parser opens a pdf and converts it into json 
data for the string parser

for parsing we use the library PyPDF2

"""

import PyPDF2, json


# write to json file
def write_json_data(json_file, obj):
    with open(json_file, 'w') as f:
        json.dump(obj, f)

        print('parsed to', json_file)

# returns an array of dictionaries with the name of file, 
# page index and string of raw text
def parse_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as f:
        # readable object from pdf
        pdfReader = PyPDF2.PdfFileReader(f)
        num_pages = pdfReader.numPages
        # page count
        count = 0

        # list of objects to return
        pdf_dict = []
        # save only the name of the file
        title = pdf_file.split('/')[-1]
        #The while loop will read each page
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count += 1
            text = pageObj.extractText()

            # convert to ascii string
            t = text.encode(encoding='ascii', errors='ignore').decode()
            clean_text = ''.join(c for c in t if c.isprintable())
            pdf_dict.append({'title': title, 'page': count, 'text': clean_text})
        
        print('parsed from', pdf_file, '\nnumber of pages:', count)
        return pdf_dict

# from a pdf to json data
def pdf_2_json(pdf_file, json_file):
    pdf = parse_from_pdf(pdf_file)
    write_json_data(json_file, pdf)
