#!/usr/bin/python3
from mensagens import connect
from mensagens import publish
from mensagens import subscribe
import socket

c = connect.Connect()
p = publish.Publish()
sub = subscribe.Subscribe()
c.mount_message()
pacote = c.get_complete_packet()
print("Pacote Connect:",pacote)

TCP_IP = 'mqtt.sj.ifsc.edu.br'
TCP_PORT = 1883
BUFFER_SIZE = 2024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(pacote)

data = s.recv(BUFFER_SIZE)


print ("received data:", data)


topic_name = "sensor/temperatura"
valor = "22"
p.mount_message(topic_name,valor)
pacote_publish = p.get_complete_packet()
if(pacote_publish):
    print("Pacote Publish",pacote_publish)
    s.send(pacote_publish)
    s.close()
