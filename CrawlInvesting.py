# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 11:09:39 2018

@author: zerow
"""
import pandas as pd
import numpy as np
import xlrd
import time
import Utilities
import WebLinkedList
from queue import Queue
import threading
import pyodbc 
import datetime

def LoadAssetInfo(CsvFile):
    """ Load asset info from csv """
    AssetDict = dict()
    TickerData = Utilities.ExtractCsvInfo(TickerFile)
    AssetDict = Utilities.ExtractAssetInfo(TickerData)
    return AssetDict

def CreateWebsList(AssetInfo, TimePause, TimesFetch):
    """ Get web pages """ 
    AssetTickers = list(AssetInfo.keys())
    # Create a linked list for every asset
    WebsLists = dict()
    for s in AssetTickers:
        WebsLists[s] = WebLinkedList.WebList()
    # Start crawling
    for t in range(TimesFetch):
        for s in AssetTickers:
            AssetLink = AssetInfo[s]
            [tempWebPage, tempTime] = Utilities.FetchWebPage(AssetLink)
            tempWebNode = WebLinkedList.WebNode(tempWebPage, tempTime)
            WebsLists[s].Append(tempWebNode)
        time.sleep(TimePause)
    return WebsLists

def ParseCurrentPrices(WebsLists, AssetInfo):
    """ Store the prices into a df """
    TimesFetch = next (iter (WebsLists.values())).length
    AssetTickers = list(WebsLists.keys())
    Columns = ['Time', 'Ticker', 'Price']
    FetchedPrices = pd.DataFrame(np.zeros([TimesFetch * \
                    len(AssetTickers), 3]), columns = Columns)
    TimeLine = list()
    Counter = 0
    for s in AssetTickers:
        tempWebList = WebsLists[s]
        for t in range(TimesFetch):
            [webpage, CurrentTime] = tempWebList.GetWebPage(t)
            sPrice = Utilities.ParseWebPage(webpage)
            FetchedPrices.loc[Counter, [Columns[0]]] = CurrentTime
            FetchedPrices.loc[Counter, [Columns[1]]] = s
            FetchedPrices.loc[Counter, [Columns[2]]] = sPrice
            TimeLine.append(CurrentTime)
            Counter += 1
    return FetchedPrices

def InsertIntoTable(conn, FetchedPrices, TableName, row):
    """ Insert the records into SQL table """
    cursor = conn.cursor()
    # Insert into SQL
    CommandPre = "insert into " + TableName + " (Time, Ticker, Price) values "
    InsertData = "('{}', '{}', {:.2f})".format(FetchedPrices.loc[row]['Time'], \
                  FetchedPrices.loc[row]['Ticker'], \
                  FetchedPrices.loc[row]['Price'])
    Command = CommandPre + InsertData
    cursor.execute(Command)
    conn.commit()
    
def PrintTable(conn, TableName):
    """ Print the table out """
    cursor = conn.cursor()
    cursor.execute("select * from " + TableName)
    for row in cursor.fetchall():
        print (row[0], row[1], row[2])

###### Main ######
if __name__ == "__main__":
    
    # Start time
    StartTime = time.clock()
    
    # Set up the dict to store information of each asset
    TickerFile = 'Tickers.xlsx'
    AssetInfo = LoadAssetInfo(TickerFile)
    
    # Traverse time
    TimePause = 0
    # The number of times to crawl, you can also change the inside loop into
    # while True
    TimesFetch = 100
        
    # Collect price data
    WebsLists = CreateWebsList(AssetInfo, TimePause, TimesFetch)
    FetchedPrices = ParseCurrentPrices(WebsLists, AssetInfo)
    
    # Output to SQL
    conn = pyodbc.connect('DRIVER = {SQL Server};\
                         SERVER = <Your Server Name>;\
                         Trusted_Connection = yes\
                         DATABASE = <Your Database Name>;\
                         UID = <Your Username>;\
                         PWD = <Your Password>')
    TableName = "<Your Table Name>"
    for t in range(len(FetchedPrices)):
        InsertIntoTable(conn, FetchedPrices, TableName, t)
    # Take a look at the table in SQL
    PrintTable(conn, TableName)
    
    # End time
    EndTime = time.clock()
    print ('Time used is: ', EndTime - StartTime, ' seconds\n')