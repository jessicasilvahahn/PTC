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
c.parse_connack(data)


topic_name = "sensor/temperatura"
sub.mount_message(topic_name)
pacote_sub = sub.get_complete_packet()
print("Pacote:",pacote_sub)
s.send(pacote_sub)
while(True):
	data = s.recv(BUFFER_SIZE)
	sub.parse_suback(data)


