import sqlalchemy as sql
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(
        sql.String(length=60),
        unique=True,
        nullable=False
    )

    books = relationship("Book", back_populates="publisher")


class Book(Base):
    __tablename__ = "book"

    id = sql.Column(sql.Integer, primary_key=True)
    title = sql.Column(sql.String(length=100))
    id_publisher = sql.Column(
        sql.Integer,
        sql.ForeignKey("publisher.id"),
        nullable=False
    )

    publisher = relationship(Publisher, back_populates="books")
    stock = relationship("Stock", back_populates="books")


class Shop(Base):
    __tablename__ = "shop"

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(
        sql.String(length=60),
        unique=True,
        nullable=False
    )

    stock = relationship("Stock", back_populates="shops")


class Stock(Base):
    __tablename__ = "stock"

    id = sql.Column(sql.Integer, primary_key=True)
    id_book = sql.Column(
        sql.Integer,
        sql.ForeignKey("book.id"),
        nullable=False
    )
    id_shop = sql.Column(
        sql.Integer,
        sql.ForeignKey("shop.id"),
        nullable=False
    )
    count = sql.Column(sql.Integer, nullable=False)

    books = relationship(Book, back_populates="stock")
    shops = relationship(Shop, back_populates="stock")
    sales = relationship("Sale", back_populates="stocks")


class Sale(Base):
    __tablename__ = "sale"

    id = sql.Column(sql.Integer, primary_key=True)
    price = sql.Column(sql.Float, nullable=False)
    date_sale = sql.Column(sql.DateTime, nullable=False)
    id_stock = sql.Column(
        sql.Integer,
        sql.ForeignKey("stock.id"),
        nullable=False
    )
    count = sql.Column(sql.Integer, nullable=False)

    stocks = relationship(Stock, back_populates="sales")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
