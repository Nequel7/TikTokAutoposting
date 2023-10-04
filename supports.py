import random
import proxy_data
import os


def random_proxy():
    return random.choice(proxy_data.proxy)


def account_exists(account):
    for acc in os.listdir('cookies'):
        if acc.split("_")[0] == account:
            return True
    return False
