import serial


#testando máquina de recepcao
s = serial.Serial("/dev/pts/15")
print(s.name)
b = b'~abcedf1234567~'
s.write(b)
s.close()