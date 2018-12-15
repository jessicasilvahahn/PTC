from context import mqtt

#1 para armazenar o topico no broker
#0 ou outro valor broker não irá armazenar
core = mqtt.core.core('mqtt.sj.ifsc.edu.br')
if(not core.publish('temperatura/cozinha/', '80',0)):
    print("Error\n")
