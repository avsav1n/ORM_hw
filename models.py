import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id_pub = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=30), unique=True, nullable=False)

    book = relationship('Book', back_populates='publisher')

    def __str__(self):
        return f'publisher || id_pub: {self.id_pub}\n\tname: {self.name}'

class Book(Base):
    __tablename__ = 'book'

    id_book = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), nullable=False)
    id_pub = sq.Column(sq.Integer, sq.ForeignKey('publisher.id_pub'), nullable=False)

    publisher = relationship('Publisher', back_populates='book')
    stock = relationship('Stock', back_populates='book')

    def __str__(self):
        return f'book || id_book: {self.id_book}\n\tid_pub: {self.id_pub}\n\ttitle: {self.title}'

class Shop(Base):
    __tablename__ = 'shop'

    id_shop = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=30), unique=True, nullable=False)

    stock = relationship('Stock', back_populates='shop')

    def __str__(self):
        return f'shop || id_shop: {self.id_shop}\n\tname: {self.name}'

class Stock(Base):
    __tablename__ = 'stock'

    id_stock = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id_book'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id_shop'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    shop = relationship('Shop', back_populates='stock')
    book = relationship('Book', back_populates='stock')
    sale = relationship('Sale', back_populates='stock')

    def __str__(self):
        return (f'stock || id_stock: {self.id_stock}\n\tid_book: {self.id_book}'
                f'\n\tid_shop: {self.id_shop}\n\tcount: {self.count}')

class Sale(Base):
    __tablename__ = 'sale'

    id_sale = sq.Column(sq.Integer, primary_key=True)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id_stock'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    price = sq.Column(sq.Float, nullable=False)

    stock = relationship('Stock', back_populates='sale')
    
    def __str__(self):
        return (f'sale || id_sale: {self.id_sale}\n\tid_stock: {self.id_stock}'
                f'\n\tcount: {self.count}\n\tdata: {self.data}\n\tprice: {self.price}')

def create_table(engine):
    Base.metadata.create_all(engine)

def delete_table(engine):
    Base.metadata.drop_all(engine)
