from flask_sqlalchemy import SQLAlchemy

from models import Role, User


def populate_db(db: SQLAlchemy):
    """Takes care of populating the database for testing purposes, going to create two types of roles (admin and
    regular user) and a user for each type of role.

    :param db: an instance of SQLAlchemy, representing the database to be populated
    """
    roles = ["admin", "regular_user"]
    for role in roles:
        new_role = Role(name=role)
        db.session.add(new_role)
        db.session.commit()

    users = [["mariorossi", "password", 1], ["lucaverdi", "secretpassword", 2]]
    for user in users:
        new_user = User(username=user[0], password=user[1], role_id=user[2])
        db.session.add(new_user)
        db.session.commit()
