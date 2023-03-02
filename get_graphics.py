from requests import Session
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import MySQLdb
import time

session = Session()
session.headers.update(
    {
        'Host': 'partner.market.yandex.ru',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'X-Market-Core-Service': '<UNKNOWN>',
        'sk': 'u85cdeae0fc9ab23e06aa540b590d300f',
        'Content-Length': '81',
        'Origin': 'https://partner.market.yandex.ru',
        'Connection': 'keep-alive',
        'Referer': 'https://partner.market.yandex.ru/supplier/21962613/sales-statistics',
        'Cookie': 'yasc=U+aBFqN1jnuGXwU3PyuY1irpI8PDhkQaXpwa4wOyqfZUJuL807bqRQWvo/Q2dC/q5K0u; \
            i=5SMgvJI6RszG5TE5RrSHh6ugaSJUd4FTBz1cMqPUrCMwF2ODaqwVIbZMdGLRHhVmsXa7ZIkZ2Xvu0k1yOcg7HKxvcgE=',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }
)

def create_post_request(session, sku):

    url = 'https://partner.market.yandex.ru/api/resolve/?r=spaInitialStateResolvers/supplierSalesStatistics:resolveInitialState'

    date_to = (datetime.today() - relativedelta(days=1)).strftime('%Y-%m-%d')
    date_from = (datetime.today() - relativedelta(months=1)).strftime('%Y-%m-%d')

    path = f"/supplier//sales-statistics?tab=conversions&sortedBy=SHOWS&order=DESC&page=1\
            &searchString=&grouping=CATEGORIES&detail=DAY&dateFrom={date_from}&dateTo={date_to}&shows=true\
                &checkout=true&checkout_conversion=true&items_delivered=true&price=true&sales=true&shopSkus={sku}"

    params = {"params":[{"campaignId": ""}],
              "path": path}

    data = session.post(url, json=params).json()

    return data


def get_skus_from_db():

    dict_ids = dict()

    db = MySQLdb.connect(host="",user="",
                  password="",database="")

    c = db.cursor()

    c.execute(f"""SELECT id, other_id FROM main_yandexproducts""")

    items = c.fetchall()

    for item in items:

        dict_ids.update({item[0]: item[1]})

    return dict_ids


def get_shows(data):

    shows = []

    for item in data['results'][0]['data']['page']['charts']['data']['shows']['shows']['points']:

        shows.append(
            {
                datetime.utcfromtimestamp(item['timestamp']/1000).strftime('%d-%m-%Y'): item['value']
            }
        )

    return shows


def get_sales(data):

    sales = []

    for item in data['results'][0]['data']['page']['charts']['data']['checkout']['checkout']['points']:

        sales.append(
            {
                datetime.utcfromtimestamp(item['timestamp']/1000).strftime('%d-%m-%Y'): item['value']
            }
        )
    
    return sales


def get_graphics(shows, sales, product_id, graphics):

    graphics.update({product_id: {'sales': sales, 'shows':shows}})


def main():

    graphics = dict()
    
    dict_ids = get_skus_from_db()

    for product_id, other_id in dict_ids.items():

        print(f'Processing request for product ID {product_id}')
        data = create_post_request(session, other_id)

        print('Waiting 10 seconds')
        time.sleep(10)

        shows = get_shows(data)
        sales = get_sales(data)
            
        get_graphics(shows, sales, product_id, graphics)


    with open('graphics.json', 'w') as f:
        f.write(json.dumps(graphics))

    print('The script finished')


main()

