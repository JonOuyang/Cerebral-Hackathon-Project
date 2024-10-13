from flask import Flask, jsonify, request 
 
app = Flask(__name__) 
 
@app.route('/api/data', methods=['GET']) 
def get_data(): 
    # Sample data you want to return 
    data = {"message": "Hello from Flask!"} 
    return jsonify(data) 
 
@app.route('/api/execute', methods=['POST']) 
def execute_function(): 
    # Example of executing a function and returning a result 
    input_data = request.json.get('input', '') 
    result = f"Processed: {input_data}" 
    return jsonify({"result": result}) 
 
if __name__ == '__main__': 
    app.run(debug=True)
