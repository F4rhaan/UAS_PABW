from flask import Flask, jsonify, request, render_template
import csv
import os

app = Flask(__name__)
FILE_NAME = 'cars-crud.csv'

# Upload and process a new CSV file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file as cars.csv
    file.save(FILE_NAME)
    return jsonify({'message': 'File uploaded successfully'}), 200

# Fetch all cars (Read operation)
@app.route('/cars', methods=['GET'])
def get_cars():
    if not os.path.exists(FILE_NAME):
        return jsonify({'error': 'No file uploaded yet. Please upload a file first.'}), 400

    with open(FILE_NAME, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return jsonify(list(reader))

# Serve HTML interface
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)