# Projeto da Disciplina de Protocolo

Onde estudamos os protocolos existentes e projetamos um protocolo próprio ao longo da disciplina. Etapas.


  - Enviar e receber dados via serial
  - Enquadrar os dados recebidos via serial de acordo com o enquadramento do tipo sentinela. Tamanho mínimo do campo dado: 8 bytes.Tamanho máximo do campo dado: 256 bytes
  -  Calcular CRC e acrescentar ao quadro do item 2. Tamanho do campo CRC: 2 bytes. Módulo em pyhton: https://pypi.org/project/PyCRC/

#Falta implementar 
 - Terminar Transmissão ARQ
 - Verificar CRC no ARQ
 - Aplicar retransmissão de quadro (quadro vazio vindo do desenquadra ou quando vim quadro com erro)
 - Tratar a tamanho máximo do payload, não podendo ultrapassar 256 bytes
 - Aplicar timeout no ARQ
 - Tratar o enquadramento e desenquadramento a nível de transmissor e receptor, pois quando estiver em receptor ou transmissor terá um comportamento diferente



