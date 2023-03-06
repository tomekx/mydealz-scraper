from scraper import md_scrape, ebay_scrape
from filter import filter
from splitter import Splitter
from namelint import lint

from logger import get_module_logger


def start(config):
    # log config
    get_module_logger('setup').info(config)

    # set variables
    pages = config['pages']
    subpage = config['subpage']

    #run scraper
    data = md_scrape(pages, subpage)

    #init filter
    voucher = config['voucher']
    min_price = config['min_price']
    max_price = config['max_price']
    keywords = config['keywords']
    blacklist = config['blacklist']

    filtered_data = filter(data, voucher, min_price, max_price, keywords, blacklist)




    for i in range(len(filtered_data)):

        ebay_val = ebay_scrape(lint(list(filtered_data.values())[i]['title']))
        
        filtered_data[list(filtered_data)[i]]['med_price'] = str(ebay_val[0]) + '€'
        filtered_data[list(filtered_data)[i]]['sales_week'] = len(ebay_val[1])
        filtered_data[list(filtered_data)[i]]['sales_month'] = len(ebay_val[2])
        filtered_data[list(filtered_data)[i]]['sales_total'] = len(ebay_val[3])
        filtered_data[list(filtered_data)[i]]['ebay_url'] = ebay_val[4]

    Splitter(filtered_data).discord()
