import os
from dotenv import load_dotenv

load_dotenv()

host = os.environ.get('HOST')
port = os.environ.get('PORT')
email = os.environ.get('EMAIL')
password = os.environ.get('EMAIL_PASSWORD')
password_length = 6
email_subject = "Вы были добавлены в систему"
email_body = ("Добро пожаловать в систему БКС!\nНиже в этом письме содержится ваш пароль для входа в систему, "
              "который был сгенерирован автоматически.\nАвторизуйтесь в системе и смените пароль в целях "
              "безопасности.\n\n{0}")
