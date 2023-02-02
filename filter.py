import locale

from logger import log

class Filter:
    
    def __init__(self, data, voucher, min_price, max_price, keywords, blacklist):
        self.data = data
        self.voucher = voucher
        self.min_price = min_price
        self.max_price = max_price
        self.keywords = keywords
        self.blacklist = blacklist

    def filter(self):
        locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')

        filtered_deals = {}

        for i in range(len(self.data)):
            try:
                val = list(self.data.values())[i]

                if '<' in str(val['discount']):
                    val['discount'] = None

                #check for keywords
                if self.keywords != []:
                    res = any(ele.lower() in val['title'].lower() for ele in self.keywords)
                    #skip deal if keyword not found
                    if res == False:
                        continue

                #check for blacklisted words
                if self.blacklist != []:
                    res = any(ele.lower() in val['title'].lower() for ele in self.blacklist)
                    #skip deal if keyword is blacklisted
                    if res == True:
                        continue

                #check for min_price & max_price    
                if val['price'] != None and val['price'] != 'KOSTENLOS':
                    p = val['price'].replace('€', '').replace('.', '')
                    price = int(float(locale.atof(p)))
                    
                    if self.min_price and self.max_price:
                        if self.min_price <= price <= self.max_price:
                            #price is in range
                            pass
                        else:
                            continue
                    elif self.min_price:
                        if price >= self.min_price:
                            # price is above min_price
                            pass
                        else:
                            continue
                    elif self.max_price:
                        if price <= self.max_price:
                            # price is below max_price
                            pass
                        else:
                            continue

                elif val['price'] == None and self.voucher == False:
                    continue

                filtered_deals['deal-' + str(i + 1)] = dict(title = val['title'], href = val['href'], price = val['price'], discount = val['discount'], img = val['img'])

            except:
                log(f'Error occured in filter on data set {str(self.data)}')

        return(filtered_deals)