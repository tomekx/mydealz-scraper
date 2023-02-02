from dischook import DiscHook
import time

from logger import log

class Splitter:
    def __init__(self, data):
        self.data = data

    def discord(self):

        try:
            for i in self.data:
                time.sleep(1)
                DiscHook(self.data[i]['title'], self.data[i]['href'], self.data[i]['price'], self.data[i]['discount'], self.data[i]['img'], self.data[i]['med_price'],
                self.data[i]['sales_week'], self.data[i]['sales_month'], self.data[i]['sales_total'], self.data[i]['ebay_url'] ).send_hook()
        except:
            log(f'error occured in splitter: {str(self.data)}')