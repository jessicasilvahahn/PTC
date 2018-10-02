from Arq import Arq

porta_transmissor = "/dev/pts/12"
porta_receptor = "/dev/pts/11"
payload = "~Qualquer coisa, o Lucas, esqueceu a calculadora~"
arq = Arq(lambda arg: print(arg),porta_transmissor , porta_receptor)
print(arq.envia(payload))
