
from datetime import datetime

import quandl
import numpy

quandl.ApiConfig.api_key="K6qMLKTnVQuUYut4siUX"

from datetime import date
from dateutil.relativedelta import relativedelta

import cx_Oracle

def connect():
    global connection
    connection = cx_Oracle.connect('shrey/oracle123@localhost/XE')
    global cursor
    cursor=connection.cursor()


class datfet:
    
    @classmethod
    def fetch(cls,symbol,flag):
        start=0
        if(flag == 1): #10 days
            start = date.today() + relativedelta(days = -10)
        elif(flag == 2): #6 months
            start = date.today() + relativedelta(months = -6)
        elif(flag == 3): #1 year
            start = date.today() + relativedelta(years = -1)
        start = str(start)
        end = str(date.today())
        print("NSE/" + symbol)
        data = quandl.get("NSE/" + symbol, start_date=start, end_date=end,returns="numpy")
        date_data = [data[i][0] for i in range(len(data))]
        price_data = [data[i][4] for i in range(len(data))]
        cls.store(symbol,date_data[len(data)-1])
        return date_data,price_data
