from Arq import Arq

# camada de aplicacao
arq1 = Arq(lambda arg: print(arg), "/dev/pts/3", "/dev/pts/3")
arq1.recebe()
