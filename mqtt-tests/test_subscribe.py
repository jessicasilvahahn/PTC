from context import mqtt

core = mqtt.core.core('mqtt.sj.ifsc.edu.br')
topico = "temperatura/cozinha/"

while(True):
   (r, data) = core.subscribe(topico)
   if (not r):
      print("error\n")
   else:
      print("Data Teste:", data)

