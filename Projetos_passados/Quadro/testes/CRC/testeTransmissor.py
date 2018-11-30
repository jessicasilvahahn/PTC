import Enquadramento

porta = input("Digite a porta serial gerada pelo serialemu: ")
e = Enquadramento.Enquadramento(porta, 9600)
payload = input("Digite uma informação: ")
bytes = bytes(payload, 'utf-8')
e.transmite(bytes)
