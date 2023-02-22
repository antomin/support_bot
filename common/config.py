from environs import Env

env = Env()
env.read_env()

TG_TOKEN = env.str('TG_TOKEN')
SUPPORT_CHAT_ID = env.str('SUPPORT_CHAT_ID')
support_ids = [
    5159866416,
]
