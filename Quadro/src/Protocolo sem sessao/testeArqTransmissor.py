from Arq import Arq

porta_transmissor = "/dev/pts/4"
porta_receptor = "/dev/pts/4"
payload = "Testand~~}}o..."
arq = Arq(lambda arg: print(arg),porta_transmissor , porta_receptor)
if(arq.envia(payload)==[]):
    print("Estourou quantidade de retransmissões do protocolo")
