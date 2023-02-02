import requests
from bs4 import BeautifulSoup
import statistics
from datetime import datetime

from logger import log


class Scraper:
    def __init__(self, pages, subpage):
        self.pages = pages
        self.subpage = subpage

    def md_scrape(self):
        deals = {}

        for i in range(1, self.pages + 1):
            print('running page ' + str(i))

            r = requests.get(f'https://mydealz.de/{self.subpage}?page={i}', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

            if r.status_code != 200:
                log(f'Error in mydealz request --- {r.status_code}')

            soup = BeautifulSoup(r.text, 'html.parser')

            try:
                threads = soup.find_all('article', 'thread')
            except:
                log(f'Error in md scraper: invalid HTML delivered: {str(soup)}')
                return

            for ind, thread in enumerate(threads):

                title = thread.find('a', 'cept-tt')['title']

                href1 = thread.find('a', 'cept-tt')

                href= href1['href']

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

                img1 = thread.find('img', 'thread-image')

                img = img1['src']

                deals['page-' + str(i) + '-deal-' + str(ind + 1)] = dict(title = title, href = href, price = price, discount = discount, img = img)
            print('finished page ' + str(i))

        return(deals)

    
    def ebay_scrape(self, pd_name):
        deals = {}

        pd_name = pd_name.replace(' ', '+')

        base_url = f'https://www.ebay.de/sch/i.html?_from=R40&_nkw={pd_name}&_sacat=0&LH_Sold=1&LH_Complete=1&rt=nc&LH_ItemCondition=1000&_ipg=240'

        r = requests.get(base_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

        if r.status_code != 200:
            log(f'Error occured in ebay scraper bad status code {r.status_code}')
            return

        soup = BeautifulSoup(r.text, 'html.parser')

        try:
            item = soup.find_all('div', 's-item__info')
        except:
            log(f'Error occured in ebay scraper invalid HTML delivered {str(soup)} ')
            return

        prices = []

        sales_month = []

        sales_week = []

        sales_total = []

        for i in range(1, len(item)):

            try:
                date = item[i].find_all('span', 'POSITIVE')[0].text.replace('Verkauft  ', '').split(' ')

                price = item[i].find_all('span', 'POSITIVE')[1].text.replace('EUR ', '').split(',')

                prices.append(int(float(price[0])))

                title = item[i].find('div', 's-item__title').text.replace('Neues Angebot', '')

                def get_month(mname):
                    mnum = datetime.strptime(mname, '%b').month
                    return(mnum)

                day = int(date[0].replace('.', ''))
                month = get_month(date[1].replace('Dez', 'Dec').replace('Mai', 'May').replace('Mär', 'Mar').replace('Okt', 'Oct'))
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

            except:
                log(f'Error occured in ebay scraper in line 94: {str(item)}')

        try:
            med_prices = statistics.median(prices)
        except statistics.StatisticsError:
            med_prices = 0

        return([med_prices, sales_week, sales_month, sales_total, base_url])