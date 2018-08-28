from PTC.Quadro.src.transmissor import Enquadramento
e = Enquadramento.Enquadramento("/dev/pts/12", 9600)
b = b'~}~a~bcedf}1234567~'
e.transmite(b)
