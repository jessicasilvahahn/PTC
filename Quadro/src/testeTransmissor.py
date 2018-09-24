import Enquadramento
e = Enquadramento.Enquadramento("/dev/pts/14", 9600)
b = b'~zabx123456~'
e.transmite(b)
