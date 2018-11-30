#!/usr/bin/python3
from mensagens import tamanho_restante
class Publish:

    def __init__(self):
        # estrutura de um pacote mqtt

        self.pacote = {
            'cabecalho_fixo': None,
            'cabecalho_variavel': None,
            'payload': None
        }

    def mount_message(self,topic_name,topic):
        if( isinstance(topic_name,str) and  isinstance(topic,str)):
            tamanho_topic_name = b'\x00' + bytes(bytearray([len(topic_name)]))
            self.pacote['cabecalho_variavel'] = tamanho_topic_name + topic_name.encode("utf-8")
            self.pacote['payload'] = topic.encode("utf-8")
            tamanho_restante_local = tamanho_restante.get_tamanho_restante(len(self.pacote['cabecalho_variavel'] + self.pacote['payload']))
            self.pacote['cabecalho_fixo'] = b'\x31' + tamanho_restante_local
        else:
            print("Topic Name  ou Topic não são string\n")
            return 0

    #nao tem puback pq ele so esta presente quando qos é 1 ou 2

    def get_complete_packet(self):
        if (self.pacote['cabecalho_fixo'] == None or self.pacote['cabecalho_variavel'] == None or self.pacote[
            'payload'] == None):
            print("Pacote Connect Imcompleto ou vazio\n")
            return 0
        else:
            return self.pacote['cabecalho_fixo'] + self.pacote['cabecalho_variavel']  + self.pacote['payload']
