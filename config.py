import configparser

def create_default_config(path):
    config = configparser.ConfigParser()
    config['Generic settings'] = {
        'host' : '127.0.0.1',
        'port' : '5432',
        'dbname' : 'database_name',
        'user' : 'ivan',
        'password' : '12345',
    }
    config['Small scale plot settings'] = {
        'wait_list' : "Client, Activity, IO, LWLock, Lock, Extension, IPC, BufferPin, Timeout",
    }
    config['History settings'] = {
        'history_path': 'history.csv',
    }
    with open(path, 'w') as configfile:
        config.write(configfile)
    return config

def get_config(path):
    current_config = configparser.ConfigParser()
    current_config.read(path)
    return current_config