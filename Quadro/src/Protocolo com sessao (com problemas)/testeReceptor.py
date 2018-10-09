from Arq import Arq

porta_transmissor = "/dev/pts/9"
porta_receptor = "/dev/pts/9"
arq = Arq(lambda arg: print(arg), porta_transmissor, porta_receptor)
arq.recebe()


