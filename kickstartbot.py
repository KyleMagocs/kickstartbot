import json
from bs4 import BeautifulSoup
import requests
import time
import datetime
from money_parser import price_str
ks_addr = 'https://www.kickstarter.com/projects/markkleeb/wonderville-arcade'
post_addr = ''  # you'll need to get your own slack bot token for this


encoded_data = json.dumps({'text': 'hey looks like I\'m starting up the app again, sorry',}).encode('utf-8')

money_string = '${:,.2f}'


def get_ks_total():
    page = requests.get(url=ks_addr)
    soup = BeautifulSoup(page.text, 'html.parser')
    things = soup.find_all(class_='ksr-green-700')
    for thing in things:

        if '$' in thing.text:
            return thing.text
    return None

def get_ks_backers():
    page = requests.get(url=ks_addr)
    soup = BeautifulSoup(page.text, 'html.parser')
    things = soup.find_all(class_='block type-16 type-24-md medium soft-black')
    for thing in things:
        return thing.text
    return None

init_backers = get_ks_backers()
init_total = get_ks_total()


def send_slack_msg(text, actually_send=True):
    if actually_send:
        r = requests.post(url=post_addr, data=json.dumps({'text': text, }).encode('utf-8'), headers={'Content-Type': 'application/json'})
    else:
        print(text)


    # send_slack_msg(f'hey looks like I\'m starting up the app again, sorry')

current_backers=price_str(init_backers)
current_total=price_str(init_total)

while True:

    try:

        new_backers=price_str(get_ks_backers())
        new_total=price_str(get_ks_total())

        print(price_str(new_total))
        print('{0:.1%}'.format(float(new_total) / 70000.))
        print(datetime.datetime.now())

        if(new_backers != current_backers or new_total != current_total):
            backer_diff = int(new_backers) - int(current_backers)
            price_diff = money_string.format(int(new_total) - int(current_total))
            goal_perc = '{0:.1%}'.format(float(new_total) / 70000.)
            emoji = ':crying_cat_face::crying_cat_face: oh no :crying_cat_face::crying_cat_face:'

            if (int(int(new_total) - int(current_total)) > 0):
                emoji = ':bug: inchin\' along :bug:'
            if (int(int(new_total) - int(current_total)) >= 40):
                emoji = ':money-money: cool! :money-money:'
            if (int(int(new_total) - int(current_total)) >= 100):
                emoji = ':moneybag::moneybag: hell yeah! :echeese::moneybag::moneybag:'
            if (int(int(new_total) - int(current_total)) >= 200):
                emoji = ':echeese::cliffy-parrot: COWABUNGA, CHEESE FREAKS :cliffy-parrot::echeese:'
            if (int(int(new_total) - int(current_total)) >= 1000):
                emoji = 'https://media2.giphy.com/media/4FmAj1XiioCVW/giphy.gif'

            current_backers = new_backers
            current_total = new_total
            format_total = money_string.format(float(current_total))


            send_slack_msg(f'Now at {current_backers} backers (a difference of {backer_diff})\n'
                           f'With a total of {format_total} (a difference of {price_diff})\n'
                           f'We\'re at {goal_perc} of our goal!\n'
                           f'{emoji}')

        time.sleep(60 * 2)
    except Exception as e:
            print('Oh shit I went and crashed like some sort of lowlife.  Yikes.  :echeese:')
            print(e)
