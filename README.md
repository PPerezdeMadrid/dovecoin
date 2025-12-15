# Dovecoin

> 🇬🇧 **English version**  
> 👉 [Ver versión en Español](#versión-en-español)


## Description

Dovecoin is an example cryptocurrency designed to explore how blockchain technology and cryptocurrencies work.  
This project provides a hands-on understanding of blockchain concepts, smart contracts, and cryptocurrency development.


## Features

- **Cryptocurrency**: Basic implementation of a digital currency with essential functionalities.
- **Smart Contract**: Solidity code that enables automated transactions on the network.
- **src**: Web application for the DoveCoin cryptocurrency.


## Installation

1. Clone the repository.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

## Explanation

### Cryptocurrency

Practical implementation of cryptocurrencies using the Flask framework:

* **Distributed Blockchain**: Mechanism to securely and distributively store transactions.

* **Proof of Work (PoW)**: Consensus system that ensures data integrity.

* `palomaDoveCoin.py`, `pedroDoveCoin.py`, and `solDoveCoin.py` simulate three users. These files can be used with Postman to visualize the distributed behavior of the blockchain.

* `blockchain.py` contains the basic cryptocurrency logic, while `dovecoin.py` implements a unique PoW algorithm specific to Dovecoin.


## Smart Contract

This section simulates a wallet (**MyEtherWallet**) and an ICO contract.

### What is an ICO?

An **ICO (Initial Coin Offering)** is a fundraising mechanism in the cryptocurrency space where a new company offers tokens or cryptocurrencies to investors in exchange for capital. It is similar to an IPO in traditional stock markets, with some key differences:

* **Token Issuance**: Investors purchase tokens that may represent future access to products or services, or may simply hold market value.
* **Transparency**: ICOs are usually accompanied by a *white paper* explaining the project, its vision, the underlying technology, and how funds will be used.
* **Risks**: Investing in an ICO carries significant risks, as many projects are new and lack a proven track record. Regulatory and security concerns are also common.
* **Early Stage**: ICOs typically occur before the launch of a product or service, meaning investors are betting on the project’s future potential.


## Source (`src`)

This section contains all the code for a Flask-based web server.

### Usage

To run the application, use the following command:

```bash
python app.py --port <port>
```

The port is important because it determines the IP address used to connect with other nodes and verify whether your blockchain is the most up to date.

---

## Functionalities

### Basic Routes

* **`/`**: Home page that renders `index.html`.
* **`/contact`**: Displays a contact form. Supports GET and POST methods.
* **`/register`**: Displays a registration form. Supports GET and POST methods.
* **`/blog`**: Displays a blog page. Supports GET and POST methods.



### Core Blockchain Routes

* **`/registerClient`**

  * Method: POST
  * Registers a new client with name, email, password, and node.
  * Stores the information in the database and displays a success message.

* **`/login`**

  * Method: POST
  * Authenticates a user using email and password.
  * Redirects to the user profile upon successful login.

* **`/mine_block_ajax`**

  * Method: GET
  * Mines a new block in the blockchain.
  * Performs proof of work and adds an empty transaction.

* **`/get_chain`**

  * Method: GET
  * Returns the full blockchain and its length.

* **`/is_valid`**

  * Method: GET
  * Checks whether the blockchain is valid.

* **`/GoTransaction`**

  * Method: GET
  * Displays a form to perform a transaction.

* **`/add_transaction`**

  * Method: POST
  * Adds a new transaction to the blockchain.
  * Returns the index of the block where the transaction will be added.


### Decentralization Routes

* **`/connect_node`**

  * Method: GET and POST
  * Connects new nodes to the blockchain.
  * Displays the list of connected nodes.

* **`/replace_chain`**

  * Method: GET and POST
  * Replaces the blockchain with the longest valid chain if needed.


### Administrative Routes

* **`/admin`**

  * Method: GET and POST
  * Displays the admin panel.
  * Allows authentication via password.

* **`/logout`**

  * Method: GET
  * Logs out the administrator.

* **`/delete_user/<int:user_id>`**

  * Method: POST
  * Deletes a user by ID.

* **`/update_user/<int:user_id>`**

  * Method: POST
  * Updates user information by ID.

* **`/edit_user/<int:user_id>`**

  * Method: GET
  * Displays the user edit form.

* **`/change_password/<int:user_id>`**

  * Method: POST
  * Changes a user’s password.

---

# Versión en Español

## Descripción
Dovecoin es una criptomoneda de ejemplo diseñada para explorar el funcionamiento de la tecnología blockchain y criptomonedas. Este proyecto ofrece una comprensión práctica de conceptos de blockchain, contratos inteligentes y desarrollo de criptomonedas.

## Características
- **CriptoCurrency**: Implementación básica de una moneda digital con funcionalidades esenciales.
- **SmartContract**: Código en Solidity que permite la automatización de transacciones en la red.
- **src**: Aplicación web de la criptomoneda DoveCoin. 


### Instalación
1. Clona el repositorio.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

### Explicación

#### CriptoCurrency
Puesta en práctica de las criptmonedas con el framework Flask :
- **Blockchain distribuida:** Mecanismo para almacenar transacciones de forma segura y distribuida.
- **Prueba de trabajo (PoW):** Sistema de consenso que asegura la integridad de los datos.

- palomaDoveCoin.py, pedroDoveCoin.py y solDoveCoin.py simulan tres usuarios. Estos archivos se pueden usar para visualizar con PostMan el funcionamiento distribuido de la cadena de bloques.
- blockchain.py es la criptmoneda básica mientras que dovecoin.py tiene un PoW único que identifica a la dovecoin

### SmartContract 
Este apartado simula una cartera (**MyEtherWallet**) y un contrato ICO.
#### ¿Qué es un ICO?

Un **ICO** (Initial Coin Offering) es un mecanismo de recaudación de fondos en el ámbito de las criptomonedas, donde una nueva empresa ofrece tokens o criptomonedas a inversores a cambio de capital. Este proceso se asemeja a una oferta pública inicial (IPO) en el mercado de valores, pero con algunas diferencias clave:

- **Emisión de Tokens**: Durante un ICO, los inversores compran tokens que pueden representar un acceso futuro a productos o servicios de la empresa, o simplemente pueden tener valor en el mercado.

- **Transparencia**: Los ICOs suelen estar acompañados de un "white paper", un documento que detalla el proyecto, su visión, la tecnología detrás de él y cómo se utilizarán los fondos recaudados.

- **Riesgos**: Invertir en un ICO conlleva riesgos significativos, ya que muchas de estas empresas son nuevas y pueden no tener un historial comprobado. También hay preocupaciones sobre la regulación y la seguridad de los fondos.

- **Fase Inicial**: Generalmente, los ICOs se llevan a cabo antes del lanzamiento de un producto o servicio, lo que significa que los inversores están apostando por el potencial futuro de la empresa.

### Source (src)

Este apartado contiene todo el código de un servidor web Flask.

#### Uso

Para ejecutar la aplicación, utiliza el siguiente comando:

```bash
python app.py --port <puerto>
```

El puerto es importante porque va a ser la dirección IP con la cual te vas a poder conectar a otros nodos y comprobar si tu cadena es la más reciente.

#### Funcionalidades

##### Rutas Básicas

- **`/`**: Página de inicio que renderiza `index.html`.
- **`/contact`**: Muestra un formulario de contacto. Soporta métodos GET y POST.
- **`/register`**: Muestra un formulario de registro. Soporta métodos GET y POST.
- **`/blog`**: Muestra una página de blog. Soporta métodos GET y POST.

##### Rutas de Funcionalidades Básicas

- **`/registerClient`**: 
  - Método: POST.
  - Registra un nuevo cliente. Recibe datos como nombre, email, contraseña y nodo.
  - Almacena la información en la base de datos y muestra un mensaje de éxito.

- **`/login`**: 
  - Método: POST.
  - Autentica a un usuario usando email y contraseña.
  - Si la autenticación es exitosa, redirige al perfil del usuario.

- **`/mine_block_ajax`**: 
  - Método: GET.
  - Permite minar un bloque en la blockchain.
  - Realiza la prueba de trabajo y añade una transacción vacía.

- **`/get_chain`**: 
  - Método: GET.
  - Devuelve la cadena completa de bloques y su longitud.

- **`/is_valid`**: 
  - Método: GET.
  - Verifica si la cadena de bloques es válida y devuelve el estado.

- **`/GoTransaction`**: 
  - Método: GET.
  - Muestra un formulario para realizar una transacción.

- **`/add_transaction`**: 
  - Método: POST.
  - Añade una nueva transacción a la blockchain.
  - Responde con el índice del bloque al que se añadirá la transacción.

##### Rutas de Funcionalidades de Descentralización

- **`/connect_node`**: 
  - Método: POST y GET.
  - Conecta nuevos nodos a la blockchain.
  - Muestra los nodos conectados.

- **`/replace_chain`**: 
  - Método: GET y POST.
  - Reemplaza la cadena de bloques por la más larga si es necesario.

##### Rutas Administrativas

- **`/admin`**: 
  - Método: GET y POST.
  - Muestra el panel de administración.
  - Permite autenticación mediante contraseña.

- **`/logout`**: 
  - Método: GET.
  - Cierra la sesión del administrador.

- **`/delete_user/<int:user_id>`**: 
  - Método: POST.
  - Elimina un usuario basado en su ID.

- **`/update_user/<int:user_id>`**: 
  - Método: POST.
  - Actualiza la información de un usuario basado en su ID.

- **`/edit_user/<int:user_id>`**: 
  - Método: GET.
  - Muestra el formulario para editar la información de un usuario.

- **`/change_password/<int:user_id>`**: 
  - Método: POST.
  - Cambia la contraseña de un usuario basado en su ID.


