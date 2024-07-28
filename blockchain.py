# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 09:36:03 2024

@author: pperezdemadrid
"""

# Cliente HTTP Postman: https://www.getpostman.com/ (descargar app)

import datetime
from flask import Flask, jsonify
import json
import hashlib

# Parte 1: Crear la cadena de bloques
class Blockchain:
    
    # Constructor
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        # proof --> identificador del bloque
        
    def create_block(self, proof, previous_hash):
        block = {
                'index': len(self.chain)+1 , # Así bloque genesis es el 1
                'timestamp': str(datetime.datetime.now()),
                'proof': proof, # el Nonce!
                'previous_hash': previous_hash
            }
            
        self.chain.append(block)
        return block
        
    def get_previous_block(self):
        return self.chain[-1]
    
    # Proof-of-work --> el nonce que los mineros tienen que encontrar
    def proof_of_work(self, previous_proof):
        new_proof = 1 
        check_proof = False # si resuelve el problema criptográfico
        
        while check_proof is False:
            # No hacer esta operación simétrica!!
            number_new_prev_proof = str((new_proof**2 - previous_proof**3)**(1/5)) # Num que implique el new proof y el prev proof 
            
            hash_operation = hashlib.sha256(number_new_prev_proof.encode().hexdigest())
            
            # Revisar si tiene 4 ceros en las primeras posiciones
            if hash_operation[:4] =='0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
        
        
        
# Parte 2 - Minado de un bloque de la cadena


