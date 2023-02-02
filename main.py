import json
from scraper import Scraper
from filter import Filter
from splitter import Splitter
from namelint import NameLint


def main():
    #load config
    f = open('config.json')
    config = json.load(f)

    pages = config['pages']
    subpage = config['subpage']

    #run scraper
    data = Scraper(pages, subpage).md_scrape()

    #init filter
    voucher = config['voucher']
    min_price = config['min_price']
    max_price = config['max_price']
    keywords = config['keywords']
    blacklist = config['blacklist']

    filtered_data = Filter(data, voucher, min_price, max_price, keywords, blacklist).filter()


    for i in range(len(filtered_data)):

        ebay_val = Scraper(pages, subpage).ebay_scrape(NameLint(list(filtered_data.values())[i]['title']).lint())
        
        filtered_data[list(filtered_data)[i]]['med_price'] = str(ebay_val[0]) + '€'
        filtered_data[list(filtered_data)[i]]['sales_week'] = len(ebay_val[1])
        filtered_data[list(filtered_data)[i]]['sales_month'] = len(ebay_val[2])
        filtered_data[list(filtered_data)[i]]['sales_total'] = len(ebay_val[3])
        filtered_data[list(filtered_data)[i]]['ebay_url'] = ebay_val[4]

    Splitter(filtered_data).discord()

if __name__ == '__main__':
    main()