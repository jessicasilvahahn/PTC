#!/usr/bin/python3

class Subscribe:

    def __init__(self):
    # estrutura de um pacote mqtt

      self.pacote = {
        'cabecalho_fixo': None,
        'cabecalho_variavel': None,
        'payload': None
        }

    def mount_message(self):
      pass

    def parse_suback(self):
      pass

    def get_complete_packet(self):
      pass

