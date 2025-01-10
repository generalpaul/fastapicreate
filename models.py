from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, BLOB, TIMESTAMP, Float


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)



class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(BLOB, primary_key=True)
    last_name = Column(String, unique=True)
    middle_name = Column(String, unique=True)
    first_name = Column(String)
    address_street_barangay = Column(String)
    addrress_town_city = Column(String)
    address_zip = Column(String)
    bank_file_info= Column(String)



class Product(Base):
    __tablename__ = 'products'

    product_id = Column(String, primary_key=True)
    product_short_name = Column(String)
    product_long_name = Column(String)


class Product_Sub(Base):
    __tablename__ = 'products_sub'

    product_sub_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String)
    product_sub_code = Column(String)
    barcode = Column(String)
    amount = Column(Float)



class Buy(Base):
    __tablename__ = 'buy'

    id = Column(Integer, primary_key=True, index=True)
    product_sub_id = Column(String)
    description = Column(String)
    quantity = Column(Integer)
    amount = Column(Float, default=False)
    date_transacted = Column(TIMESTAMP)
