import locale
from locale import atof 


from logger import get_module_logger


# apply filters
def filter(data, voucher, min_price, max_price, keywords, blacklist):

    # set locale
    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

    # init dict
    filtered_deals = {}

    # loop throught every deal
    for i in range(len(data)):
    
        # convert into list
        val = list(data.values())[i]

        # check if deal is discounted
        if '<' in str(val['discount']):
            val['discount'] = None

        #check for keywords
        if keywords != []:
            res = any(ele.lower() in val['title'].lower() for ele in keywords)
            #skip deal if keyword not found
            if res == False:
                continue

        #check for blacklisted words
        if blacklist != []:
            res = any(ele.lower() in val['title'].lower() for ele in blacklist)
            #skip deal if keyword is blacklisted
            if res == True:
                continue

        #check for min_price & max_price    
        if val['price'] != None and val['price'].upper() != 'KOSTENLOS':
            p = val['price'].replace('€', '').replace('.', '')
            

            price = int(float(p.replace(',', '.')))
            
            
            if min_price and max_price:
                if min_price <= price <= max_price:
                    #price is in range
                    pass
                else:
                    continue
            elif min_price:
                if price >= min_price:
                    # price is above min_price
                    pass
                else:
                    continue
            elif max_price:
                if price <= max_price:
                    # price is below max_price
                    pass
                else:
                    continue

        elif val['price'] == None and voucher == False:
            continue

        filtered_deals['deal-' + str(i + 1)] = dict(title = val['title'], href = val['href'], price = val['price'], discount = val['discount'], img = val['img'])


    return(filtered_deals)
