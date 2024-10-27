import sqlite3

def create_database():
    # Conectar a la base de datos
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Crear la tabla 'clients'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            node TEXT NOT NULL
        )
    ''')

    # Cerrar la conexión
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
