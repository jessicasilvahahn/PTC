from Arq import Arq

#camada de aplicacao
payload = "Qualquer coisa, o Lucas, esqueceu a calculadora"
arq1 = Arq(lambda arg: print(arg),"/dev/pts/12","/dev/pts/13")
arq1.recebe()
