from Arq import Arq

#camada de aplicacao
payload = "Qualquer coisa, o Lucas, esqueceu a calculadora"
arq1 = Arq(lambda arg: print(arg),"/dev/pts/9","/dev/pts/10")
arq1.recebe()
