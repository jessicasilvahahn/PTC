from context import mqtt

core = mqtt.core.core('mqtt.sj.ifsc.edu.br')
if(not core.unsubscribe('teste/testando')):
    print("error\n")