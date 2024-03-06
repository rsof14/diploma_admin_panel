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
from datetime import datetime
from passlib.hash import pbkdf2_sha256
from static_data import CITIES, CURRENCY, TICKERS, STRATEGY_NAMES, STRATEGY_TYPES, WEIGHTS, RISK_PROFILES, \
    SYSTEM_OBJECTS, PERMISSIONS, ROLES, RISK_METRICS, CUSTOMER_NUMBER, USER_NUMBER, TICKER_ISIN, PORTFOLIO_NUMBER

load_dotenv()

person = Person(locale=Locale.RU)
sex = [Gender.MALE, Gender.FEMALE]

conn = psycopg2.connect(host=os.environ.get('DB_HOST', '127.0.0.1'),
                        port=os.environ.get('DB_PORT', 5432),
                        database=os.environ.get('DB_NAME'),
                        user=os.environ.get('DB_USER'),
                        password=os.environ.get('DB_PASSWORD'))
cur = conn.cursor()


def generate_currency():
    result = "INSERT INTO public.currency (currency, description) VALUES \n"
    for curr in CURRENCY:
        result += f"{curr}, \n"
    result = result[:len(result) - 3]
    result += " ON CONFLICT DO NOTHING;"
    return result


def generate_system_objects():
    result = "INSERT INTO public.system_objects (object_name) VALUES \n"
    for obj in SYSTEM_OBJECTS:
        result += f"('{obj}'), \n"
    result = result[:len(result) - 3]
    result += " ON CONFLICT DO NOTHING;"
    return result


def generate_permissions():
    result = "INSERT INTO public.permissions (permission) VALUES \n"
    for perm in PERMISSIONS:
        result += f"('{perm}'), \n"
    result = result[:len(result) - 3]
    result += " ON CONFLICT DO NOTHING;"
    return result


def generate_roles():
    result = "INSERT INTO public.roles (id, name) VALUES \n"
    for role in ROLES:
        result += f"('{str(uuid.uuid4())}', '{role}'), \n"
    result = result[:len(result) - 3]
    result += " ON CONFLICT DO NOTHING;"
    return result


def generate_strategy_type():
    result = "INSERT INTO public.strategy_type (type) VALUES \n"
    for str_type in STRATEGY_TYPES:
        result += f"('{str_type}'), \n"
    result += "('NULL'), \n"
    result = result[:len(result) - 3]
    result += " ON CONFLICT DO NOTHING;"
    return result


def generate_objects_permissions():
    result = "INSERT INTO public.objects_permissions (object, role_id, permission, strategy_type, id) VALUES \n"
    cur.execute("SELECT id from public.roles;")
    roles_ids = cur.fetchall()
    for obj in SYSTEM_OBJECTS:
        for role_id in roles_ids:
            result += (f"('{obj}', '{str(role_id[0])}', '{random.choice(PERMISSIONS)}', "
                       f"'{random.choice(STRATEGY_TYPES) if obj == 'Strategy' else 'NULL'}', '{str(uuid.uuid4())}'), \n")
    result = result[:len(result) - 3]
    result += " ON CONFLICT DO NOTHING;"
    return result


def generate_risk_profiles():
    result = "INSERT INTO public.risk_profile (name, max_var) VALUES \n"
    for profile in RISK_PROFILES:
        result += f"('{profile}', {round(random.uniform(0.1, 0.8), 2)}), \n"
    result = result[:len(result) - 3]
    result += " ON CONFLICT DO NOTHING;"
    return result


def generate_risk_metrics():
    result = "INSERT INTO public.risk_metrics (name) VALUES \n"
    for metric in RISK_METRICS:
        result += f"('{metric}'), \n"
    result = result[:len(result) - 3]
    result += " ON CONFLICT DO NOTHING;"
    return result


def generate_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def generate_hashed_password(length=None):
    password = '123qwe'
    if length:
        password = generate_password(length)
    return pbkdf2_sha256.hash(password)


def generate_customer():
    result = "INSERT INTO public.customer (id, name, branch) VALUES \n"
    for _ in range(0, CUSTOMER_NUMBER):
        result += (f"('{str(uuid.uuid4())}', '{person.full_name(gender=random.choice(sex))}', "
                   f"'{random.choice(CITIES)}'), \n")
    result = result[:len(result) - 3]
    result += " ON CONFLICT DO NOTHING;"
    return result


def generate_user():
    result = "INSERT INTO public.user (id, login, name, password, created_at, is_superuser, role_id) VALUES \n"
    cur.execute("SELECT id from public.roles;")
    roles_ids = cur.fetchall()
    for _ in range(0, USER_NUMBER):
        result += (f"('{str(uuid.uuid4())}', '{person.email(domains=['bcs.ru'])}', "
                   f"'{person.full_name(gender=random.choice(sex))}', '{generate_hashed_password()}', "
                   f"'2024-01-05', {False}, '{str(random.choice(roles_ids)[0])}'), \n")
    result = result[:len(result) - 3]
    result += " ON CONFLICT DO NOTHING;"
    return result


def generate_assets():
    result = 'INSERT INTO public.asset ("ISIN", ticker, name, sector) VALUES \n'
    assets = [yf.Ticker(t) for t in TICKERS]
    for asset in assets:
        asset_info = asset.get_info()
        isin = TICKER_ISIN[asset_info['symbol']] if asset.isin == '-' else asset.isin
        result += (f"('{isin}', '{asset_info['symbol']}', '{asset_info['shortName']}', "
                   f"'{asset_info['sector']}'), \n")
    result = result[:len(result) - 3]
    result += " ON CONFLICT DO NOTHING;"
    return result


def generate_strategy_structure():
    result = '{'
    for weight in WEIGHTS:
        result += f'"{random.choice(TICKERS)}": {weight}, '
    result = result[:len(result) - 2]
    result += '}'
    return result


def get_benchmark():
    return '{"IMOEX": 100}'


def generate_strategy():
    result = ('INSERT INTO public.strategy(id, name, currency, type, risk_profile, structure, valid, management_fee, '
              'success_fee, benchmark) VALUES \n')
    cur.execute("SELECT currency from public.currency;")
    strategy_currency = cur.fetchall()
    for strategy_name in STRATEGY_NAMES:
        result += (f"('{str(uuid.uuid4())}', '{strategy_name}', '{random.choice(strategy_currency)[0]}', "
                   f"'{random.choice(STRATEGY_TYPES)}', '{random.choice(RISK_PROFILES)}', "
                   f"'{generate_strategy_structure()}', {True}, {round(random.uniform(0.1, 0.9), 1)}, "
                   f"{round(random.uniform(1, 5), 1)}, '{get_benchmark()}'), \n")
    result = result[:len(result) - 3]
    result += " ON CONFLICT DO NOTHING;"
    return result


def generate_account_numb():
    return f"{int(random.uniform(100000, 999999))}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}"


def get_portfolio_structure():
    return '{}'


def generate_portfolio():
    result = ("INSERT INTO public.portfolio (account, customer_id, strategy_id, structure, asset_manager, "
              "creation_date,"
              "updated) VALUES \n")
    cur.execute("SELECT id from public.customer;")
    customers = cur.fetchall()
    cur.execute("SELECT id from public.strategy;")
    strategies = cur.fetchall()
    cur.execute("SELECT id from public.roles WHERE name = 'Управляющий';")
    role_id = cur.fetchone()
    cur.execute(f"SELECT id from public.user WHERE role_id = '{str(role_id[0])}';")
    users = cur.fetchall()
    for i in range(0, PORTFOLIO_NUMBER):
        account = generate_account_numb()
        customer_id = str(random.choice(customers)[0])
        strategy_id = str(random.choice(strategies)[0])
        manager_id = str(random.choice(users)[0])
        result += f"('{account}', '{customer_id}', '{strategy_id}', '{get_portfolio_structure()}', '{manager_id}', '2024-01-05', {False}), \n"
    result = result[:len(result) - 3]
    result += " ON CONFLICT DO NOTHING;"
    return result


def generate_portfolio_values():
    result = "INSERT INTO public.portfolio_values (account, date, value) VALUES \n"
    cur.execute("SELECT account from public.portfolio;")
    portfolios = cur.fetchall()
    for account in portfolios:
        result += f"('{account[0]}', '{datetime.now().date().strftime('%Y-%m-%d')}', {random.randint(1000000, 5000000)}), \n"
    result = result[:len(result) - 3]
    result += " ON CONFLICT DO NOTHING;"
    return result


def generate_basic_objects():
    """Returning sql file with insert operation, this file must be executed before formation dependent objects"""
    result = (
        f"{generate_currency()}\n{generate_system_objects()}\n{generate_permissions()}\n{generate_roles()}\n"
        f"{generate_strategy_type()}\n{generate_risk_profiles()}\n"
        f"{generate_risk_metrics()}\n{generate_customer()}\n{generate_assets()}\n"
        f"")
    f = open('basic_objects.sql', 'w')
    f.write(result)
    f.close()


def generate_dependent_objects():
    result = (f"{generate_objects_permissions()}\n{generate_user()}\n{generate_strategy()}\n"
              f"{generate_portfolio()}")
    f = open('dependent_objects.sql', 'w')
    f.write(result)
    f.close()


def generate_ramaining_objects():
    result = f"{generate_portfolio_values()}"
    f = open('remaining_objects.sql', 'w')
    f.write(result)
    f.close()


generate_basic_objects()
