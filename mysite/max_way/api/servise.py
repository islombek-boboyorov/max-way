from django.db import connection
from contextlib import closing


def get_category():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from category""")
        category = dict_fetchall(cursor)
    return category


def get_product():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from product """)
        product = dict_fetchall(cursor)
    return product


def get_order():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from order """)
        product = dict_fetchall(cursor)
    return product


def get_user():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from user """)
        product = dict_fetchall(cursor)
    return product


def get_bot():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from bot_user """)
        product = dict_fetchall(cursor)
    return product


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row))
            for row in cursor.fetchall()]


def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.fetchall()]
    return dict(zip(columns, row))
