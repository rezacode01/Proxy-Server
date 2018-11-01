import datetime
from config import LOG_CONFIG

log_file_name = LOG_CONFIG['logFile']
log_enable = LOG_CONFIG['enable']
log_file = open(log_file_name, 'w')


def get_time():
    time = datetime.datetime.now()
    return time


def log(message):
    std_message = '[' + str(get_time()) + '] ' + str(message)
    print(std_message)
    if log_enable:
        log_file.write(std_message + '\n')


def log_header(data):
    if log_enable:
        log_file.write('\n' + str(get_time()) + '\n')
        log_file.write('-------------------------------------------\n')
        for line in data.splitlines():
            log_file.write(str(line) + '\n')
            print(line)
        log_file.write('-------------------------------------------\n')


def close():
    if log_enable:
        log_file.write('-------------------------------------' + '\n')
        log_file.close()
