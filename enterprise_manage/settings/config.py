import configparser
import os


conf = configparser.ConfigParser()
cur_path = os.path.dirname(os.path.realpath(__file__))
config_url = os.path.join(cur_path, 'config.ini')
conf.read(config_url)

MYSQL_IP = conf.get('mysql', 'mysql_ip')
MYSQL_PORT = conf.get('mysql', 'mysql_port')
MYSQL_DB = conf.get('mysql', 'mysql_db')
MYSQL_USER = conf.get('mysql', 'mysql_user')
MYSQL_PASSWORD = conf.get('mysql', 'mysql_password')
