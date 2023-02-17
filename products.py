import MySQLdb
import json

def get_returned_json_from_db():

    data = []

    db = MySQLdb.connect(host='', user='',
                        password='', database='')
    
    c = db.cursor()
    c.execute(f"""SELECT return_json FROM  json_products
                WHERE created_at BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW()""")
    
    for item in c.fetchall():

        row = json.loads(item[0])

        for index, x in enumerate(row['result']['offerMappingEntries']):
            id = row['result']['offerMappingEntries'][index]['mapping']['marketSku']
            title = row['result']['offerMappingEntries'][index]['offer']['name']
            
            try:
                picture = row['result']['offerMappingEntries'][index]['offer']['pictures'][0]
            except IndexError:
                picture = None
            
            barcode = row['result']['offerMappingEntries'][index]['offer']['barcodes'][0]
            
            try:
                url = row['result']['offerMappingEntries'][index]['offer']['urls'][0]
            except KeyError:
                url = None
            
            other_id = row['result']['offerMappingEntries'][index]['offer']['shopSku']

            data.append(
                {
                    'id': id,
                    'title': title,
                    'picture': picture,
                    'barcode': barcode,
                    'url': url,
                    'other_id': other_id
                }                
            )

    return data


def insert_to_db(data):
    db = MySQLdb.connect(host="",user="",
                  password="",database="")

    c = db.cursor()
    for index, x in enumerate(data):
        try:
            c.execute(f"""INSERT INTO main_yandexproducts (id, title, status, barcode, other_id, photo, url, shop_id)
                    VALUES ({data[index]['id']}, '{data[index]['title']}', {1}, '{data[index]['barcode']}',
                    '{data[index]['other_id']}', '{data[index]['picture']}', '{data[index]['url']}', {1})""")
        except MySQLdb.IntegrityError:
            c.execute(f"""UPDATE main_yandexproducts SET photo = '{data[index]['picture']}', barcode = '{data[index]['barcode']}'
                    WHERE id = {data[index]['id']} AND other_id = '{data[index]['other_id']}' AND shop_id = {1}""")

    db.commit()


# with open('file.json', 'w') as file:
#     file.write(json.dumps(get_returned_json_from_db()))

insert_to_db(get_returned_json_from_db())