from Arq import Arq

#camada de aplicacao
arq1 = Arq(lambda arg: print(arg),"/dev/pts/6","/dev/pts/9")
arq1.recebe()
