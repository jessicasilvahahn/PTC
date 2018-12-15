from context import mqtt

core = mqtt.core.core('mqtt.sj.ifsc.edu.br')

def sub():
    (r, data) = core.subscribe("temperatura/cozinha/")
    return (r,data)
def loop():
    while (True):
        (r, data) = sub()
        if (not r):
            print("error\n")
        else:
            if (core.get_pulish_received()):
                print("Data Received Publish:", data)
                break
    if (not core.unsubscribe('temperatura/cozinha/')):
        print("error\n")


loop()


