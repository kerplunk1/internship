import MySQLdb
import json


with open('graphics.json', 'r') as graphics:
    data = json.load(graphics)

db = MySQLdb.connect(host="",user="",
                  password="",database="")

c = db.cursor()

for product_id in data:

    for sale in data[product_id]['sales']:
        for date, value in sale.items():
            c.execute(f"""UPDATE main_yandexproductparametrsdata
                        SET add_cart = {value}
                        WHERE product_id = {product_id} AND `date` = STR_TO_DATE("{date}", "%d-%m-%Y")""")
            
    for show in data[product_id]['shows']:
        for date, value in show.items():
            c.execute(f"""UPDATE main_yandexproductparametrsdata
                        SET hits = {value}
                        WHERE product_id = {product_id} AND `date` = STR_TO_DATE("{date}", "%d-%m-%Y")""")

db.commit()

