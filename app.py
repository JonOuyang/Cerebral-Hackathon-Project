from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, template_folder="templates")

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()  # retrieve the data sent from JavaScript
    result = ts.translate_text(data['value'])  # various processing steps
    print(data)
    print(result)
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)
