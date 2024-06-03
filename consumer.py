# App Python com o Kafka Consumer

# Módulo consumidor para ler os dados do Kafka 

# Instale o Miniconda (se não tiver ainda) e execute no terminal: pip install kafka-python

# Imports
import json
from kafka import KafkaConsumer, KafkaProducer
from Init import Initialize

# Inicializa as configurações
init_object = Initialize()

# Classe do Kafka Consumer
class Data_Consumer():

    # Neste método poderíamos colocar Machine Learning para prever um resultado com base nos dados dos sensores
    def process_sensor_data(self):
        print ("Processando Dados!")

    # Método para obter os dados
    def gather_data(self):

        # Variáveis globais
        global prev_vals
        global main_energy_forecast
        global main_traffic_forecast

        # Consumer
        consumer = KafkaConsumer(auto_offset_reset = 'latest', bootstrap_servers = ['localhost:9092'], api_version = (0, 10), consumer_timeout_ms = 1000)

        # Cria a subscrição para ler somente dados com o texto "sensor"
        consumer.subscribe(pattern='^sensor.*')  

        # Listas de controle
        main_list = []
        main_list_traffic = []

        # Loop
        while True:
            for message in consumer:
                print (message.topic)

                # Verifica o nome do tópico
                if message.topic == "sensorData":

                    # Extrai o valor da mensagem
                    string_val = str(message.value)

                    # Faz o strip por linha
                    string_val = string_val.strip("b'").strip("\n")

                    # Divide a linha por coluna
                    row = string_val.split(";")

                    # Obtém os dados
                    sensor_id = row[0]
                    data = float(row[2])

                    # Dicionário para gravar os dados de saída para análise
                    data_json = {} 

                    # O sensor S1 é a câmera
                    if sensor_id == "S1":
                        data_json["camera_count"] = data

                    # O sensor S11 é o counter
                    elif sensor_id == "S11":
                        data_json["counter"] = data

                    # O sensor S12 é o parking mat
                    elif sensor_id == "S12":
                        data_json["parking_space"] = data
                        print ("Parking ")

                    # Grava a saída em disco no formato JSON
                    with open('json_data.json', 'w') as outfile:
                        json.dump(data_json, outfile)

                  
# Bloco main
if __name__ == '__main__':
    data_consumer = Data_Consumer()
    data_consumer.gather_data()


