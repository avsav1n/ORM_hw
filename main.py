import os
import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from prettytable import PrettyTable as pt
import models
from models import Publisher, Book, Shop, Stock, Sale

def alchemy_init():
    DSN = f'postgresql://postgres:{os.getenv('PSQLPASS')}@localhost:5432/pypost'
    engine = sqlalchemy.create_engine(DSN)
    Session = sessionmaker(engine)
    return engine, Session()

def create(engine, session):
    '''Создание таблиц моделями классов SQLAlchemy'''
    with session:
        models.create_table(engine)

def delete(engine, session):
    '''Удаление таблиц'''
    with session:
        models.delete_table(engine)

def add_data(engine=None, session=None):
    '''
    Функция заполнения таблиц из файла data\\tests_data.json
    '''
    with open('data\\tests_data.json', encoding='utf-8') as f:
        data = json.load(f)
    with session:
        for info in data:
            match info['model']:
                case 'publisher':
                    model = Publisher(id_pub=info['pk'],
                                      name=info['fields']['name'])
                case 'book':
                    model = Book(id_book=info['pk'],
                                 title=info['fields']['title'],
                                 id_pub=info['fields']['id_pub'])
                case 'shop':
                    model = Shop(id_shop=info['pk'],
                                 name=info['fields']['name'])
                case 'stock':
                    model = Stock(id_stock=info['pk'],
                                  id_book=info['fields']['id_book'],
                                  id_shop=info['fields']['id_shop'],
                                  count=info['fields']['count'])
                case 'sale':
                    model = Sale(id_sale=info['pk'],
                                 id_stock=info['fields']['id_stock'],
                                 count=info['fields']['count'],
                                 date_sale=info['fields']['date_sale'],
                                 price=info['fields']['price'])
            session.add(model)
        session.commit()

def request_info(engine=None, session=None):
    '''
    Функция выборки информации по покупкам книг выбранного издателя с последующим 
    выводом в терминал

    SELECT b.title, sh.name, sl.price, date(sl.date_sale)
    FROM publisher p 
    JOIN book b ON p.id_pub = b.id_pub 
    JOIN stock st ON st.id_book = b.id_book 
    JOIN shop sh ON sh.id_shop = st.id_shop 
    JOIN sale sl ON sl.id_stock = st.id_stock 
    WHERE p.name = 'Pearson'
    '''
    input_ = {'1': 'O’Reilly', '2': 'Pearson', '3': 'Microsoft Press', '4': 'No starch press'}
    input_ = input_[input('O’Reilly - 1\n'
                          'Pearson - 2\n'
                          'Microsoft Press - 3\n'
                          'No starch press - 4\n'
                          'Введите номер желаемого автора: ')]
    table = pt()
    table.field_names = ['Book', 'Shop', 'Price', 'Date']

    result = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
                  join(Publisher, Book.id_pub == Publisher.id_pub).\
                  join(Stock, Stock.id_book == Book.id_book).\
                  join(Shop, Shop.id_shop == Stock.id_shop).\
                  join(Sale, Sale.id_stock == Stock.id_stock).\
                  filter(Publisher.name == input_).all()

    for line in result:
        row = list(line)
        row[3] = row[3].date()
        table.add_row(row)

    print(f'\nФакты покупки книг издателя {input_} выведены ниже:')
    print(table)
    session.close()

# delete(*alchemy_init())
# create(*alchemy_init())

# add_data(*alchemy_init())
# request_info(*alchemy_init())
