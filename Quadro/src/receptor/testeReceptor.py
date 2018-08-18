import serial


#testando máquina de recepcao
s = serial.Serial("/dev/pts/11")
print(s.name)
b = b'~abcedf1234567~~abcedf}}^1234567~~abcedf012}]9876~~}]}^}]}]}]}^}^}^}]}]}]~'
s.write(b)
s.close()