from flask_wtf import FlaskForm
from wtforms import TextField,SubmitField,PasswordField,IntegerField,SelectField
from wtforms.validators import Email,DataRequired,EqualTo,Length
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email=TextField("Email Address",validators=[DataRequired(),Email()])
    password=PasswordField("Enter Password",validators=[DataRequired()])
    submit= SubmitField("Login")

class SignupForm (FlaskForm):
    fname= TextField("First Name: ", validators=[DataRequired()])
    lname= TextField("Last Name: ",validators=[DataRequired()])
    email= TextField("Email: ",validators=[DataRequired(),Email()])
    password= PasswordField("Password: ",validators=[DataRequired()])
    confirm_password= PasswordField("Confirm password: ",validators=[EqualTo('password', message="password match")])
    gstnumber= IntegerField("GST Number: ")
    companyname= TextField("Company Name: ",validators=[DataRequired()])
    phone= IntegerField("Phone: ")
    address= TextField("Address: ", validators=[DataRequired()])
    submit=SubmitField("Submit")

    def check_email(self,field):
        if(self.query.filter_by(email=field.data).first()):
            raise ValidationError("Already registered")

class InvoiceForm(FlaskForm):
    client= TextField("Client:",validators=[DataRequired()])
    creator=TextField("Creator:",validators=[DataRequired()])
    item_name=TextField("Item name:")
    price= IntegerField("Price of One Unit:")
    quantity= IntegerField("Quantity")
    submit=SubmitField("Create Invoice")
