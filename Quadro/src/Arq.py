from PTC.Quadro.src.transmissor import Enquadramento
from PTC.Quadro.src.receptor import Desenquadramento

#quadro arq é o payload do enquadramento
class Arq:
    def __init__(self):
        self.estado = "comunicando"
        self.m = False
        self.n = False
        self.quadro_recebido = None
        self.payload = None


    def MefArq(self):

        if (self.estado == "comunicando"):
            if (self.payload):
                self.envia()
                self.estado = "aguardandoAck"
                return
            if (self.quadro_recebido):
                if (self.m == self.extrai_sequencia()):
                    self.extrai_payload()
                    self.confirma()
                    self.m = not self.m
                elif (not self.m == self.extrai_sequencia()):
                    self.confirma()
                self.estado = "comunicando"
                return
        if (self.estado == "aguardandoAck"):
            if (self.quadro_recebido):
                if (self.m == self.extrai_sequencia()):
                    self.extrai_payload()
                    self.confirma()
                    self.m = not self.m
                elif (not self.m == self.extrai_sequencia()):
                    self.confirma()
                self.estado = "aguardandoAck"
                return
            if (self.ack == self.extrai_ack()):
                if (not self.n == self.extrai_sequencia()):
                    self.envia()
                    self.setTimerOut()
                    self.estado = "aguardandoAck"
                if (self.n == self.extrai_sequencia()):
                    self.n = not self.n
                    self.estado = "comunicando"
                return

    def setTimerOut(self):
        pass

    # retira bit 7 do byte de controle pra verificar se eh ACK ou DATA
    def extrai_ack(self):
        pass

    #montar quadro arq
    def envia(self):
        pass

    #envia ack
    def confirma(self):
        pass

    #extrai o payload do quadro
    def extrai_payload(self):
        #considerando que quadro é [] e tem controle(1byte) + proto(1byte) + payload + crc
        self.quadro_recebido = []
        self.payload = self.quadro_recebido[2:-2]
        return


    #extrai sequencia do byte de controle do quadro arq
    def extrai_sequencia(self):
        sequencia = self.quadro_recebido[0]
        #ascii - 48 - bit 0 e 14 bit 1
        bit_list = list(sequencia)
        sequencia = bit_list[4]
        if(sequencia==48):
            return False
        elif(sequencia==49):
            return True

