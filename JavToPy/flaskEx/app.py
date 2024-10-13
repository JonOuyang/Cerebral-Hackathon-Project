from flask import Flask,render_template, request, jsonify
import os
import translators as ts #translator library


app = Flask(__name__,template_folder="templates")

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json() # retrieve the data sent from JavaScript
    # process the data using Python code
    result = ts.translate_text(data['value']) #actual translation
    return jsonify(result=result) #return in js
if __name__ == '__main__':
    app.run(debug=True)
