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

  def __init__(self, enq, arq, tout):
    poller.Callback.__init__(self, enq._serial, tout)
    self.enq = enq
    self.arq = arq

  def handle(self):
    quadro = self.enq.recebe()
    print("Quadro recebido da Serial:",arq.converte_list(quadro),"\n")
    self.arq.recebe(quadro)

  def handle_timeout(self):
   print("Timeout Serial")
   self.enq.handle_timeout()


tun = Tun("tun0","10.0.0.1","10.0.0.2",mask="255.255.255.252",mtu=1500,qlen=4)
tun.start()

portas = {
	'transmissor':"/dev/pts/9" ,
	'receptor': "/dev/pts/10"
}

arq = Arq(lambda arg: print(arg),portas['receptor'] , portas['transmissor'])
enq = Desenquadramento.Desenquadrador(portas['receptor'], 9600)
cb_enquadramento = CallbackEnq(enq,arq,10)
cb_tun = CallbackTun(tun,1)

sched = poller.Poller()
sched.adiciona(cb_enquadramento)
sched.adiciona(cb_tun)

sched.despache()
