from Arq import Arq

porta_transmissor = "/dev/pts/11"
porta_receptor = "/dev/pts/10"
payload = "~Testando~"
arq = Arq(lambda arg: print(arg),porta_transmissor , porta_receptor)
if(arq.envia(payload)==[]):
    print("Estourou quantidade de retransmissões do protocolo")
