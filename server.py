from flask import Flask, render_template, request, url_for, redirect, session, send_file
from flask_migrate import Migrate
from tempfile import NamedTemporaryFile
from InvoiceGenerator.api import Invoice,Item,Client,Provider,Creator
from InvoiceGen import app, db
from InvoiceGen.forms import InvoiceForm, LoginForm, SignupForm
from InvoiceGen.models import Our_customer
from flask_bcrypt import Bcrypt
from flask_login import login_user,login_required,logout_user
import os

logged_in=False

db.create_all()

Migrate(app,db)

hash= Bcrypt(app)

@app.route('/home')
@login_required
def home():
    return render_template('home.html')



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


@app.route('/invoice',methods=['GET','POST'])
@login_required
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
            pdf.gen("invoice.pdf",generate_qr_code=True)
            return send_file("invoice.pdf")
    else:
        return redirect(url_for('login'))
    return render_template('invoice.html',form=form)

@app.route("/",methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    form= LoginForm()
    if(form.validate_on_submit()):
        session['email']=form.email.data
        session['password']=form.password.data
        user=Our_customer.query.filter_by(email=session['email']).first()
        if(user.check_password(password=session['password'])):
            login_user(user)
            next= request.args.get('next')
            if(next == None):
                return redirect(url_for('home'))
            return redirect(next)
        else:
           return redirect(url_for("login"))
    return render_template('login.html', form =form)



if __name__ == '__main__':
    app.run(debug= True)
