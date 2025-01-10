import json
import random

# Генерация списков мужских и женских имен, фамилий и отчеств
male_names = ["Алексей", "Иван", "Дмитрий", "Сергей", "Максим", "Андрей", "Артём", "Владимир", "Павел", "Роман"]
male_surnames = ["Иванов", "Смирнов", "Кузнецов", "Попов", "Соколов", "Лебедев", "Козлов", "Новиков", "Морозов", "Петров"]
male_patronymics = ["Алексеевич", "Иванович", "Дмитриевич", "Сергеевич", "Максимович", "Андреевич", "Артёмович", "Владимирович", "Павлович", "Романович"]

female_names = ["Анастасия", "Мария", "Екатерина", "Ольга", "Татьяна", "Елена", "Юлия", "Наталья", "Ирина", "Виктория"]
female_surnames = ["Иванова", "Смирнова", "Кузнецова", "Попова", "Соколова", "Лебедева", "Козлова", "Новикова", "Морозова", "Петрова"]
female_patronymics = ["Алексеевна", "Ивановна", "Дмитриевна", "Сергеевна", "Максимовна", "Андреевна", "Артёмовна", "Владимировна", "Павловна", "Романовна"]

# Списки марок автомобилей
car_brands = ["ВАЗ", "BMW", "Mercedes-Benz", "Porsche", "Toyota", "Honda", "Ford", "Chevrolet", "KIA", "Hyundai"]

# Генерация случайного регистрационного номера в формате K392HP
def generate_reg_number():
    letters = ''.join(random.choices('АВЕКМНОРСТУХ', k=1))
    numbers = ''.join(random.choices('0123456789', k=3))
    region_letters = ''.join(random.choices('АВЕКМНОРСТУХ', k=2))
    return f"{letters}{numbers}{region_letters}"

# Генерация данных для каждого владельца
owner_data = []
for _ in range(25):
    men_or_women = random.randint(1, 2)
    if men_or_women == 1:
        person_name = random.choice(male_names)
        person_surname = random.choice(male_surnames)
        person_patronymic = random.choice(male_patronymics)
    else:
        person_name = random.choice(female_names)
        person_surname = random.choice(female_surnames)
        person_patronymic = random.choice(female_patronymics)
    reg_number = generate_reg_number()
    car_brand = random.choice(car_brands)
    engine_volume = round(random.randint(10, 40) / 10, 1)  # Объем двигателя в кубических сантиметрах
    year_of_release = random.randint(1990, 2023)
    year_of_registration = random.randint(year_of_release, 2023)
    data = {
        "surname": person_surname,
        "name": person_name,
        "patronymic": person_patronymic,
        "reg_number": reg_number,
        "car_brand": car_brand,
        "engine_volume": engine_volume,
        "year_of_release": year_of_release,
        "year_of_registration": year_of_registration,
    }
    owner_data.append(data)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(owner_data, f, ensure_ascii=False, indent=4)
    print('Successfully saved data to data.json')
