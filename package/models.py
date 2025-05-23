from package import database, bcrypt, login_manager
from sqlalchemy.orm import mapped_column, relationship, foreign
from sqlalchemy import Integer, String
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    id = mapped_column(Integer,
        primary_key = True, 
        nullable = False, 
        unique = True)
    
    username = mapped_column(String(30),
        unique = True,
        nullable = False)
    
    email = mapped_column(String(50),
        unique = True,
        nullable = False)
    
    password_hashed = mapped_column(String(40),
        nullable = False)
    
    budget = mapped_column(Integer,
        nullable = False,
        default = 1000)
    
    items = relationship("Item", backref = "owned_by", lazy = True)
#   items = database.relationship("Item", backref = "user_item", lazy = True)

    @property
    def budget_comma(self):
        return f"{(int(self.budget)):,}$"

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, pure_password):
        self.password_hashed = bcrypt.generate_password_hash(pure_password).decode("utf-8")

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hashed, attempted_password)
    

class Item(database.Model):
    id = database.Column(database.Integer(),
        primary_key = True)

    name = database.Column(database.String(length = 30),
        nullable = False,
        unique = True)

    price = database.Column(database.Integer(),
        nullable = False)

    barcode = database.Column(database.String(length = 12),
        nullable = False,
        unique = True)
    
    description = database.Column(database.String(length = 1024),
        nullable = False,
        unique = True)
    
    owner = database.Column(database.Integer(), database.ForeignKey("user.id"))

    def __repr__(self):
        return f"Item {self.name}"