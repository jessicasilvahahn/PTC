from PTC.Quadro.src.transmissor import Enquadramento
e = Enquadramento.Enquadramento("/dev/pts/4", 9600)
b = b'zabcedf}1234567~'
e.transmite(b)
