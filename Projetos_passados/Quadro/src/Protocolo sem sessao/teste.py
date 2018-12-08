#!/usr/bin/python3

from Arq import Arq
import sys

try:
  f = open(sys.argv[1])
except:
  print('Uso: %s nome_arquivo' % sys.argv[0])
  sys.exit(0)

porta_transmissor = "/dev/pts/10"
porta_receptor = "/dev/pts/10"
payload = "Testand~~}}o..."
arq = Arq(lambda arg: print(arg),porta_transmissor , porta_receptor)

while True:
  l = f.readline()
  if not l: break
  if (arq.envia(l)==[]):
    print("Estourou quantidade de retransmissões do protocolo")
    break
  else:
    print('enviou:', l, end='')
