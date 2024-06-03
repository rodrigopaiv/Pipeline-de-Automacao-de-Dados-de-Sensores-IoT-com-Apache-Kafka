# App Python com o Kafka Producer

# Módulo produtor para enviar os dados dos sensores do CupCarbon (IoT_Simulator) para o Kafka (Streamer de Dados)

# Instale o Miniconda (se não tiver ainda) e execute no terminal: pip install kafka-python

# Imports
import csv
import sys
import time
import subprocess
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime, timedelta

# Imports dos módulos auxiliares
from Init import Initialize
from CustomLogger import logger

# Inicializa as configurações
init_object = Initialize()

# Classe para o Kafka Producer
class kafka_producer():

    # Método de publicação de mensagens
    def publish_message(self, producer_instance, topic_name, key, value):
        try:
            key_bytes = bytearray(key,'utf8')
            value_bytes = bytearray(value,'utf8')
            producer_instance.send(topic_name, key = key_bytes, value = value_bytes)
            producer_instance.flush()
            print('Mensagem Publicada com Sucesso.')
        except Exception as ex:
            print('Erro ao publicar a mensagem.')
            print(str(ex))

    # Método de conexão no Kafka
    def connect_kafka_producer(self):
        _producer = None
        try:
            _producer = KafkaProducer(bootstrap_servers = ['localhost:9092'], api_version = (0, 10))
        except Exception as ex:
            print('Erro ao conectar no Kafka')
            print(str(ex))
        finally:
            return _producer

# Cria o objeto
producer_object = kafka_producer()

# Classe para o Streamer
class Data_Streamer():

    # Método construtor
    def __init__(self):

        # Data de início da captura dos dados
        self.start_time = datetime.now() - timedelta(days = 20)

        # Lista de sensores definidos no simulador IoT
        self.sensor_list = ["S1","S11","S12"]

    # Método para o streamer de dados
    def stream_data(self):

        # Conecta no Kafka
        producer_instance = producer_object.connect_kafka_producer()

        # Dicionários de controle
        sensor_id_seconds = {}
        sensor_id_value = {}

        # Loop pela lista de sensores para inicializar os dicionários
        for id in self.sensor_list:
            sensor_id_seconds[id] = 0
            sensor_id_value[id] = 0

        # Variável de controle
        seconds  = 0

        # Aqui fazemos a leitura dos dados de sensores IoT
        # Loop pelo arquivo txt gerado pelo CupCarbon. Vamos abrir o arquivo como csv separado por ;
        with open(init_object.data_path + init_object.data_file) as csv_file:

            # Abre o arquivo para leitura
            csv_reader = csv.reader(csv_file, delimiter = ';')

            # Contadores
            count = 0
            total_seconds = 0

            # Loop
            while (True):

                # Loop pelo arquivo 
                for row in csv.reader(iter(csv_file.readline, '')):

                    # Divisão das linhas
                    if len(row) > 0:
                        line = row[0].strip("\n")

                        # Divisão das colunas
                        if "Time" in line:
                            if ":" in line and " " in line:
                                time_list = line.split(":")[1].split(" ")
                                if len(time_list) > 1:
                                    if "." in time_list[1]:
                                        try:
                                           current_time = float(line.split(":")[1].split(" ")[1])
                                        except:
                                            pass

                    # Gravando a mensagem, imprimindo na tela e gerando o log de saída
                    if ("is writing the message") in line:

                        # Se o sensor estiver na lista de sensores, fazemos a divisão da linha no arquivo
                        if any(sensor in line for sensor in self.sensor_list):
                            sensor_id = line.split(" ")[0]
                            print (sensor_id)

                            # Se o sensor estiver na lista de sensores organiza os dados para publicação no Kafka
                            if sensor_id in self.sensor_list:
                                value_text = line.split(" ")[6]
                                value = value_text.split("#")[-1].strip("\"")
                                sensor_id_seconds[sensor_id] += 0
                                sensor_id_value[sensor_id] = value
                                line_data = sensor_id + ";" +str(seconds) + ";" + str(value)
                                print (line_data)
                                producer_object.publish_message(producer_instance, "sensorData", "data", line_data)
                                logger.info("Mensagem Publicada ", line_data)

# Função main do programa Python
if __name__ == '__main__':
    data_producer_object = Data_Streamer()
    data_producer_object.stream_data()



