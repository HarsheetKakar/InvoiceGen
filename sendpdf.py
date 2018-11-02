import codecs

from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    filename = request.form.get('invoice.pdf')
    print(filename)
    file_data = codecs.open(filename, 'rb').read()
    response = make_response()
    response.headers['my-custom-header'] = 'my-custom-status-0'
    response.data = file_data
    return response

if __name__ == '__main__':
    app.run(debug=True)
