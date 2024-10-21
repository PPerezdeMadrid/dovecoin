import datetime
import json
import hashlib
import requests
from urllib.parse import urlparse

class Blockchain:

    # Constructor
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()  # colección por que no hay orden de nodos (obv)
        self.create_block(proof=1, previous_hash='0')
        # proof -→ identificador del bloque

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,  # Así bloque genesis es el 1
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,  # el Nonce!
            'previous_hash': previous_hash,
            'transactions': self.transactions,
        }
        self.transactions = []  # Una vez se mina la transacción, se vacía la memoria de transacciones
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False  # si resuelve el problema criptográfico

        while check_proof is False:
            # No hacer esta operación simétrica!!
            number_new_prev_proof = str(
                (new_proof ** 2 - previous_proof ** 3) ** (1 / 5))  # Num que implique el new proof y el prev proof
            hash_operation = hashlib.sha256(number_new_prev_proof.encode()).hexdigest()

            # Revisar si tiene 4 ceros en las primeras posiciones
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    # Crear el hash de un bloque
    def hash(self, block):
        # json se puede codificar directamente en un formato binario para haslib.sha256
        encoded_block = json.dumps(block,
                                   sort_keys=True).encode()  # 2º arg --> ordenadar alfabéticamente, nos aseguramos que la info viene siempre en el mismo orden (si el orden cambia el hash cambia, efecto avalancha, no nos interesa)
        return hashlib.sha256(encoded_block).hexdigest()

    # Validar el contenido de nuestro bloque es correcto (buen hash)
    #   para cada bloque --> prev_hash = hash bloque anterior y comprobar la proof (nonce, supera la ecuación)
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1  # se irá actualizando y comprobará el 1 con el 2, el 2 con el 3, ...
        while block_index < len(chain):

            # Comprobar los previous hashes
            current_block = chain[block_index]
            if current_block['previous_hash'] != self.hash(previous_block):
                return False

            # Comprobar que el proof (que devuelva 4 ceros)
            previous_proof = previous_block['proof']
            current_proof = current_block['proof']
            # calcular la operación de hash
            number_current_prev_proof = str((current_proof ** 2 - previous_proof ** 3) ** (1 / 5))
            hash_operation = hashlib.sha256(number_current_prev_proof.encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False

            # Actualizar las variables del bucle
            previous_block = current_block
            block_index += 1

        return True

    def add_transaction(self, sender, receiver, amount):  # emisor y receptor se envían dovecoin
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        prev_block = self.get_previous_block()
        return prev_block['index'] + 1  # índice donde aparecerá esa transacción

        # Añadir un nodo

    def add_node(self, address):  # en nuestro caso 'http://127.0.0.1:5000/'
        # url parse procesa urls
        parsed_url = urlparse(address) # ParseResult(scheme='http', netloc='127.0.0.1:5000', path='/', params='', query='', fragment='')
        self.nodes.add(parsed_url.netloc)

    # Protocolo de consenso (apuntes)
    def replace_chain(self): # cambiar la cadena, por ejemplo para actualizar la cadena de bloques
        # Nodo tiene la cadena más larga, llamo a replace_chain para el resto de nodos
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain) # longitud máx es la mía salvo que encuentre otra
        for node in network:
            response = requests.get(f'http://{node}/get_chain') # devuelve chain y length
            if response.status_code==200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain is not None:
            # actualizar mi cadena
            self.chain = longest_chain
            return True
        else:
            return False