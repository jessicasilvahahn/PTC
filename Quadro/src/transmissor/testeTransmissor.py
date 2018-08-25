from Quadro.src.transmissor import Enquadramento
e = Enquadramento.Enquadramento("/dev/pts/15", 9600)
b = b'abcedf1234567'
e.transmite(b)
