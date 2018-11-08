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
    	(proto,payload)= tun.get_frame()
    	print("Bytes Recebidos da Tun:'", proto, payload)
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
    print("Handle Serial")
    quadro = self.enq.recebe()
    print("Quadro recebido da serial:",quadro)
    print("Proto Serial",quadro[1])
    self.arq.recebe(quadro)
    self.arq.proto = quadro[1]
    #enviando quadro recebedido para tun
    self.envia_tun()
    return

  def handle_timeout(self):
   print("Timeout Serial")
   self.enq.handle_timeout()
  
  def envia_tun(self):

  	if(self.arq.proto == b'\x04'):
  		print("aqui")
  		self.arq.proto = 2048 
  	if(self.arq.proto == b'\x06'):
  		self.arq.proto = 34525
  	if(self.arq.proto == b'\x00'):
  		print("Nao enviamos para Tun\n")
  		return
  	if(self.arq.converte_list(self.arq.quadro['payload']) == b''):
  		return
  	
  	print("AVISO: enviando o seguinte quadro recebido para tun: \n",self.arq.converte_list(self.arq.quadro['payload']))
  	#para teste e ver o pacote no wireshark
  	payload = self.arq.converte_list(self.arq.quadro['payload']) 
  	print("payload envia tun",payload,"proto",self.arq.proto)
  	self.tun.send_frame(payload, self.arq.proto)





tun = Tun("tun0","10.0.0.1","10.0.0.2",mask="255.255.255.252",mtu=1500,qlen=4)
tun.start()
#pegando as portas
porta_transmissor = input("Favor digitar a porta serial referente ao transmissor:")
porta_receptor = input("Favor digitar a porta serial referente ao receptor:")


portas = {
	'transmissor': porta_transmissor,
	'receptor': porta_transmissor
}

arq = Arq(lambda arg: print(arg),portas['receptor'] , portas['transmissor'])
enq = Desenquadramento.Desenquadrador(portas['receptor'], 9600)
cb_enquadramento = CallbackEnq(enq,arq,tun,10)
cb_tun = CallbackTun(tun,1)

sched = poller.Poller()
sched.adiciona(cb_enquadramento)
sched.adiciona(cb_tun)

sched.despache()
