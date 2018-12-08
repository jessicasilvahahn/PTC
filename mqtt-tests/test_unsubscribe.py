from context import mqtt

core = mqtt.core.core('mqtt.sj.ifsc.edu.br')
core.unsubscribe('teste/car')