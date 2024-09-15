"""
@author: pperezdemadrid
Crear una cadena de bloques
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
            hash_operation = hashlib.sha256(number_new_prev_proof.encode()).hexdigest()
            
            # Revisar si tiene 4 ceros en las primeras posiciones
            if hash_operation[:4] =='0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
      
    
    # Crear el hash de un bloque
    def hash(self, block):
        # json se puede codificar directamente en un formato binario para haslib.sha256
        encoded_block = json.dumps(block, sort_keys=True).encode() # 2º arg --> ordenadar alfabéticamente, nos aseguramos que la info viene siempre en el mismo orden (si el orden cambia el hash cambia, efecto avalancha, no nos interesa)
        return hashlib.sha256(encoded_block).hexdigest()
        
        
    # Validar el contenido de nuestro bloque es correcto (buen hash)
    #   para cada bloque --> prev_hash = hash bloque anterior y comprobar la proof (nonce, supera la ecuación)
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1 # se irá actualizando y comprobará el 1 con el 2, el 2 con el 3, ...
        while block_index < len(chain):
            
            # Comprobar los previous hashes
            current_block = chain[block_index]
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            
            # Comprobar que el proof (que devuelva 4 ceros)
            previous_proof = previous_block['proof']
            current_proof = current_block['proof']
            # calcular la operación de hash
            number_current_prev_proof = str((current_proof**2 - previous_proof**3)**(1/5))
            hash_operation = hashlib.sha256(number_current_prev_proof.encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            
            # Actualizar las variables del bucle
            previous_block = current_block
            block_index += 1
            
        return True
            
        
        
# Parte 2 - Minado de un bloque de la cadena

# Crear una aplicación web
app = Flask(__name__)
# Si falla probar con --> app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


# Crear un objeto blockchain
blockchain = Blockchain()

# Minar un bloque
@app.route('/mine_block', methods=['GET'])
def mine_block():
    # 1) Proof of work --> param: previous_proof
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    
    # 2) Crear el bloque --> param: proof y prev hash
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    
    # 3) Mostrar la info en postman
    response = {
        'message': '¡Enhorabuena! Has minado un nuevo bloque',
        'index': block['index'] , # Así bloque genesis es el 1
        'timestamp': block['timestamp'],
        'proof': block['proof'], # el Nonce!
        'previous_hash': block['previous_hash']
        }
    
    return jsonify(response) , 200 # pasarlo a JSON + código

# Obtener la cadena de bloques al completo
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
    return jsonify(response), 200

# implementar "is valid"
@app.route('/is_valid', methods=['GET'])
def is_valid():
    current_chain = blockchain.chain
    is_valid = blockchain.is_chain_valid(current_chain)
    if is_valid:
        response = {'message': 'Todo correcto. La cadena de bloques es válida.'}
    else:
        response = {'message': ' La cadena de bloques no es válida.'}
    return jsonify(response), 200

# Ejecutar la app
app.run(host='0.0.0.0', port=5000, debug=True)

"""
POSTMAN
* GET: http://127.0.0.1:5000/get_chain 
* Respuesta: {
    "chain": [
        {
            "index": 1,
            "previous_hash": "0",
            "proof": 1,
            "timestamp": "2024-07-29 10:22:19.819831"
        }
    ],
    "length": 1
}

* GET: http://127.0.0.1:5000/mine_block
* Respuesta: {
    "index": 2,
    "message": "¡Enhorabuena! Has minado un nuevo bloque",
    "previous_hash": "9e6b9bbeaa51489dc9b59bd9e2ae8d36024ea9c001d47d09932909c9b1af0bc6",
    "proof": 2875,
    "timestamp": "2024-07-29 10:25:56.457138"
}
"""












