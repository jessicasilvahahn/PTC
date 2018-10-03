from Protocolo import Protocolo

porta_transmissor = "/dev/pts/14"
porta_receptor = "/dev/pts/17"
proto = Protocolo(lambda arg: print(arg), porta_transmissor, porta_receptor)
proto.recebe()
