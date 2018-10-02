from Arq import Arq

porta_transmissor = "/dev/pts/10"
porta_receptor = "/dev/pts/13"
arq = Arq(lambda arg: print(arg), porta_transmissor, porta_receptor)
arq.recebe()
