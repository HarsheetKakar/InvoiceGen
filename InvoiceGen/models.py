from InvoiceGen import db

class Our_customer(db.Model):
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

class Items(db.Model):
    __tablename__= 'Items'

    id= db.Column(db.Integer(),)
