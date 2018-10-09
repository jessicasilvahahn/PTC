from Arq import Arq

porta_transmissor = "/dev/pts/6"
porta_receptor = "/dev/pts/6"
arq = Arq(lambda arg: print(arg), porta_transmissor, porta_receptor)
while True:
    arq.recebe()


