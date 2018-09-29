from Arq import Arq

#camada de aplicacao
payload = "~Qualquer coisa, o Lucas, esqueceu a calculadora~"
#Restricao não pode receber bytes
arq2 = Arq(lambda arg: print(arg),"/dev/pts/6","/dev/pts/9")
arq2.envia(payload)