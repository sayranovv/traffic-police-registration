from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Чтение данных из файла
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Сохранение данных в файл
def save_data(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Реализация функции сортировки обменом (сортировка пузырьком)
def bubble_sort(data, key_func):
    n = len(data)
    for i in range(n):
        for j in range(n - i - 1):
            if key_func(data[j]) > key_func(data[j + 1]):
                data[j], data[j + 1] = data[j + 1], data[j]

# Определение маршрута для получения списка всех владельцев автомобилей
@app.route('/owners', methods=['GET'])
def get_owners():
    owners = load_data()
    return jsonify(owners)

# Определение маршрута для генерации отчета по типу
@app.route('/reports/<int:report_type>', methods=['POST'])
def generate_report(report_type):
    # Получаем данные запроса в формате JSON
    data = request.json
    owners = load_data()
    sorted_data = owners[:]

    # Формирование отчета типа 1: Сортировка по году постановки на учет и фамилии
    if report_type == 1:
        bubble_sort(sorted_data, lambda x: (-x['year_of_registration'], x['surname']))

    # Формирование отчета типа 2: Владельцы автомобилей ВАЗ, сортировка по году выпуска, объему двигателя и фамилии
    elif report_type == 2:
        bubble_sort(sorted_data, lambda x: (
            0 if x['car_brand'].lower() == 'ваз' else 1,
            -x['year_of_release'],
            x['engine_volume'],
            x['surname']
        ))
        sorted_data = [x for x in sorted_data if x['car_brand'].lower() == 'ваз']

    # Формирование отчета типа 3: Владельцы автомобилей с годом выпуска ранее заданного
    elif report_type == 3:
        year_limit = data.get('year_limit', 0)
        bubble_sort(sorted_data, lambda x: (
            0 if x['year_of_release'] < year_limit else 1,
            -x['year_of_release'],
            x['car_brand']
        ))
        sorted_data = [x for x in sorted_data if x['year_of_release'] < year_limit]

    else:
        return jsonify({"error": "Invalid report type"}), 400

    return jsonify(sorted_data)

# Определение маршрута для добавления нового владельца
@app.route('/owners', methods=['POST'])
def add_owner():
    new_owner = request.json
    owners = load_data()
    owners.append(new_owner)
    save_data(owners)
    return jsonify({"message": "Owner added successfully"}), 201

# Определение маршрута для редактирования владельца по регистрационному номеру
@app.route('/owners/<string:reg_number>', methods=['PUT'])
def edit_owner(reg_number):
    updated_owner = request.json
    owners = load_data()
    for i, owner in enumerate(owners):
        if owner['reg_number'] == reg_number:
            owners[i] = updated_owner
            save_data(owners)
            return jsonify({"message": "Owner updated successfully"}), 200
    return jsonify({"error": "Owner not found"}), 404

# Определение маршрута для удаления владельца по регистрационному номеру
@app.route('/owners/<string:reg_number>', methods=['DELETE'])
def delete_owner(reg_number):
    owners = load_data()
    owners = [owner for owner in owners if owner['reg_number'] != reg_number]
    save_data(owners)
    return jsonify({"message": "Owner deleted successfully"}), 200

# Запуск приложения Flask
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
