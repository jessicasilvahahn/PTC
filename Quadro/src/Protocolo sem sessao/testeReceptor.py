from Arq import Arq

porta_transmissor = "/dev/pts/7"
porta_receptor = "/dev/pts/7"
arq = Arq(lambda arg: print(arg), porta_transmissor, porta_receptor)
arq.recebe()


