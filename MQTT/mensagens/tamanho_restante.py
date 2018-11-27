#!/usr/bin/python3

def get_tamanho_restante(tamanho):
    if(tamanho<=127):
        remainingLength = []
        while(tamanho >0):
            encodedByte = tamanho % 128
            tamanho  = tamanho // 128
            if(tamanho >0):
                encodedByte = encodedByte | 128
            remainingLength.append(encodedByte)
        return bytes(remainingLength)
    else:
        #fazer o outro algoritmo
        pass