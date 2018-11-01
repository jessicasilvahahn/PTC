#!/usr/bin/python3
from tun import Tun
from Arq import Arq
import Desenquadramento
import poller
import pickle

class CallbackTun(poller.Callback):
    
    def __init__(self, tun, tout):
        poller.Callback.__init__(self, tun.fd, tout)
        self._tun = tun
     
    def handle(self):
        proto, payload= tun.get_frame()
        print("Bytes Recebidos da Tun:",payload)
        print("prot:%s" % hex(proto))
        arq.envia(proto,payload)
        
    def handle_timeout(self):
        print('Timeout Tun!')

class CallbackEnq(poller.Callback):

  def __init__(self, enq, arq, tun, tout):
    poller.Callback.__init__(self, enq._serial, tout)
    self.enq = enq
    self.arq = arq
    self.tun = tun

  def handle(self):
    quadro = self.enq.recebe()
    print("Quadro recebido da Serial:",arq.converte_list(quadro), "tamanho",len(arq.converte_list(quadro)),"\n")
    self.arq.recebe(quadro)
    #enviando quadro recebedido para tun
    self.envia_tun()

  def handle_timeout(self):
   print("Timeout Serial")
   self.enq.handle_timeout()
  
  def envia_tun(self):

    if(self.arq.proto == b'\x04'):
  	    self.arq.proto = 0x800
    elif(self.arq.proto == b'\x06'):
        self.arq.proto = 0x86dd
    else:
        self.arq.proto = 0x000
    if(self.arq.converte_list(self.arq.quadro['payload']) == b''):
        pass
    else:
        print("AVISO: enviando o seguinte quadro recebido para tun: \n",self.arq.converte_list(self.arq.quadro['payload']))
        #para teste e ver o pacote no wireshark
        payload = self.arq.converte_list(self.arq.quadro['payload'])
        self.tun.send_frame(payload,self.arq.proto)





tun = Tun("tun0","10.0.0.1","10.0.0.2",mask="255.255.255.252",mtu=1500,qlen=4)
tun.start()
#pegando as portas
loop = True
while(loop):
	porta_transmissor = input("Favor digitar a porta serial referente ao transmissor:")
	porta_receptor = input("Favor digitar a porta serial referente ao receptor:")
	if(porta_receptor!=porta_transmissor):
		loop = False
	else:
		print("\n Obs: Favor digitar portas diferentes para o transmissor e receptor\n")

portas = {
	'transmissor': porta_transmissor,
	'receptor': porta_receptor
}

arq = Arq(lambda arg: print(arg),portas['receptor'] , portas['transmissor'])
enq = Desenquadramento.Desenquadrador(portas['receptor'], 9600)
cb_enquadramento = CallbackEnq(enq,arq,tun,10)
cb_tun = CallbackTun(tun,1)

sched = poller.Poller()
sched.adiciona(cb_enquadramento)
sched.adiciona(cb_tun)

sched.despache()
