from requests import Session
from bs4 import BeautifulSoup
import json
import MySQLdb

def get_ret_json():

    url = 'https://www.ret.ru/?&pn=pline&view=list&gid=301745&prod=715101'

    session = Session()
    session = Session()
    session.headers.update(
        {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        })

    finished = []

    res = session.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')
    data = soup.find_all('span', attrs={'class': 'prpty_f', 'data-m': 'l'})


    for item in data:
        finished.append(
            {
                'id': item.get('data-pid'),
                'link_img': f"https://www.ret.ru{item.img.get('src')}",
                'name': item.find('a', class_='descript').string,
                'price': item.find('span', attrs={'class':'iconf rub', 'data-p': '@price'}).string,
                'link_item': f"https://www.ret.ru{item.a.get('href')}"
            }
        )

    with open('finished.json', 'w') as products:
            products.write(json.dumps(finished))
    
    return finished



def insert_to_db(finished):
    db = MySQLdb.connect(host="",user="",
                  password="",database="")


    c = db.cursor()
    for index, x in enumerate(finished):
        try:
            c.execute(f"""INSERT INTO main_otherproducts (title, other_id, photo, url, shop_id)
                    VALUES ('{finished[index]['name']}', '{finished[index]['id']}', '{finished[index]['link_img']}',
                    '{finished[index]['link_item']}', {10})""")
        except MySQLdb.IntegrityError:
            c.execute(f"""UPDATE main_otherproducts SET photo = '{finished[index]['link_img']}'
                    WHERE other_id = '{finished[index]['id']}' AND shop_id = {10}""")

    db.commit()

    for index, x in enumerate(finished):
        c.execute(f"""INSERT INTO main_otherproductparametrsdata (date, price, old_price, product_id)
                VALUES (SYSDATE(), '{finished[index]['price']}', '{finished[index]['price']}',
                (SELECT id FROM main_otherproducts WHERE shop_id = 10 AND other_id = '{finished[index]['id']}'))""")

    db.commit()


insert_to_db(get_ret_json())

