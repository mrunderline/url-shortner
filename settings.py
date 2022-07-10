from dotenv import load_dotenv
from urllib.parse import quote

import os

load_dotenv()

DOMAIN = os.getenv("DOMAIN")

DATABASE_URL = f'mysql+pymysql://{os.getenv("DATABASE_USERNAME")}:{quote(os.getenv("DATABASE_PASSWORD"))}@{os.getenv("DATABASE_HOST")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}'

SHORTNER_SALT = os.getenv('SHORTNER_SALT', 'mrunderline random url shortner salt')
