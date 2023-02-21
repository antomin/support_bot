import os

from environs import Env

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

env = Env()
env.read_env(os.path.join(BASE_DIR, '../.env'))

TG_TOKEN = env.str('TG_TOKEN')
