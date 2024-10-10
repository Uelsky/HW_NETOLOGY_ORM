import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
import json


print("Enter hostname of your DB")
host = input()
print("Enter port of your DB")
port = input()
print("Enter name of your DB")
db_name = input()
print("Enter your login")
login = input()
print("Enter your password")
password = input()


DSN = f"postgresql://{login}:{password}@{host}:{port}/{db_name}"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


# with open('fixtures/tests_data.json', 'r') as fd:
#     data = json.load(fd)
#
# for record in data:
#     model = {
#         'publisher': Publisher,
#         'shop': Shop,
#         'book': Book,
#         'stock': Stock,
#         'sale': Sale,
#     }[record.get('model')]
#     session.add(model(id=record.get('pk'), **record.get('fields')))
# session.commit()

with open(r"fixtures/tests_data.json", 'r', encoding='utf-8') as file:
    tests = json.load(file)
    for test in tests:
        if test['model'] == 'publisher':
            session.add(Publisher(
                id = test['pk'],
                name = test['fields']['name']
            ))
            session.commit()

        elif test['model'] == 'book':
            session.add(Book(
                id = test['pk'],
                title = test['fields']['title'],
                id_publisher = test['fields']['id_publisher']
            ))
            session.commit()

        elif test['model'] == 'shop':
            session.add(Shop(
                id = test['pk'],
                name = test['fields']['name']
            ))
            session.commit()

        elif test['model'] == 'stock':
            session.add(Stock(
                id = test['pk'],
                id_shop = test['fields']['id_shop'],
                id_book = test['fields']['id_book'],
                count = test['fields']['count']
            ))
            session.commit()

        elif test['model'] == 'sale':
            date = test['fields']['date_sale'].split('T')[0]
            time = test['fields']['date_sale'].split('T')[1][:-1]
            date_sale = f"{date} {time}"
            session.add(Sale(
                id = test['pk'],
                price = float(test['fields']['price']),
                date_sale = date_sale,
                count = test['fields']['count'],
                id_stock = test['fields']['id_stock']
            ))


def search(publ: int):
    books_of_publisher = session.query(Book).join(Publisher.books).filter(Publisher.id == publ).all()

    for book in books_of_publisher:
        book_id = book.id
        book_title = book.title
        stocks_of_book = session.query(Stock).join(Book.stock).filter(Stock.id_book == book_id).all()

        for stock in stocks_of_book:
            stock_id = stock.id
            shop_name = session.query(Shop).filter(Shop.id == stock.id_shop).all()[0].name
            sales_of_stock = session.query(Sale).join(Stock.sales).filter(Sale.id_stock == stock_id).all()

            for sale in sales_of_stock:
                total = sale.price * sale.count
                print(" | ".join([
                    book_title, shop_name, str(total),
                    f"{sale.date_sale.day}-{sale.date_sale.month}-{sale.date_sale.year}"
                ]))



if __name__ == "__main__":
    publisher = input()
    if publisher.isdigit():
        publ = publisher
        search(int(publ))
    else:
        publ = session.query(Publisher).filter(Publisher.name==publisher).all()[0].id
        search(int(publ))

    session.close()

else:
    session.close()
