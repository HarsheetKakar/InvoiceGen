#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, url_for, redirect, session
from flask_migrate import Migrate
from tempfile import NamedTemporaryFile
from InvoiceGenerator.api import Invoice,Item,Client,Provider,Creator
from forms import LoginForm, InvoiceForm, SignupForm

logged_in=False

app = Flask(__name__)
app.config['SECRET_KEY']="mykey"

from flask_sqlalchemy import SQLAlchemy
import os

x=os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///"+os.path.join(x,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)



################DATABASE###############
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

    #def __init__(self,name,email,password,
    #             gstnumber,total_receivables,total_payable
    #             companyname,address,phone):
    #    self.name=name
    #    self.email=email
    #    self.password=password
    #    self.

db.create_all()

Migrate(app,db)


@app.route('/home')
def home():
    if(not logged_in):
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route("/",methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    form= LoginForm()
    if(form.validate_on_submit()):
        session['email']=form.email.data
        session['password']=form.password.data
        print(Our_customer.query.filter_by(email=session["email"]).first().name)
        if(Our_customer.query.filter_by(email=session["email"])and Our_customer.query.filter_by(password=session["password"])):
            logged_in=True
            return redirect(url_for("home"))
        else:
           return redirect(url_for("login"))
    return render_template('login.html', form =form)


#@app.route('/register')
#def register():
#    session['email']= form.email.data
#    session['password']= form.password.data
#    if(form.validate_on_submit()):
#        return render_template(url_for("logged_in"))
#    return render_template('login.html', form=form)

@app.route('/logged_in')
def logged_in():
    return render_template("logged_in.html")

@app.route('/signup',methods=['GET','POST'])
def signup():
    form= SignupForm()
    new_owner= Our_customer()
    if form.validate_on_submit():
        new_owner.name= form.fname.data+" "+form.lname.data
        new_owner.email= form.email.data
        new_owner.password= form.password.data
        new_owner.gstnumber= form.gstnumber.data
        new_owner.companyname= form.companyname.data
        new_owner.phone= form.phone.data
        new_owner.address= form.address.data
        new_owner.total_receivables=0
        new_owner.total_payable=0
        db.session.add(new_owner)
        db.session.commit()
        return redirect(url_for("logged_in"))
    return render_template("signup.html",form=form)


@app.route('/invoice',methods=['GET','POST'])
def invoice():
    if(logged_in):
        form= InvoiceForm()
        if form.validate_on_submit():
            session['client']=form.client.data
            session['creator']=form.creator.data
            session['item_name']=form.item_name.data
            session['price']=form.price.data
            session['quantity']=form.quantity.data
            a=Our_customer.query.filter_by(email=session["email"]).first()
            client= Client(session['client'])
            provider= Provider(a.name, bank_account=a.gstnumber, bank_code='2018')
            creator= Creator(session['creator'])
            os.environ["INVOICE_LANG"]="en"
            invoice=Invoice(client,provider,creator)
            invoice.currency_locale="en_US.UTF_8"

            invoice.add_item(Item(session['quantity'],session['price'],session['item_name']))
            from InvoiceGenerator.pdf import SimpleInvoice
            pdf=SimpleInvoice(invoice)
            pdf.gen("invoice.pdf",generate_qr_code=False)

    else:
        return redirect(url_for('login'))
    return render_template('invoice.html',form=form)

def download_page():
    a=Our_customer.query.filter_by(email=session["email"]).first()
    client= Client(session['client'])
    provider= Provider(a.name, bank_account=a.gstnumber, bank_code='2018')
    creator= Creator(session['creator'])

    invoice=Invoice(client,provider,creator)
    invoice.currency_locale="en_US.UTF_8"

    invoice.add_item(Item(session['quantity'],session['price'],session['item_name']))
    from InvoiceGenerator.pdf import SimpleInvoice
    pdf=SimpleInvoice(invoice)
    pdf.gen("invoice.pdf",generate_qr_code=True)


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug= True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
