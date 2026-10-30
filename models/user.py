from models.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserManager:
    @staticmethod
    def create_user(username, email, password):
        if User.query.filter_by(username=username).first():
            raise ValueError("Username already exists")
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already exists")
        
        password_hash = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            return user
        return None
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

from models.database import User
