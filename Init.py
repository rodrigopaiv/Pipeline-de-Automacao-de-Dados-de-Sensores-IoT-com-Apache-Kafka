# Módulo de Inicialização das Configurações Básicas

# Imports
import traceback
from configparser import ConfigParser

#  Configs
CONFIG_FILE = "settings.conf"
CONFIG_SECTION = "settings"

# Classe
class Initialize():

    # Método construtoor
    def __init__(self):
        try:
            parser = ConfigParser()
            parser.read(CONFIG_FILE)
            
            # Caminho para o arquivo do Cupcarbon IoT Simulator
            self.data_path = parser.get(CONFIG_SECTION, "data_path")

            # Nome do arquivo do Cupcarbon IoT Simulator
            self.data_file = parser.get(CONFIG_SECTION, "data_file")

            # Servidor Kafka
            self.kafka_host = parser.get(CONFIG_SECTION, "kafka_host")
        except Exception as e:
            traceback.print_exc()



