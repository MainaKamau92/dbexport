"""
Export data from the db do some aggregating(average, total, etc.)
publish the information in a json formatted file, example csv format,
"""
from config import session
from models import Reviews, Products
from sqlalchemy import func
import json

reviews_statement = (
    session.query(
        Reviews.product_id,
        func.count("*").label("review_count"),
        func.avg(Reviews.rating).label("review_average"),
    )
    .group_by(Reviews.product_id)
    .subquery()
)
products = []
for product, review_count, avg_rating in (
    session.query(
        Products, reviews_statement.c.review_count, reviews_statement.c.review_average
    )
    .outerjoin(reviews_statement, Products.id == reviews_statement.c.product_id)
    .limit(50)
):
    products.append(
        {
            "name": product.name,
            "level": product.level,
            "published": product.published,
            "created_on": str(product.created_on.date()),
            "review_count": review_count or 0,
            "average_rating": round(float(avg_rating), 4) if avg_rating else 0,
        }
    )

with open("products_json.json", mode="w") as f:
    json.dump(products, f)
