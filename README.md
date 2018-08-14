#Projeto destinado a disciplina de Projeto de Protocolos, onde estudamos os protocolos existentes e projetamos um protocolo próprio ao longo da disciplina
#Autores: Jéssica Hahn, Lucas Thiesen e HelenLuciany

#Etapas:

1 - Enviar e receber dados via serial
2 - Enquadrar os dados recebidos via serial de acordo com o enquadramento do tipo sentinela
	* Tamanho mínimo do campo dado: 8 bytes
	* Tamanho máximo do campo dado: 256 bytes
3 - Calcular CRC e acrescentar ao quadro do item 2.
	* Tamano: 2 bytes
	* Módulo em pyhton: https://pypi.org/project/PyCRC/ 


