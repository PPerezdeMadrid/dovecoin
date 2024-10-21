from uuid import uuid4
from flask import Flask, render_template, request, jsonify,redirect, flash
import modules.dovecoinBC as dc
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Dirección del nodo en el puerto 5000
node_address = str(uuid4()).replace('-','')

# Crear un objeto blockchain
blockchain = dc.Blockchain()

"""
#################
    Rutas Básicas
################
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def go_contact():
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def go_register():
    return render_template('register.html')


"""
###################################
    Rutas Funcionalidades Básicas
###################################
"""

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
###############################################
    Rutas Funcionalidades Descentralización
###############################################
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

