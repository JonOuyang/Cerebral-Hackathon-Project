from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/process', methods =['POST'])
def process():
    #get data that is passed over -> AJAX calls are in the form dict
    email = request.form['email']
    name = request.form['name']

    #complete action if both name and email exist
    if name and email:
        newName = name[::-1]
        return jsonify ({'name':newName}) #jsonify returns value in json format
    return jsonify({'error':'Missing data!'})

if __name__ == '__main__':
    app.run(debug=True)

