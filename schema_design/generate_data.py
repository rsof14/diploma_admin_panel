from mimesis import Person
from mimesis.locales import Locale
from mimesis.enums import Gender
import yfinance as yf
import psycopg2
import random
import string
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

person = Person(locale=Locale.RU)
sex = [Gender.MALE, Gender.FEMALE]
cities = ['Астрахань', 'Барнаул', 'Волгоград', 'Воронеж', 'Екатеринбург', 'Ижевск', 'Иркутск', 'Казань',
          'Калининград', 'Калуга', 'Кемерово', 'Краснодар', 'Красноярск', 'Липецк', 'Москва', 'Нижний Новгород',
          'Новосибирск', 'Омск', 'Пермь', 'Санкт-Петербург', 'Сочи', 'Тюмень', 'Уфа', 'Челябинск', 'Ярославль']
roles = ['3864be7b-1432-4111-9056-5f7fc3ba8fb9', 'b7eb8dea-bf52-49df-aeba-ab716fad29bb',
         '8086f599-8822-4302-9b3e-cb14018af3de', '4773b77e-2637-496d-a86b-6e91279b0128',
         'd02f84a9-bc73-4f7f-9107-26484e449943']
tickers = ['AAPL', 'MSFT', 'NFLX', 'NVDA', 'META', 'TSLA', 'AMZN', 'WMT', 'PSX', 'OXY', 'GOOG', 'DIS',
           'SPOT', 'LLY', 'MRK', 'PFE']
weights = [30, 40, 15, 7, 8]
strategy_names = ['Стратегия Глобального Роста', 'Импульс Инноваций', 'Прорыв на Рынке', 'Агрессивный Баланс',
                  'Путь к Успеху', 'Сила Диверсификации', 'Выгодное Вложение', 'Движущая Сила Инвестиций',
                  'Золотой Фонд', 'Инвестиционный Ренессанс', 'Ключ к Прибыли', 'Мультистратегия', 'Ось Успеха',
                  'Путь к Стабильности', 'Растущая Мощь', 'Рыночная Экспансия', 'Скачок к Успеху',
                  'Стремление к Вершинам', 'Финансовая Независимость', 'Фортуна Инвестора', 'Взлет и Падение',
                  'Волна Роста', 'Грядущие Возможности', 'Древо Успеха', 'Защитный Экран', 'Инвестиции в Будущее',
                  'Ключ к Умножению', 'Мастер-План', 'На гребне Волны', 'Обогащение', 'Оптимальный Выбор',
                  'Погоня за Прибылью', 'Путь к Процветанию', 'Рост и Развитие', 'Рыночный Взрыв', 'Секрет Инвестора',
                  'Сила Финансов', 'Смелый Шаг', 'Создание Ценности', 'Стратегия Растущих Доходов', 'Триумф Инвестора',
                  'Устойчивый Рост', 'Финансовая Революция', 'Формула Успеха', 'Хребет Капитала', 'Ценные Вложения',
                  'Экономика Роста', 'Эффективное Распределение', 'Ядро Прибыли', 'Активный Рост',
                  'Амбициозный Инвестор', 'Баланс Риска и Дохода', 'Вершина Финансов', 'Вихрь Капитала', 'Волна Успеха',
                  'Выгодная Инвестиция', 'Гармония Финансов', 'Глобальное Видение', 'Двойная Сила', 'Доходный Путь',
                  'Дорога к Богатству', 'Инвестор-Победитель', 'Капитальный Взрыв', 'Ключ к Успеху',
                  'Концентрическая Экспансия', 'Максимальная Прибыль', 'Мастерство Инвестиций', 'Многоуровневая Мощь',
                  'Неограниченный Доход', 'Новый Век Инвестиций', 'Оптимизация Прибыли', 'Перспективные Вложения',
                  'Поток Финансов', 'Прогрессивные Инвестиции', 'Путь к Финансовой Свободе', 'Рост и Процветание',
                  'Рыночная Динамика', 'Сила Эффективных Инвестиций', 'Смелые Решения', 'Созидательный Инвестор',
                  'Стабильность и Рост', 'Стратегический Инвестор', 'Тайная Формула', 'Триумф Финансов',
                  'Уверенный Рост', 'Финансовая Гибкость', 'Финансовый Вихрь', 'Фортуна на Сторону', 'Центр Прибыли',
                  'Энергия Финансов', 'Эффективный Рост', 'Ясный Путь', 'Авантюрный Инвестор', 'Взлет к Вершине',
                  'Волшебство Финансов', 'Глобальный Взрыв', 'Идеальная Инвестиция', 'Инвестор с Большой Буквы',
                  'Ключ к Будущему', 'Мощь Диверсифицированных Инвестиций']
currency = ['RUB', 'USD', 'EUR']
strategy_types = ['Регламентная', 'Индивидуальная']
risk_profiles = ['Умеренный', 'Консервативный', 'Рациональный', 'Агрессивный']


def generate_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def get_customer():
    return str(uuid.uuid4()), person.full_name(gender=random.choice(sex)), random.choice(cities)


def get_user():
    return (str(uuid.uuid4()), person.email(domains=['bcs.ru']), person.full_name(gender=random.choice(sex)),
            generate_password(10), '2024-01-05', False, random.choice(roles))


def get_assets():
    assets = [yf.Ticker(t) for t in tickers]
    for asset in assets:
        asset_info = asset.get_info()
        print(f"('{asset.isin}', '{asset_info['symbol']}', '{asset_info['shortName']}', '{asset_info['sector']}'), ")


def generate_strategy_structure():
    result = '{'
    for weight in weights:
        result += f'"{random.choice(tickers)}": {weight}, '
    result = result[:len(result) - 2]
    result += '}'
    return result


def get_benchmark():
    return '{"IMOEX": 100}'


def generate_strategy():
    for strategy_name in strategy_names:
        print(
            f"('{str(uuid.uuid4())}', '{strategy_name}', '{random.choice(currency)}', '{random.choice(strategy_types)}', '{random.choice(risk_profiles)}', '{generate_strategy_structure()}', {True}, {round(random.uniform(0.1, 0.9), 1)}, {round(random.uniform(1, 5), 1)}, '{get_benchmark()}'), ")


def generate_account_numb():
    return f"{int(random.uniform(100000, 999999))}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}"


def generate_portfolio():
    conn = psycopg2.connect(host=os.environ.get('DB_HOST', '127.0.0.1'),
                            port=os.environ.get('DB_PORT', 5432),
                            database=os.environ.get('DB_NAME'),
                            user=os.environ.get('DB_USER'),
                            password=os.environ.get('DB_PASSWORD'))
    cur = conn.cursor()
    cur.execute("SELECT id from public.customer;")
    customers = cur.fetchall()
    cur.execute("SELECT id from public.strategy;")
    strategies = cur.fetchall()
    cur.execute("SELECT id from public.roles WHERE name = 'Управляющий';")
    role_id = cur.fetchone()
    cur.execute(f"SELECT id from public.user WHERE role_id = '{str(role_id[0])}';")
    users = cur.fetchall()
    for i in range(0, 300):
        account = generate_account_numb()
        customer_id = str(random.choice(customers)[0])
        strategy_id = str(random.choice(strategies)[0])
        manager_id = str(random.choice(users)[0])
        print(f"('{account}', '{customer_id}', '{strategy_id}', '{manager_id}', '2024-01-05', {False}), ")


def main():
    # Generate 200 customers
    for _ in range(0, 200):
        print(f'{get_customer()},')
    # Generate 30 users
    for _ in range(0, 30):
        print(f'{get_user()},')
    get_assets()
    generate_strategy()
    generate_portfolio()

main()