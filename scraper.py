# imports
import requests
from bs4 import BeautifulSoup
import statistics
from datetime import datetime

from logger import get_module_logger

# mydealz scraper
def md_scrape(pages, subpage):
    # define dict
    deals = {}

    # scrape through every page
    for i in range(1, pages + 1):
        print('running page ' + str(i))

        r = requests.get(f'https://mydealz.de/{subpage}?page={i}', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

        # error handling
        if r.status_code != 200:
            get_module_logger('mydealz_scraper').info('mydealz delivered invalid status code')
            return

        # init bs4
        soup = BeautifulSoup(r.text, 'html.parser')

        # check for valid html
        try:
            threads = soup.find_all('article', 'thread')
        except:
            get_module_logger('mydealz_scraper').info('invalid html')
            return

        # parse every thread
        for ind, thread in enumerate(threads):

            try:
                title = thread.find('a', 'cept-tt')['title']

                href1 = thread.find('a', 'cept-tt')

                href= href1['href']
            except:
                continue

            #check if thread is a deal
            try:
                price = thread.find('span', 'thread-price').contents[0]

            except AttributeError:
                continue

            #check if deal is a voucher
            if '%' in price:
                discount = price
                price = None
            else:
                try:
                    discount = thread.find('span', 'space--ml-1').contents[0]
                except (IndexError, AttributeError):
                    discount = None
            
            # get img
            img1 = thread.find('img', 'thread-image')

            img = img1['src']

            # append deal to list
            deals['page-' + str(i) + '-deal-' + str(ind + 1)] = dict(title = title, href = href, price = price, discount = discount, img = img)
        print('finished page ' + str(i))


    return(deals)

# scrape ebay sold products
def ebay_scrape(pd_name):

    # edit product name
    pd_name = pd_name.replace(' ', '+')

    # request ebay
    base_url = f'https://www.ebay.de/sch/i.html?_from=R40&_nkw={pd_name}&_sacat=0&LH_Sold=1&LH_Complete=1&rt=nc&LH_ItemCondition=1000&_ipg=240'

    r = requests.get(base_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

    # error handling
    if r.status_code != 200:
        get_module_logger('ebay_scraper').info('ebay request delivered invalid status code')
        return

    # init bs4
    soup = BeautifulSoup(r.text, 'html.parser')

    # error handling
    try:
        item = soup.find_all('div', 's-item__info')
    except:
        get_module_logger('ebay-scraper').info('ebay request delivered invalid html')
        return
    
    # parse number of results
    count = soup.find('h1', 'srp-controls__count-heading').find('span', 'BOLD').text.replace('.', '')


    prices = []

    sales_month = []

    sales_week = []

    sales_total = []

    item_count = len(item)

    if item_count == 0:
        return([0, 0, 0, 0, base_url])

    if int(count) <= len(item):
        item_count = int(count) + 1

    # loop through every item
    for i in range(1, item_count):

        date = item[i].find_all('span', 'POSITIVE')[0].text.replace('Verkauft  ', '').split(' ')

        try:
            price = item[i].find_all('span', 'POSITIVE')[1].text.replace('EUR ', '').split(',')
        except:
            continue

        prices.append(int(float(price[0].replace('.', ''))))

        def get_month(mname):
            mnum = datetime.strptime(mname, '%b').month
            return(mnum)

        
        # analize sale date
        day = int(date[0].replace('.', ''))
        month = get_month(date[1].replace('Dez', 'Dec').replace('Mai', 'May').replace('Mrz', 'Mar').replace('Okt', 'Oct'))
        year = int(date[-1])

        insertion_date = datetime(year, month, day)

        time_between_insertion = datetime.now() - insertion_date

        if time_between_insertion.days <= 7:
            sales_week.append(insertion_date)
            sales_month.append(insertion_date)
            sales_total.append(insertion_date)
            continue
        elif time_between_insertion.days <= 30:
            sales_month.append(insertion_date)
            sales_total.append(insertion_date)
            continue
        else:
            sales_total.append(insertion_date)

    # calculate median price
    try:
        med_prices = statistics.median(prices)
    except statistics.StatisticsError:
        get_module_logger('scraper').info(prices)
        med_prices = 0

    return([med_prices, sales_week, sales_month, sales_total, base_url])
