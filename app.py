# -*- coding: utf-8 -*-
"""
Created on Wed May 19 23:55:00 2021

@author: venkatesh surampally
"""

from pywebio.output import *
from pywebio.input import * 
import time
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
import pandas as pd
import urllib.request
import json
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from keras.models import load_model
app=Flask(__name__)
def predict():
    def forecastbtc(prices,days):
        loaded_model = load_model("bitcoin.h5")
        use=np.array(prices[-21:-1])
        use=use.reshape(1,20,1)
        use=use/100000
        predicts=float(loaded_model.predict(use))*100000
        scale=(prices[-1]+1000)/predicts
        final=[]
        day=0
        while(day<days):
            day+=1
            use=np.array(prices[-20:])
            use=use.reshape(1,20,1)
            use=use/100000
            predicts=float(loaded_model.predict(use))*100000
            final.append(predicts*scale)
            prices.append(predicts*scale)
        return final
    today=str(datetime.datetime.today())[:10]
    past=str(datetime.datetime.today()-datetime.timedelta(days=30))[:10]
    put_markdown('The Cryptocurrency')
    put_text("Use this app to know the statistics of Bitcoin and Dogecoin.")
    with popup("Caution!"):
        put_text("The predictions are just for educational purposes, please refrain from relying upon it!")
    condition = select("Choose the type of Cryptocurrency", ['Bitcoin', 'Dogecoin'])
    with popup("Note"):
        put_text("We are purely relying upon the data provideb by various websites, we are not responsible for any mistakes prent in the data.")
    if condition=='Bitcoin':
        url = 'https://api.nomics.com/v1/currencies/sparkline?key=63a6fb7bcdc2345fac6baed3afd92150&ids=BTC&start='+past+'T00%3A00%3A00Z&end='+today+'T00%3A00%3A00Z'
        k=urllib.request.urlopen(url).read()
        o=json.loads(k)
        times=o[0]['timestamps']
        times=list(map(lambda x:x[:10],times))
        prices=o[0]['prices']
        prices=list(map(float,prices))
        plt.figure(figsize=(20,5))
        plt.plot(times,prices)
        plt.title('Bitcoinprice vs time')
        plt.xticks(rotation=90)
        plt.xlabel('time')
        plt.ylabel('price')
        plt.savefig('btcprice.png')
        put_image(open('btcprice.png', 'rb').read(),width='3000px')
        days1 = select("How many days into the future you want the predictions.", [1,2,3,4,5,6,7,8,9,10])
        with popup("Caution!"):
            put_text("The predictions are just for educational purposes, prices are lot dependent on the external factors!")
        predicted=forecastbtc(prices,days1)
        plt.figure(figsize=(20,5))
        plt.plot([i for i in range(1,days1+1)],predicted)
        plt.title('Bitcoinprice prediction vs time')
        plt.xticks(rotation=90)
        plt.xlabel('time')
        plt.ylabel('price')
        plt.savefig('btcpricepred.png')
        put_image(open('btcpricepred.png', 'rb').read(),width='3000px')
app.add_url_rule('/tool','webio_view',webio_view(predict),methods=["GET","POST","OPTIONS"])
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(predict, port=args.port)