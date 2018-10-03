from Protocolo import Protocolo

porta_transmissor = "/dev/pts/16"
porta_receptor = "/dev/pts/15"
payload = "~Qualquer coisa, o Lucas, esqueceu a calculadora~"
proto = Protocolo(lambda arg: print(arg),porta_transmissor , porta_receptor)
proto.conectar()
proto.recebe()
