from Arq import Arq

#camada de aplicacao
payload = "Qualquer coisa, o Lucas, esqueceu a calculadora"
arq2 = Arq(lambda arg: print(arg),"/dev/pts/13","/dev/pts/12")
arq2.envia(payload)