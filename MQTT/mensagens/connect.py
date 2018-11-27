#!/usr/bin/python3

from mensagens import tamanho_restante
class Connect:

    def __init__(self):
        # estrutura de um pacote mqtt
        self.pacote = {
            'cabecalho_fixo': None,
            'cabecalho_variavel': None,
            'payload': None
        }


    def mount_message(self):
        nome_protocolo = b'\x00' + b'\x04' + "MQTT".encode('utf-8')
        nivel_protocolo = b'\x04'
        flags = b'\x02'
        keep_alive = b'\x00' + b'\x00'
        self.pacote['cabecalho_variavel'] = nome_protocolo + nivel_protocolo + flags + keep_alive
        cliente_id = "JHL-001".encode('utf-8')
        self.pacote['payload'] = b'\x00' + bytes(bytearray([len(cliente_id)])) + cliente_id
        tamanho_restante_local = tamanho_restante.get_tamanho_restante(len(self.pacote['cabecalho_variavel']+self.pacote['payload']))
        self.pacote['cabecalho_fixo'] =  b'\x10' + tamanho_restante_local

    def get_complete_packet(self):
        if(self.pacote['cabecalho_fixo']==None or self.pacote['cabecalho_variavel']== None or self.pacote['payload']==None):
            print("Pacote Connect Imcompleto ou vazio\n")
            return 0
        else:
            return self.pacote['cabecalho_fixo'] + self.pacote['cabecalho_variavel'] + self.pacote['payload']

    def parse_connack(self,connack):
        #connack have 4 bytes
        controle = connack[0]
        print("Controle:",controle)
        if(controle == 32):
            estado = connack[3]
            print("Estado:",estado)
            if(estado == 0):
                print("Conexão Aceita pelo Broker\n")
                return 1
            else:
                print("Conexão Recusada\n")
                return 0
        else:
            print("Não é um pacote ConnAck\n")
            return 0

