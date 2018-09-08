from PTC.Quadro.src.receptor import Desenquadramento
r = Desenquadramento.Desenquadrador("/dev/pts/6", 9600)
print(r.recebe())