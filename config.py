import json

with open("config.json") as config_file:
    config_data = json.load(config_file)

PORT = config_data['port']
MAX_CONNECTION = 3
MAX_BUFFER_SIZE = 8096
LOG_CONFIG = config_data['logging']
PRIVACY = config_data['privacy']

RESTRICTION = config_data['restriction']
SLOW = 'SLOW'
BLOCK = 'BLOCK'
