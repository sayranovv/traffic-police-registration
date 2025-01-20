from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Чтение данных из файла
with open('data.json', 'r', encoding='utf-8') as f:
    owners = json.load(f)

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
    return jsonify(owners) # Получаем данные запроса в формате JSON

# Определение маршрута для генерации отчета по типу
@app.route('/reports/<int:report_type>', methods=['POST'])
def generate_report(report_type):
    # Получаем данные запроса в формате JSON
    data = request.json
    # Копируем исходные данные, чтобы не изменять их напрямую
    sorted_data = owners[:]

    # Формирование отчета типа 1: Сортировка по году постановки на учет и фамилии
    if report_type == 1:
        # Сортируем по убыванию года регистрации и по возрастанию фамилии
        bubble_sort(sorted_data, lambda x: (-x['year_of_registration'], x['surname']))

    # Формирование отчета типа 2: Владельцы автомобилей ВАЗ, сортировка по году выпуска, объему двигателя и фамилии
    elif report_type == 2:
        # Сортируем по году выпуска, объему двигателя и фамилии, с фильтрацией внутри key_func
        bubble_sort(sorted_data, lambda x: (
            0 if x['car_brand'].lower() == 'ваз' else 1,  # Сначала ВАЗы
            -x['year_of_release'],
            x['engine_volume'],
            x['surname']
        ))
        # Оставляем только ВАЗы
        sorted_data = [x for x in sorted_data if x['car_brand'].lower() == 'ваз']

    # Формирование отчета типа 3: Владельцы автомобилей с годом выпуска ранее заданного
    elif report_type == 3:
        # Получаем год ограничения из данных запроса
        year_limit = data.get('year_limit', 0)
        # Сортируем по году выпуска и марке автомобиля, с фильтрацией внутри key_func
        bubble_sort(sorted_data, lambda x: (
            0 if x['year_of_release'] < year_limit else 1,  # Сначала те, кто младше year_limit
            -x['year_of_release'],
            x['car_brand']
        ))
        # Оставляем только те, кто младше year_limit
        sorted_data = [x for x in sorted_data if x['year_of_release'] < year_limit]

    # Если тип отчета не поддерживается, возвращаем ошибку (защита от дурака)
    else:
        return jsonify({"error": "Invalid report type"}), 400

    # Возвращаем отсортированные данные в формате JSON
    return jsonify(sorted_data)

# Запуск приложения Flask
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
