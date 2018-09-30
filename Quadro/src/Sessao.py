from Arq import Arq


class Sessao:
    def __init__(self, tratadorAplicacao, portaReceptor, portaTransmissor):
        self.estado = 'Desconectado'
        self.tratadorAplicacao = tratadorAplicacao
        self.canal = Arq(self._trataDadoRecebido,
                         portaReceptor, portaTransmissor)
        self.conectado = False
        self.idSessao = -1
        # só será utilizado quando integrado ao linux
        self.manterConexao = False

    def _tratadorRecebimento(self, mensagem):
        if (mensagem == None):
            self._controladorSessao('timeout')
        else:
            evento = self._identificaEvento(mensagem)
            self.mensagemRecebida = mensagem
            self._controladorSessao(evento)

    def _controladorSessao(self, evento):
        if (self.estado == 'Desconectado'):
            if (evento == 'conectando'):
                self._enviaPedidoConexao()
                self.estado = 'Handshake enviado'
            if (evento == 'conexao recebida'):
                self._confirmaConexao()
                self.estado = 'Handshake enviado'

        if (self.estado == 'Handshake enviado'):
            if (evento == 'erro'):
                self._retornaEstadoInicial()
            if (evento == 'timeout'):
                self._enviaPedidoConexao()
            if (evento == 'confirmacao recebida'):
                self._enviaDado()
                self.estado = 'conectado'

        if (self.estado == 'Handshake recebido'):
            if (evento == 'timeout'):
                self._retornaEstadoInicial()
            if (evento == 'mensagem recebida'):
                self.estado = 'conectado'
                self._trataDadoRecebido()

        if (self.estado == 'conectado'):
            if (evento == 'enviando desconexao'):
                self._enviaPedidoDesconexao()
                self.estado = 'half-closed enviado'
            if (evento == 'desconexao recebida'):
                self._enviaPedidoDesconexao()
                self.estado = 'half-closed recebido'
            if (evento == 'enviar mensagem'):
                self._enviaDado()
            if (evento == 'mensagem recebida'):
                self._trataDadoRecebido()

        if (self.estado == 'half-closed recebido'):
            if (evento == 'desconexao recebida'):
                self._enviaPedidoDesconexao()
            if (evento == 'desconexao confirmada'):
                self._retornaEstadoInicial()
            if (evento == 'timeout'):
                self._retornaEstadoInicial()

        if (self.estado == 'half-closed enviado'):
            if (evento == 'mensagem recebida'):
                self._trataDadoRecebido()
            if (evento == 'timeout'):
                self._enviaPedidoDesconexao()
            if (evento == 'desconexao recebida'):
                self._confirmaDesconexao()
                self._retornaEstadoInicial()
            if (evento == 'erro'):
                self._retornaEstadoInicial()

    def _enviaPedidoConexao(self):
        quadro = [self.idSessao, b'\xff', b'\x00']
        self.canal.envia(quadro)

    def _confirmaConexao(self):
        quadro = [self.idSessao, b'\xff', b'\x01']
        self.canal.envia(quadro)

    def _enviaDado(self):
        quadro = [self.idSessao, b'\x00'] + list(self.payload)
        self.canal.envia(quadro)

    def _trataDadoRecebido(self):
        payload = self.mensagemRecebida[2:]
        self.tratadorAplicacao(payload)

    def _enviaPedidoDesconexao(self):
        quadro = [self.idSessao, b'\xff', b'\x04']
        self.canal.envia(quadro)

    def _confirmaDesconexao(self):
        quadro = [self.idSessao, b'\xff', b'\x05']
        self.canal.envia(quadro)

    def _retornaEstadoInicial(self):
        self.estado = 'Desconectado'
        self.conectado = False
        self.idSessao = -1
        self.manterConexao = False

    def _identificaEvento(self, mensagem):
        proto = mensagem[1]
        if (proto == b'\x00'):
            return 'mensagem recebida'
        elif (proto == b'\xff'):
            tipo = mensagem[2]
            if (tipo == b'\x00'):
                return 'conexao recebida'
            if (tipo == b'\x01'):
                return 'confirmacao recebida'
            if (tipo == b'\x04'):
                return 'desconexao recebida'
            if (tipo == b'\x05'):
                return 'desconexao confirmada'
        return 'erro'

# interface para o gerenciamento de sessão pelo protocolo

    def conectar(self):
        if (not self.conectado):
            self._controladorSessao('conectando')
            self.conectado = True

    def desconectar(self):
        if (self.conectado):
            self._controladorSessao('enviando desconexao')
            self.conectado = False

    def enviar(self, payload):
        if (not self.conectado):
            self.conectar()
        self.payload = payload
        self._controladorSessao('enviar mensagem')

    def receber(self):
        self.canal.recebe()
