import Desenquadramento
porta = input("Digite a porta serial gerada pelo serialemu: ")
r = Desenquadramento.Desenquadrador(porta, 9600)
print(r.recebe())
