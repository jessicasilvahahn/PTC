from Arq import Arq

# camada de aplicacao
payload = "~Qualquer coisa, o Lucas, esqueceu a calculadora~"
# Restricao não pode receber bytes
arq2 = Arq(lambda arg: print(arg), "/dev/pts/2", "/dev/pts/2")
arq2.envia(payload)
