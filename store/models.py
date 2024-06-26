
from store import db, login_manager, app
from store import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))


class Item(db.Model):
    name = db.Column(db.String(length=100), primary_key=True, )
    img = db.Column(db.String(length=1000), nullable=False)

    price = db.Column(db.Integer(), nullable=False)
    info = db.Column(db.String(length=100000), nullable=False)
    amnt_in_stock = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.Integer(), nullable=False)


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=1000), nullable=False)
    email = db.Column(db.String(length=100000), nullable=False)
    amount_in_acc = db.Column(db.Numeric(precision=20, scale=2), nullable=False)
    # Hashing the password:
    password_hash = db.Column(db.String(length=60), nullable=False)


    @property
    # the getter func
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        # where password_hash is the field in the db that has the user passwords

    # to ensure that the hashed password is stored as a Unicode string.
    # The hash generated by bcrypt is typically a binary data sequence,
    # and this step might be necessary depending on how the password_hash attribute
    # is expected to be stored and used.

    # func below to allow you to check password when user logs in:
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


#
class BoughtItems(db.Model):
    transaction_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer())
    item_name = db.Column(db.String())

class CartItems(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer())
    item_name = db.Column(db.String())

with app.app_context():
    db.create_all()
