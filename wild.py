from requests import Session
import json


def get_json_wild(query):
    
    session = Session()
    session.headers.update(
        {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        })

    finished = []
    counter = 1

    for i in range(1, 21):

        url = 'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1'\
            '&couponsGeo=2,12,7,3,6,18,21&curr=rub&dest=-971633&emp=0&lang=ru&locale=ru&page=' + str(i) + '&pricemarginCoeff=1.0&query=' + str(query) + '&reg=0'\
            '&regions=80,64,83,4,38,33,70,68,69,86,30,40,48,1,22,66,31&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false'

        res = session.get(url)

        data = res.json()

        if not data['data']['products']:
                break

        for index, x in enumerate(data['data']['products']):
            finished.append({'index': counter, 'id': data['data']['products'][index]['id'], 'name': data['data']['products'][index]['name']})
            counter += 1
    

    with open('finished.json', 'w') as products:
        products.write(json.dumps(finished))


get_json_wild('xbox')

