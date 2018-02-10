# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 15:22:54 2018

@author: zerow
"""
import pandas as pd
import numpy as np
import xlrd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen    
import WebLinkedList
import datetime

def ExtractCsvInfo(CsvFile):
    """ Read excel file data """
    TickerData = pd.read_excel(CsvFile)
    TickerData = TickerData.drop_duplicates('Ticker')
    TickerData.reset_index(drop = True, inplace = True)
    return TickerData

def ExtractAssetInfo(TickerData):
    """ Extract asset info from csv """
    AssetDict = dict()
    for i in range(len(TickerData)):
        TempTicker = TickerData.loc[i, ['Ticker']][0]
        TempLink = TickerData.loc[i, ['Link']][0]
        AssetDict[TempTicker] = TempLink
    return AssetDict

def FetchWebPage(link):
    """ Collect the web page from url """
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        webpage = urlopen(req).read()
    except urllib.error.URLError as e:
            print(e.reason)
    CurrentTime = datetime.datetime.now().isoformat()
    return [webpage, CurrentTime]

def ParseWebPage(webpage, ID = 'last_last'):
    """ Parse the website information with prices scraped """
    try:
        bs = BeautifulSoup(webpage, 'lxml')
        # Find a list of all span elements
        spans = bs.find_all('span', id = ID)
        # Create a list of lines corresponding to element texts
        lines = [span.get_text() for span in spans]
        strPrice = lines[0]
        # Check if there is ',' in the string number
        if ',' not in strPrice:
            CurrentPrice = float(strPrice)
        else:
            CurrentPrice= float(strPrice.replace(",",""))
    except:
        print('Fail to parse asset info')
        return
    return CurrentPrice
    
if __name__ == '__main__':
    print ('Completed compiling utilities.')
