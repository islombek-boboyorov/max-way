from django.db import connection
from contextlib import closing


def get_status_info():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select max_way_user.*, max_way_order.status as status
            from max_way_user left join max_way_order 
            on max_way_user.order_id =max_way_order.id""")
        status = dict_fetchall(cursor)
    return status


def get_status_1():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select count(status) from max_way_order where status = 1""")
        status = dict_fetchall(cursor)
    return status


def get_status_2():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select count(status) from max_way_order where status = 2""")
        status = dict_fetchall(cursor)
    return status


def get_status_3():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select count(status) from max_way_order where status = 3""")
        status = dict_fetchall(cursor)
    return status


def get_order_by_id(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from  max_way_order 
                 where id = %s""", [pk])
        status = dict_fetchone(cursor)
    return status


def get_category_by_id(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from  max_way_category 
                 where id = %s""", [pk])
        status = dict_fetchone(cursor)
    return status


def get_category_count():
    with closing(connection.cursor()) as cur:
        cur.execute("""select count(name) as name from max_way_category """)
        count_cat = dict_fetchone(cur)
    return count_cat


def news_count():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select name, count(title) as news_count from 
            max_way_category left join max_way_product on max_way_category.id=max_way_product.category_id
             group by name""")
        news = dict_fetchall(cursor)
    return news


def get_product_count():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select count(title) as title from max_way_product""")
        count_prod = dict_fetchone(cursor)
    return count_prod


def get_user():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from max_way_user""")
        users = dict_fetchall(cursor)
        return users


def get_order():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from max_way_order""")
        orders = dict_fetchall(cursor)
    return orders


def get_category():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from max_way_category""")
        categories = dict_fetchall(cursor)
    return categories


def get_product():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select * from max_way_product""")
        products = dict_fetchall(cursor)
    return products


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
