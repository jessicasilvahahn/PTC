from context import mqtt

core = mqtt.core.core('mqtt.sj.ifsc.edu.br')

def escolhe():
    print("Opções:\n")
    print("1 - Escolher um tópico\n")
    print("2 - Encerrar programa\n")
    op = input("Digite uma opção: ")
    return op

continua = True
while(continua):
    op = escolhe()
    if(str(op)=="1"):
        topico = str(input("Digite o topico: "))
        while(True):
            (r, data) = core.subscribe(topico)
            if (not r):
                print("error\n")
            else:
                print("Data Teste:", data)
    elif (str(op) == "2"):
        continua = False






