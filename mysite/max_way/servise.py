from django.db import connection
from contextlib import closing


def get_product_by_id(product_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""
        select id, title as name, description, image, price from max_way_product where id = %s""",
                       [product_id])
        product = dict_fetchone(cursor)
    return product


def get_order_max_id():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select max(id) from max_way_order""")
        order_id = dict_fetchone(cursor)
    return order_id


def get_product():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from max_way_product""")
        products = dict_fetchall(cursor)
    return products


def get_product_price(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select price from max_way_product where id = %s""", [pk])
        price = dict_fetchone(cursor)
    return price


def get_category():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from max_way_category  """)
        categories = dict_fetchall(cursor)
    return categories


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row))
            for row in cursor.fetchall()]


def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))
