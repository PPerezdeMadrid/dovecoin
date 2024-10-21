from .. import db  # Importa db desde el archivo principal de la aplicación

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    telefono = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        return f'<Cliente {self.nombre}>'

""" Crear la base de datos en app.py   
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos
    app.run(debug=True)  # Ejecuta la aplicación
"""

