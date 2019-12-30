"""
Export data from the db do some aggregating(average, total, etc.)
publish the information in a csv formatted file, example csv format,
header => name,level,published,created_on,review_count,avg_rating
Body ex => Product 1,1,True,2019-07-10,10,4.3
"""
from config import session
from models import Reviews, Products
from sqlalchemy import func
import csv

csv_file = open("products_csv.csv", mode="w")
fields = ["name", "level", "published", "created_on", "review_count", "average_rating"]
csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
csv_writer.writeheader()

reviews_statement = (
    session.query(
        Reviews.product_id,
        func.count("*").label("review_count"),
        func.avg(Reviews.rating).label("review_average"),
    )
    .group_by(Reviews.product_id)
    .subquery()
)

for product, review_count, avg_rating in (
    session.query(
        Products, reviews_statement.c.review_count, reviews_statement.c.review_average
    )
    .outerjoin(reviews_statement, Products.id == reviews_statement.c.product_id)
    .limit(50)
):
    csv_writer.writerow(
        {
            "name": product.name,
            "level": product.level,
            "published": product.published,
            "created_on": product.created_on.date(),
            "review_count": review_count or 0,
            "average_rating": round(float(avg_rating), 4) if avg_rating else 0,
        }
    )

csv_file.close()
