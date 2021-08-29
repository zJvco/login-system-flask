from app import db, lm
from flask_bcrypt import Bcrypt


@lm.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, Bcrypt):
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.generate_password_hash(password)

    def verify_password(self, pwd):
        return self.check_password_hash(self.password, pwd)

    def __repr__(self):
        return "<User %r>" % self.id
