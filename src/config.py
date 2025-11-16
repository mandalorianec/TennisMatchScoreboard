import os
from dotenv import load_dotenv

load_dotenv()


min_len_name = os.getenv('MIN_LEN_NAME')
max_len_name = os.getenv('MAX_LEN_NAME')

user = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD_DB")

disable_loging = os.getenv('DISABLE_LOGGING', 'false')

allow_origins_env = os.getenv("ALLOW_ORIGINS")