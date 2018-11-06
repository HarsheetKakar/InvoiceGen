from flask import Flask, render_template, request, url_for, redirect, session, send_file
from flask_migrate import Migrate
from tempfile import NamedTemporaryFile
from InvoiceGenerator.api import Invoice,Item,Client,Provider,Creator
from InvoiceGen import app, db
from InvoiceGen.forms import InvoiceForm, LoginForm, SignupForm
from InvoiceGen.models import Our_customer, load_user
from flask_bcrypt import Bcrypt
from flask_login import login_user,login_required,logout_user, current_user
import os

logged_in=False

db.create_all()

Migrate(app,db)

hash= Bcrypt(app)

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/invoice',methods=['GET','POST'])
@login_required
def invoice():
    form= InvoiceForm()
    print(form)
    if form.validate_on_submit():
        client=form.client.data
        creator=form.creator.data
        item_name=form.item_name.data
        price=form.price.data
        quantity=form.quantity.data
        a=current_user
        client= Client(client)
        provider= Provider(a.name, bank_account=a.gstnumber, bank_code='2018')
        creator= Creator(creator)
        os.environ["INVOICE_LANG"]="en"
        invoice=Invoice(client,provider,creator)
        invoice.currency_locale="en_US.UTF_8"

        invoice.add_item(Item(quantity,price,item_name))
        from InvoiceGenerator.pdf import SimpleInvoice
        pdf=SimpleInvoice(invoice)
        pdf.gen("invoice.pdf",generate_qr_code=False)
        return send_file("invoice.pdf")
    return render_template('invoice.html',form=form)

@app.route("/",methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    form= LoginForm()
    if(form.validate_on_submit()):
        email=form.email.data
        password=form.password.data
        user=Our_customer.query.filter_by(email=email).first()
        if(user.check_password(password=password) and user is not None):
            login_user(user)
            print(user.is_active)
            next= request.args.get('next')
            print(next)
            if next == None or not next[0]=='/':
                next = url_for('home')
            return redirect(next)
    return render_template('login.html', form =form)

@app.route('/signup',methods=['GET','POST'])
def signup():
    form= SignupForm()
    new_owner= Our_customer()
    if form.validate_on_submit():
        new_owner.name= form.fname.data+" "+form.lname.data
        new_owner.email= form.email.data
        new_owner.password= hash.generate_password_hash(form.password.data)
        new_owner.gstnumber= form.gstnumber.data
        new_owner.companyname= form.companyname.data
        new_owner.phone= form.phone.data
        new_owner.address= form.address.data
        new_owner.total_receivables=0
        new_owner.total_payable=0
        db.session.add(new_owner)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html",form=form)

@app.route('/logged_out')
@login_required
def logout():
    print("logged out")
    logout_user()
    return "logged out"

if __name__ == '__main__':
    app.run(debug= True)
