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
    	print("Bytes Recebidos da Tun:",payload)
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
    print("Quadro recebido da Serial:",quadro)
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
  		self.arq.proto = 2048 
  	elif(self.arq.proto == b'\x06'):
  		self.arq.proto = 34525
  	elif(self.arq.proto == b'\x00'):
  		return
  	elif(self.arq.converte_list(self.arq.quadro['payload']) == b''):
  		return
  	else:
  		return

  	print("AVISO: Enviando o seguinte quadro recebido para tun: \n",self.arq.converte_list(self.arq.quadro['payload']))
  	payload = self.arq.converte_list(self.arq.quadro['payload']) 
  	self.tun.send_frame(payload, self.arq.proto)




tun_name = input("Favor digitar o nome da interface tun:")
ip_v4_origem = input("Favor digitar o ipv4 de origem:")
ip_v4_destino =  input("Favor digitar o ipv4 de destino:")
print("\nAVISO: Não estamos fazendo a verificação do IPv6, favor digitá-los corretamente\n")
print("O Ipv6 exemplo: 2801::3\n")
ip_v6_origem = input("Favor digitar o ipv6 de origem:")
ip_v6_destino =  input("Favor digitar o ipv6 de destino:")



tun = Tun(tun_name,ip_v4_origem,ip_v4_destino,ip_v6_origem,ip_v6_destino,mask="255.255.255.252",mtu=1500,qlen=4)
tun.start()
#pegando as portas
porta_transmissor = input("Favor digitar a porta serial referente ao transmissor:")
porta_receptor = input("Favor digitar a porta serial referente ao receptor:")


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
