from flask import Flask, render_template, jsonify,request, flash, redirect, url_for, send_file, session
from uuid import uuid4
from doveCoin import Blockchain

app = Flask(__name__)

# Dirección del nodo en el puerto 5000
node_address = str(uuid4()).replace('-','')

# Crear un objeto blockchain
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    # 1) Proof of work --> param: previous_proof
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)

    # 2) Crear el bloque --> param: proof y prev hash
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address, receiver = "Paloma PML", amount=50)
    block = blockchain.create_block(proof, previous_hash)

    # 3) Mostrar la info en postman
    response = {
        'message': '¡Enhorabuena! Has minado un nuevo bloque',
        'index': block['index'],  # Así bloque genesis es el 1
        'timestamp': block['timestamp'],
        'proof': block['proof'],  # el Nonce!
        'previous_hash': block['previous_hash'],
        'transactions': block['transactions'],
    }

    # return jsonify(response), 200  # pasarlo a JSON + código
    return render_template('mineBlock.html', data=jsonify(response)), 200

# Obtener la cadena de bloques al completo
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    # return jsonify(response), 200
    return render_template('mineBlock.html', data=jsonify(response)), 200

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


# añadir una nueva transacción a la cadena de bloques
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json() #obtener json a través de la petición
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys): # Para cada clave de transaction key están en json?
        return 'Error, faltan algunos elementos de la transacción' , 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message' : f'La transacción será añadida al bloque {index}',}
    # return jsonify(response) , 201 # Código "Created"
    return render_template('isValid.html', data=jsonify(response)), 200

"""
Descentralizar el bloque
"""



@app.route('/')
def index():
    return render_template('indexFull.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
