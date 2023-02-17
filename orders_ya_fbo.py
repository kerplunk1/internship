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

        for x in (row['result']['orders']):
            for i in x['items']:
                order_id = x['id']
                creation_date = x['creationDate']
                order = i['count']
                order_r = i['prices'][0]['total']
                status = x['status']
                product_id = i['marketSku']
                house_id = i['warehouse']['id']

                data.append({
                    'order_id': order_id,
                    'date': creation_date,
                    'order': order,
                    'order_r': order_r,
                    'status': status,
                    'product_id': product_id,
                    'house_id': house_id
                })    
    
    return data



def insert_into_db(data):
    
    db = MySQLdb.connect(host="",user="",
                  password="",database="")

    c = db.cursor()
    for index, x in enumerate(data):
        try:
            c.execute(f"""INSERT INTO main_yandexfbo (`date`, `order_id`, `order`, `order_r`, `status`, `product_id`, `shop_id`, `house_id`)
            VALUES (STR_TO_DATE("{data[index]['date']}", "%Y-%m-%d"), '{data[index]['order_id']}', {data[index]['order']},
            {data[index]['order_r']}, '{data[index]['status']}', {data[index]['product_id']}, {1}, {data[index]['house_id']})""")
        except MySQLdb.IntegrityError:
            print('error')

    db.commit()


insert_into_db(get_returned_json_from_db())

