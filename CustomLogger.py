# Módulo para leitura e geração de logs

# Imports
import time
import logging
import logging.handlers
from configparser import ConfigParser

#  Arquivo de configuração
CONFIGURATION_FILE = "settings.conf"

# Parser do arquivo
parser = ConfigParser()
parser.read(CONFIGURATION_FILE)

# LOG_PATH
LOG_PATH = parser.get('settings', 'log_path')

# PROJECT_NAME
PROJECT_NAME = parser.get("settings", "project_name")

# LOG_FILE
LOG_FILE = LOG_PATH + PROJECT_NAME

# Logger
logger = logging.getLogger('Projeto5')
log_handler = logging.FileHandler(LOG_FILE + "_" + time.strftime("%Y%m%d")+'.log')
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s',"%Y-%m-%d %H:%M:%S")
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.debug('Logger Inicializado')


