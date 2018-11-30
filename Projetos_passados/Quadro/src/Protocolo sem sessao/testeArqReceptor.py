from Arq import Arq

porta_transmissor = "/dev/pts/10"
porta_receptor = "/dev/pts/10"
arq = Arq(lambda arg: print(arg), porta_transmissor, porta_receptor)
while True:
    arq.recebe()


