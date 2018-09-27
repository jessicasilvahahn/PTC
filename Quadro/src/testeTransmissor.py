import Enquadramento
e = Enquadramento.Enquadramento("/dev/pts/9", 9600)
b = b'~zabx123456~'
print(type(b))
e.transmite(b)
