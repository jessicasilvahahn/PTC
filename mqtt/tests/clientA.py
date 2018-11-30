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

print("received data:", data)

topic_name = "sensor/temperatura"
valor = "22"
p.mount_message(topic_name, valor)
packet_publish = p.get_complete_packet()
if(packet_publish):
    print("Pacote Publish", packet_publish)
    s.send(packet_publish)
    s.close()
