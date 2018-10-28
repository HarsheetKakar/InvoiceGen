from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
from server import db

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.

class Our_customer(Base):
    __tablename__ = 'Our_customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))
    gstnumber = db.Column(db.Integer())
    total_receivables = db.Column(db.Integer())
    total_payable = db.Column(db.Integer())
    companyname = db.Column(db.String(120), unique=True)
    address= db.Column(db.String(120),unique=True)
    phone= db.Column(db.Integer(11),unique=True)


# Create tables.
Base.metadata.create_all(bind=engine)
