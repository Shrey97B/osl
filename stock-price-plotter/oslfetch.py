
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
    
       @classmethod
    def store(cls,symbol,cur_date):
        connect()
        cur_date = str(cur_date)
        cur_date = cur_date[:10]
        print(cur_date)
        try:
            query="INSERT INTO record VALUES(:value1,to_date(:value2,'YYYY-MM-DD'))"
            cursor.execute(query,(symbol,cur_date))
        except Exception as e:
            print(e)
        connection.commit()
        connection.close()

    @classmethod
    def finter(cls,symbol,datlist):
        connect()
        try:
            selq = "select searchdate from record where symbol=:value1 and searchdate between to_date(:value2,'YYYY-MM-DD') and to_date(:value3,'YYYY-MM-DD') order by  searchdate"
            cursor.execute(selq,(symbol,datlist[0],datlist[len(datlist)-1]))
            res = cursor.fetchall()
           
        except Exception as e:
            print(e)
        connection.commit()
        connection.close()
        return res
