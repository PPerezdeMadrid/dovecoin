from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    node = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, password, node):
        self.name = name
        self.email = email
        self.password = password
        self.node = node

    def __repr__(self):
        return f'<Client {self.name}>'


def get_user_by_email(email):
    return Client.query.filter_by(email=email).first()

def create_database(app):
    with app.app_context():
        db.create_all()

def get_all_nodes():
    nodes = db.session.query(Client.node).distinct().all()
    return [node[0] for node in nodes]  

