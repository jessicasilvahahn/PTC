from Arq import Arq

#camada de aplicacao
payload = "ooo"
arq2 = Arq(lambda arg: print(arg),"/dev/pts/10","/dev/pts/9")
arq2.envia(payload)