from InvoiceGen import db,app,login_manager
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

hash=Bcrypt(app)

@login_manager.user_loader
def load_user(userid):
    print(Our_customer.query.get(userid))
    return Our_customer.query.get(userid)

class Our_customer(db.Model,UserMixin):
    __tablename__ = 'Our_customer'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    password = db.Column(db.String(30))
    gstnumber = db.Column(db.Integer())
    total_receivables = db.Column(db.Integer())
    total_payable = db.Column(db.Integer())
    companyname = db.Column(db.String(120))
    address= db.Column(db.String(120))
    phone= db.Column(db.Integer())

    def check_password(self,password):
        return hash.check_password_hash(self.password, password)
# class Items(db.Model):
#     pass
#
#     id= db.Column(db.Integer(),)
