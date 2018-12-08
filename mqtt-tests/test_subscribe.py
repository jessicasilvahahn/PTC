from context import mqtt

core = mqtt.core.core('mqtt.sj.ifsc.edu.br')
#core.subscribe('random/topic')
core.subscribe('teste/testando')