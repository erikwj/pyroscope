import random
import requests
import time

HOSTS = [
    'us-east',
    'eu-north',
    'ap-south',
]

VEHICLES = [
    'bike',
    'scooter',
    'car',
]

groupby_terms_all = ['Make', 'Model', 'Model Year']
groupby_terms_one = ['Model Year']

if __name__ == "__main__":
    print(f"starting load generator-v")
    time.sleep(3)
    while True:
        host = HOSTS[random.randint(0, len(HOSTS) - 1)]
        groupby=groupby_terms_one
        isBig=True

        if host == HOSTS[0]:
            groupby=groupby_terms_all
                
        # when default is set to True, the difference between the queryparameters is more significant
        if host == HOSTS[2]:
            isBig=False
       

        params = {
            "isBig": isBig,
            "search_terms": groupby
        }

        print(f"making query {groupby} to {host}")
        try:
            resp = requests.get(f'http://{host}:5000/vehicles', params=params)
            resp.raise_for_status()
            print(f"received {resp}")
        except BaseException as e:
            print (f"http error {e}")

        time.sleep(random.uniform(0.1, 0.2))
