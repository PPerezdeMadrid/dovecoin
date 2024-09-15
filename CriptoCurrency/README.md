# dovecoin
Proyecto de creación de una criptomoneda "Dovecoin" para entender el funcionamiento del blockchain

Peticiones [GET]
- "/get_chain" --> ver la cadena de bloque
- "/mine_block" --> mina una transacción
- "/replace_chain" --> reemplazar la cadena si hay una más larga (imp el connect_node previo y el body a none)


Peticiones [POST]
- "/connect_node" --> le pasamos los nodos a POSTMAN: body>>raw>>JSON 
    Ejemplo en el nodo "http://192.168.0.202:5001":
    ```JSON
    { "nodes": ["http://192.168.0.202:5002","http://192.168.0.202:5003"]}
    ```
  
  - "/add_transaction" --> añadir una nueva transacción, le pasamos los nodos a POSTMAN: body>>raw>>JSON 
      Ejemplo: mandar 10 DoveCoin a Sol
      ```JSON
      {
        "sender": "Paloma",
        "receiver": "Pedro",
        "amount": 100
    }
    ```




Notas:
- Cuando un nodo se crea, se conecta
- Se tiene que ver que nodos hay disponibles
- Connect_node > replace_chain > Connect_node > replace_chain > Connect_node > replace_chain
- Base de datos en la nube de nodos??? o en local??