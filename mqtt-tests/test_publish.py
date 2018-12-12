from context import mqtt

core = mqtt.core.core('mqtt.sj.ifsc.edu.br')
if(not core.publish('teste/testando', 'jessica')):
    print("Error\n")
