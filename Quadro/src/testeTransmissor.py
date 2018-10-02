import Enquadramento
e = Enquadramento.Enquadramento("/dev/pts/10", 9600)
b = b'~zabx123456~'
print(type(b))
e.transmite(b)
