from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

BACKEND_URL = 'http://backend:8000'  # URL бэкенда

@app.route('/')
def index():
    return render_template('index.html')  # Шаблон с формой для поиска вакансий

@app.route('/search', methods=['POST'])
def search():
    data = request.form
    response = requests.post(f'{BACKEND_URL}/search', json=data)
    return jsonify(response.json())

@app.route('/filter', methods=['POST'])
def filter_vacancies():
    data = request.form
    response = requests.post(f'{BACKEND_URL}/filter', json=data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
