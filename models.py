# create table products (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(50) UNIQUE NOT NULL,
#     level INTEGER NOT NULL,
#     published BOOLEAN NOT NULL DEFAULT false,
#     created_on TIMESTAMP NOT NULL DEFAULT NOW()
# );
# create table reviews (
#     id SERIAL PRIMARY KEY,
#     product_id INTEGER REFERENCES products(id),
#     rating INTEGER NOT NULL,
#     comment TEXT,
#     created_on TIMESTAMP NOT NULL DEFAULT NOW()
# );
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Products(Base):
    """
    Products class to map to the products table
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    level = Column(Integer, nullable=False)
    published = Column(Boolean, nullable=False, default=False)
    created_on = Column(TIMESTAMP, nullable=False)
    reviews = relationship("Reviews", order_by="Reviews.rating", back_populates="product")

class Reviews(Base):
    """
    Reviews class to map to the reviews table
    create table reviews (
     id SERIAL PRIMARY KEY,
     product_id INTEGER REFERENCES products(id),
     rating INTEGER NOT NULL,
     comment TEXT,
     created_on TIMESTAMP NOT NULL DEFAULT NOW()
    );
    """

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_on = Column(TIMESTAMP, nullable=False)

    product = relationship("Products", back_populates="reviews")
