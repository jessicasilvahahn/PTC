from Arq import Arq

# camada de aplicacao
payload = "Helenluciany"
# Restricao não pode receber bytes
arq2 = Arq(lambda arg: print(arg), "/dev/pts/31", "/dev/pts/31")
arq2.envia(payload)
