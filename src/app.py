from uuid import uuid4
from flask import Flask, render_template, request, jsonify,redirect, flash, session,  url_for
import modules.dovecoinBC as dc
from flask_sqlalchemy import SQLAlchemy
from modules.users import Client, get_user_by_email, db, create_database, get_all_nodes, ConnectedNode
import argparse


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key ='dovecoin'
ADMIN_PASSWD = "DoveCoin1234+"

# Inicializar la base de datos
db.init_app(app)

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

@app.route('/blog', methods=['GET', 'POST'])
def go_blog():
    return render_template('blog.html')


"""
###################################
    Rutas Funcionalidades Básicas
###################################
"""

# FALTA: Manejo errores!
@app.route('/registerClient', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        node = request.form['node']

        data = {
            'name': str(name),
            'email': str(email),
            'node': str(node)
        }

        print("\033[1;32mClient Data:\033[0m")
        print("\033[1;34m-----------------\033[0m")
        for key, value in data.items():
            print(f"\033[1;36m{key.capitalize()}:\033[0m \033[1;37m{value}\033[0m")
        print("\033[1;34m-----------------\033[0m")

        # Imprimir todos los clientes:
        existing_clients = Client.query.all()  # Obtener todos los clientes
        print("\033[1;33mExisting Clients' Emails:\033[0m")
        for client in existing_clients:
            print(f"\033[1;35m{client.email}\033[0m")

        new_client = Client(name=name, email=email, password=password, node=node)

        db.session.add(new_client)
        db.session.commit()

        # Flash success message and redirect
        flash('Client registered successfully!')
        print("==> Cliente Registrado: " + str(name) + ", "+ str(email))
        return render_template('profile.html', data=data)

    return render_template('register.html')

@app.route('/go_profile', methods=['GET'])
def go_profile():
    # Verificar si el usuario está en la sesión
    if 'user_id' in session:
        # Obtener los datos del usuario desde la sesión
        user_data = {
            'id': session['user_id'],
            'name': session['user_name'],
            'email': session['user_email'],
            'node': session['user_node']
        }
        return render_template("profile.html", data=user_data)
    else:
        # Si no hay usuario en la sesión, redirigir al login o home
        flash('You must be logged in to view your profile.', 'danger')
        return redirect(url_for('home'))



@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('passwd')

    # Suponiendo que get_user_by_email() devuelve un objeto usuario o None
    user = get_user_by_email(email)

    if user:
        if user.password == password:
            # Guardamos los datos del usuario en la sesión
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['user_node'] = user.node
            
            flash('Successfully logged in!', 'success')
            print("Inicio sesión exitoso")
            return render_template("profile.html", data=user)  # `data` se usa para mostrar datos en el perfil
        else:
            flash('Incorrect password. Please try again.', 'danger')
            print("Incorrect Passwd")
            return redirect(url_for('home'))
    else:
        flash('Email not found. Please try again.', 'danger')
        return redirect(url_for('home'))


@app.route('/mine_block_ajax', methods=['GET'])
def mine_block_ajax():
    userEmail = "Empty Transaction"  # CAMBIAR!!!!
    print("Entra en la función mine_block")
    # 1) Proof of work --> param: previous_proof
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)

    # 2) Crear el bloque --> param: proof y prev hash
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address, receiver=userEmail, amount=0)
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

    return jsonify(response), 200  # pasarlo a JSON + código

# Obtener la cadena de bloques al completo
@app.route('/see_chain', methods=['GET'])
def see_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    print(response)
    # return jsonify(response), 200
    return render_template('getChain.html', data=response), 200

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
        response = {'message': 'Everything is correct. The blockchain is valid..'}
    else:
        response = {'message': 'The blockchain is not valid.'}
    # return jsonify(response), 200
    return render_template('isValid.html', data=jsonify(response)), 200

# Ir a hacer una transacción
@app.route('/GoTransaction')
def go_transaction():
    return render_template('addTransaction.html')


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']

    if not all([sender, receiver, amount]):
        return jsonify({'message': 'Error, some transaction elements are missing'}), 400

    index = blockchain.add_transaction(sender, receiver, amount)
    response = {'message': f'The transaction will be added to block {index}'}

    return jsonify(response), 200  # Código "OK"


"""
###############################################
    Rutas Funcionalidades Descentralización
###############################################
"""

# Conectar nodos
@app.route('/connect_node', methods = ['POST', 'GET'])
def connect_node():
    ip = session.get('user_node')
    print("IP del cliente: " + str(ip))
    if ip:
        existing_node = ConnectedNode.query.filter_by(ip_address=ip).first()
        print("Existing node: " + str(existing_node))
        if not existing_node:
            # Crear y añadir la nueva conexión
            new_node = ConnectedNode(ip_address=ip)
            db.session.add(new_node)
            db.session.commit()
            ips = [node.ip_address for node in ConnectedNode.query.with_entities(ConnectedNode.ip_address).all()]
            for node_ip in ips:
                print("++++++++++++++++++++++ Node de la network SUPUESTAMENTE: " + str(node_ip))
                blockchain.add_node(node_ip)
            response = {
                'message': 'Your IP has been added to the connected nodes. The DoveCoin chain contains the following nodes:  ',
                'total_nodes': get_all_nodes()
            }
            print("=====> Response" + str(response))
            return jsonify(response), 201
        else:
            response = {
                'message': 'Your IP is already in the blockchain. The DoveCoin chain contains the following users:  ',
                'total_nodes': get_all_nodes()
            }
            print("NODE NETWORK" + str(blockchain.nodes))
            return jsonify(response), 200

    return jsonify({"status": "invalid request"}), 400


# Reemplazar cadena por la cadena más larga (si es necesario)
@app.route('/replace_chain', methods=['GET', 'POST'])
def replace_chain():
    network = ConnectedNode.query.with_entities(ConnectedNode.ip_address).all()
    replace_chain = blockchain.replace_chain(network)  # True o False
    if replace_chain:
        response = {
            'message': 'The nodes had different strings and have been replaced by the longest one',
            'new_chain': [
                {
                    "index": block['index'],
                    "timestamp": block['timestamp'],
                    "proof": block['proof'],
                    "previous_hash": block['previous_hash'],
                    "transactions": block['transactions']
                } for block in blockchain.chain  
            ]
        }
    else:
        response = {
            'message': 'Everything is correct; the string in all nodes is already the longest.',
            'actual_chain': [
                {
                    "index": block['index'],
                    "timestamp": block['timestamp'],
                    "proof": block['proof'],
                    "previous_hash": block['previous_hash'],
                    "transactions": block['transactions']
                } for block in blockchain.chain  # Asegúrate de que aquí obtienes un diccionario
            ]
        }
    return jsonify(response), 200



"""
###############################################
    Rutas Administrador
###############################################
"""

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWD:  
            session['is_admin'] = True  # Marca la sesión como admin
            return redirect(url_for('admin')) 
        else:
            flash('Incorrect password', 'error')

    # Si el usuario no es admin, se muestra el formulario de contraseña
    if 'is_admin' not in session:
        return render_template('admin.html', clients=None)  # Muestra el formulario

    # Si el usuario es admin
    clients = Client.query.all()
    return render_template('admin.html', clients=clients) 


@app.route('/logout')
def logout():
    session.pop('is_admin', None)  # Eliminar la clave de sesión que indica que el usuario está conectado
    flash('You have successfully logged out', 'success')
    return render_template('index.html') 

@app.route('/clear_nodes', methods=['POST'])
def clear_nodes():
    try:
        db.session.query(ConnectedNode).delete()
        db.session.commit()
        return jsonify({"message": "All nodes have been successfully removed!"}), 200
    except Exception as e:
        db.session.rollback()  # Revertir los cambios en caso de error
        return jsonify({"message": "An error occurred while clearing nodes."}), 500  



@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    client = Client.query.get(user_id)
    if client:
        db.session.delete(client)
        db.session.commit()
        flash('User successfully deleted.', 'success')
    else:
        flash('User not found', 'error')
    return redirect(url_for('admin'))

@app.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    data = request.form
    client = Client.query.get(user_id)

    if client:
        client.name = data.get('name')
        client.email = data.get('email')
        client.node = data.get('node')
        db.session.commit()
        flash('User successfully updated.', 'success')
    else:
        flash('User not found', 'error')

    return redirect(url_for('admin'))

@app.route('/edit_user/<int:user_id>', methods=['GET'])
def edit_user(user_id):
    client = Client.query.get(user_id)
    if client:
        return render_template('editUsers.html', client=client)
    flash('User not found', 'error')
    return redirect(url_for('admin'))


@app.route('/change_password/<int:user_id>', methods=['POST'])
def change_password(user_id):
    client = Client.query.get(user_id)
    if client:
        new_password = request.form.get('password')
        if new_password:
            client.password = new_password  
            db.session.commit()
            return jsonify({'message': 'Password updated successfully'}), 200
        return jsonify({'message': 'The password cannot be empty'}), 400
    return jsonify({'message': 'User not foun'}), 404




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Ejecuta app.py --port <puerto>")
    parser.add_argument('--port', type=int, default=5000, help="Puerto en el que se ejecutará la aplicación")
    
    args = parser.parse_args()

    create_database(app)

    app.run(host='0.0.0.0', port=args.port, debug=True)
