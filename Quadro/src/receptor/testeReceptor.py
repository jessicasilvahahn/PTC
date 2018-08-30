from PTC.Quadro.src.receptor import Desenquadramento
r = Desenquadramento.Desenquadrador("/dev/pts/8", 9600)
print(r.recebe())