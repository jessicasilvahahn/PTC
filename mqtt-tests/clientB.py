import socket

from mqtt.messages import connect
from mqtt.messages import publish
from mqtt.messages import subscribe

c = connect.Connect()
p = publish.Publish()
sub = subscribe.Subscribe()
c.mount_message()
packet = c.get_complete_packet()
print("Pacote Connect:", packet)

TCP_IP = 'mqtt.sj.ifsc.edu.br'
TCP_PORT = 1883
BUFFER_SIZE = 2024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(packet)
data = s.recv(BUFFER_SIZE)
c.parse_connack(data)


topic_name = "sensor/temperatura"
sub.mount_message(topic_name)
packet_sub = sub.get_complete_packet()
print("Pacote:", packet_sub)
s.send(packet_sub)
while(True):
    data = s.recv(BUFFER_SIZE)
    sub.parse_suback(data)
