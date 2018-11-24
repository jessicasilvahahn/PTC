import asyncio
import socket

def toInt(hex): return int.from_bytes(hex, byteorder='big')

class Mensagens:
    def __init__(self):
        #estrutura de um pacote mqtt
        self.pacote = {
            'cabecalho_fixo': None,
            'cabecalho_variavel': None,
            'payload': None
        }

    def connect(self):
        #cabecalho variavel
        #protocol name (6 bytes)
        byte1_variavel = b'\x00'
        byte2_variavel = b'\x04'
        nome_protocolo = byte1_variavel + byte2_variavel + "MQTT".encode('utf-8')
        nivel_protocolo = b'\x04'
        flags = b'\x02'
        keep = b'\x00' + b'\x00'
        cabecalho_variavel = nome_protocolo + nivel_protocolo + flags + keep
        #print("Cabeçalho Variável",cabecalho_variavel)
        tamanho_cabecalho_variavel = len(cabecalho_variavel)
        tamanho_restante = self.get_tamanho_restante(tamanho_cabecalho_variavel)
        #print("Tamanho Normativa",tamanho_restante)

        # cabecalho fixo
        # 2 bytes (cabecalho fixo = MQTT Control Packet type  + Flags specific to each MQTT Control Packet type + Remaining Length)
        # 16 - 00010000
        cabecalho_fixo = b'\x10' + tamanho_restante
        #print("Cabeçaho Fixo", cabecalho_fixo)
        pacote_connect = cabecalho_fixo + cabecalho_variavel
        print("Pacote connect",pacote_connect)
        return pacote_connect


    def get_tamanho_restante(self,tamanho):
        remainingLength = []
        while(tamanho>0):
            encodedByte = tamanho % 128
            tamanho  = tamanho // 128
            if(tamanho>0):
                encodedByte = encodedByte | 128
            remainingLength.append(encodedByte)
            #print("EncodedByte",encodedByte)
        return bytes(remainingLength)

    def normativa_2(self,X):
        multiplier = 1
        value = 0
        encodedByte = 'next byte from stream'
        while((encodedByte & 128) != 0):
            value += (encodedByte & 127)*multiplier
            multiplier *= 128
            if((multiplier > 128*128*128)):
                print("Má formação do cabeçalho restante\n")
                return 0

            print("Value",value)
            return value

#loop = asyncio.get_event_loop()
#Teste connect
m = Mensagens()
pacote = m.connect()

#loop = asyncio.get_event_loop()

#reader, writer = asyncio.streams.open_connection(host='mqtt.sj.ifsc.edu.br', port=1883)

#loop.run_until_complete()
#loop.close()


TCP_IP = 'mqtt.sj.ifsc.edu.br'
TCP_PORT = 1883
BUFFER_SIZE = 2024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(pacote)

data = s.recv(BUFFER_SIZE)
s.close()

print ("received data:", data)