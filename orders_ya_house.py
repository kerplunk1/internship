import MySQLdb
import json

def get_returned_json_from_db():

    data = []

    db = MySQLdb.connect(host='', user='',
                        password='', database='')
    
    c = db.cursor()
    c.execute(f"""SELECT return_json FROM  json_orders
                WHERE created_at BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW()""")

    for item in c.fetchall():

        row = json.loads(item[0])

        for index, x in enumerate((row['result']['orders'])):
            warehouse_id = row['result']['orders'][index]['items'][0]['warehouse']['id']
            title = row['result']['orders'][index]['items'][0]['warehouse']['name']

            data.append(
                {
                'id': warehouse_id,
                'title': title
                }
            )

    return data


def insert_into_db(data):
    db = MySQLdb.connect(host="",user="",
                  password="",database="")

    c = db.cursor()
    for index, x in enumerate(data):
        try:
            c.execute(f"""INSERT INTO main_yandexhouse (id, title, stock_id)
                    VALUES ({data[index]['id']}, '{data[index]['title']}', NULL)""")
        except MySQLdb.IntegrityError:
            pass

    db.commit()


insert_into_db(get_returned_json_from_db())

