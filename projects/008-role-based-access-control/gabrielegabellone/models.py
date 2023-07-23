from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Role(db.Model):
    """Represents the model of a role in the roles table.
    """
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return f'<id: {self.id}, name: {self.name}>'


class User(UserMixin, db.Model):
    """Represents the model of a user in the users table.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return f'<id: {self.id}, username: {self.username}, role: {self.role.name}>'
