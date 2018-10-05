from Arq import Arq

# camada de aplicacao
arq1 = Arq(lambda arg: print(arg), "/dev/pts/31", "/dev/pts/31")
arq1.recebe()
