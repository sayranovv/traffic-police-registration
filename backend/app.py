from flask import Flask, jsonify, request
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)

# Чтение данных из файла
with open('data.json', 'r', encoding='utf-8') as f:
    owners = json.load(f)

def bubble_sort(data, key_func):
    n = len(data)
    for i in range(n):
        for j in range(n - i - 1):
            if key_func(data[j]) > key_func(data[j + 1]):
                data[j], data[j + 1] = data[j + 1], data[j]

@app.route('/owners', methods=['GET'])
def get_owners():
    return jsonify(owners)

@app.route('/reports/<int:report_type>', methods=['POST'])
def generate_report(report_type):
    data = request.json
    sorted_data = owners[:]

    if report_type == 1:
        bubble_sort(sorted_data, lambda x: (-x['year_of_registration'], x['surname']))
    elif report_type == 2:
        vaz_cars = list(filter(lambda x: x['car_brand'].lower() == 'ваз', sorted_data))
        bubble_sort(vaz_cars, lambda x: (-x['year_of_release'], x['engine_volume'], x['surname']))
        sorted_data = vaz_cars
    elif report_type == 3:
        year_limit = data.get('year_limit', 0)
        filtered_cars = list(filter(lambda x: x['year_of_release'] < year_limit, sorted_data))
        bubble_sort(filtered_cars, lambda x: (-x['year_of_release'], x['car_brand']))
        sorted_data = filtered_cars
    else:
        return jsonify({"error": "Invalid report type"}), 400

    return jsonify(sorted_data)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
