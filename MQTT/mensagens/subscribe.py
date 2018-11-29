#!/usr/bin/python3
from mensagens import tamanho_restante

class Subscribe:

    def __init__(self):
    # estrutura de um pacote mqtt

      self.pacote = {
        'cabecalho_fixo': None,
        'cabecalho_variavel': None,
        'payload': None
        }

    def mount_message(self,topic_name):
        if (isinstance(topic_name, str)):
            self.pacote['cabecalho_fixo'] = b'\x82'
            packet_identifier = b'\x00' + b'\x00'
            qos = b'\x00'
            tamanho_topic_name = b'\x00' + bytes(bytearray([len(topic_name)]))
            self.pacote['payload'] = tamanho_topic_name + topic_name.encode('utf-8') + qos
            self.pacote['cabecalho_variavel'] = packet_identifier
            tamanho_restante_local = tamanho_restante.get_tamanho_restante(len(self.pacote['cabecalho_variavel'] + self.pacote['payload']))
            self.pacote['cabecalho_fixo'] = self.pacote['cabecalho_fixo'] + tamanho_restante_local



    def parse_suback(self):
      pass

    def get_complete_packet(self):
        if (self.pacote['cabecalho_fixo'] == None or self.pacote['cabecalho_variavel'] == None or self.pacote[
            'payload'] == None):
            print("Pacote Connect Imcompleto ou vazio\n")
            return 0
        else:
            return self.pacote['cabecalho_fixo'] + self.pacote['cabecalho_variavel']  + self.pacote['payload']

