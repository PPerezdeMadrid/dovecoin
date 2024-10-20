from flask import Flask, render_template, jsonify,request
import datetime
import json
import hashlib
import requests
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect, flash
# import doveCoin as dc

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

"""
#################
    Rutas
################
"""  
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def go_contact():
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        email = request.form['email']
        message_body = request.form['message']

        # Prepare the email message
        msg = Message(f'New Contact Form Submission from {name}',
                      recipients=['your-email@example.com'])  # Your email
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message_body}"

        try:
            # Send the email
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            # Handle any errors in sending the email
            flash(f'Error sending email: {str(e)}', 'danger')
        
        # Redirect to the contact page after form submission
        return redirect('/contact')
    
    # If GET request, just render the form
    return render_template('contact.html')



# Dirección del nodo en el puerto 5000
node_address = str(uuid4()).replace('-','')

# Crear un objeto blockchain
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    userEmail = "Paloma PML" # CAMBIAR!!!!
    print("Entra en la función mine_block")
    # 1) Proof of work --> param: previous_proof
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)

    # 2) Crear el bloque --> param: proof y prev hash
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address, receiver = userEmail, amount=0)
    block = blockchain.create_block(proof, previous_hash)

    # 3) Mostrar la info en postman
    response = {
        'message': 'Congratulations! You have just mined a block',
        'index': block['index'],  # Así bloque genesis es el 1
        'timestamp': block['timestamp'],
        'proof': block['proof'],  # el Nonce!
        'previous_hash': block['previous_hash'],
        'transactions': block['transactions'],
    }
    print(response)

    # return jsonify(response), 200  # pasarlo a JSON + código
    return render_template('mineBlock.html', data=response), 200

# Obtener la cadena de bloques al completo
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    print(response)
    # return jsonify(response), 200
    return render_template('getChain.html', data=response), 200

# implementar "is valid"
@app.route('/is_valid', methods=['GET'])
def is_valid():
    current_chain = blockchain.chain
    is_valid = blockchain.is_chain_valid(current_chain)
    if is_valid:
        response = {'message': 'Todo correcto. La cadena de bloques es válida.'}
    else:
        response = {'message': 'La cadena de bloques no es válida.'}
    # return jsonify(response), 200
    return render_template('isValid.html', data=jsonify(response)), 200

# Ir a hacer una transacción
@app.route('/GoTransaction')
def go_transaction():
    return render_template('addTransaction.html')

# añadir una nueva transacción a la cadena de bloques
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']

    if not all([sender, receiver, amount]):  
        return 'Error, some transaction elements are missing', 400
        
    index = blockchain.add_transaction(sender, receiver, amount)
    response = {'message': f'The transaction will be added to block {index}'}
    
    # return jsonify(response) , 201 # Código "Created"
    return render_template('addTransaction.html', data=response), 200

"""
Descentralizar el bloque
"""

# Conectar nodos
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json() # {'nodes': ['127.0.0.1:5001', '127.0.0.1:5002',...]}
    nodes = json.get('nodes')
    # Comprobaciones previas
    if nodes is None:
        return f'No hay nodos para añadir', 400
    # Recorrer los nodos y darlos de alta
    for node in nodes:
        blockchain.add_node(node)

    response = {
                'message': 'Todos los nodos han sido conectados. La cadena de DoveCoin contiene los nodos siguientes: ',
                'total_nodes': list(blockchain.nodes)
                }
    # return jsonify(response), 201
    return render_template('connectNode.html', data=jsonify(response)), 200

# Reemplazar cadena por la cadena más larga (si es necesario)
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    replace_chain = blockchain.replace_chain() # True or not
    if replace_chain:
        response = {
            'message': 'Los nodos tenían diferentes cadenas y han sido reemplazadas por la más larga',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Todo correcto, la cadena en todos los nodos ya es la más larga',
            'actual_chain': blockchain.chain
        }
    # return jsonify(response), 200
    return render_template('isValid.html', data=jsonify(response)), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # app.run(host='0.0.0.0', port=5001, debug=True)

