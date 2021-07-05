from django.db import connection
from contextlib import closing
import json


def create_user(chat_id, created_at):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""
            INSERT INTO bot_user (chat_id, created_at) VALUES (%s, %s)
        """, [chat_id, created_at]
        )


def get_max_id(chat_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select max(id) from "order" where chat_id = %s""", [chat_id])
        pk = dict_fetchone(cursor)['max']
        print(pk)
    return pk


def get_user_by_chat_id(chat_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""
            SELECT * FROM bot_user WHERE chat_id = %s
        """, [chat_id])
        user = dict_fetchone(cursor)
        return user


def update_user(state, chat_id, msg):
    with closing(connection.cursor()) as cursor:
        if state == 1:
            cursor.execute("""
                UPDATE bot_user SET first_name = %s WHERE chat_id = %s
            """, [msg, chat_id]
                             )

        elif state == 2:
            cursor.execute("""
                UPDATE bot_user SET last_name = %s WHERE chat_id = %s
             """, [msg, chat_id]
                             )

        elif state == 3:
            cursor.execute("""
                UPDATE bot_user SET contact = %s WHERE chat_id = %s
            """, [msg, chat_id]
                             )


def get_product():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from product""")
        products = dict_fetchall(cursor)
    return products


def get_product_price(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select price from product where id = %s""", [pk])
        price = dict_fetchone(cursor)
    return price


def get_category():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from category  """)
        categories = dict_fetchall(cursor)
    return categories


def get_category_products(category_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from product where category_id = %s """, [category_id])
        products = dict_fetchall(cursor)
    return products


def get_product_by_id(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from product where id = %s""", [pk])
        product = dict_fetchone(cursor)
    return product



def update_order(total_price, time, cart, chat_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""INSERT INTO "order" (status, total_price, created_at, products, chat_id)
         VALUES (%s, %s, %s, %s, %s)""", [1, total_price, time, json.dumps(cart), chat_id])


def update_user_site(first_name, last_name, phone, price, time, order, address):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""INSERT INTO "user" (first_name, last_name, phone, price_type, created_at, order_id, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                       [first_name, last_name, phone, price, time, order, address])


def get_info_order(chat_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from "order" where chat_id = %s""", [chat_id])
        info = dict_fetchall(cursor)
    return info


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
