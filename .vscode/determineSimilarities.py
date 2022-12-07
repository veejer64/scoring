import sqlite3
import csv
import math
from time import time
from array import *
from vutil.comparitors import calcSim
from vutil.comparitors import rSubset
from vutil.comparitors import calcLocalHA
from vutil.db import init
from vutil.db import buildfeatures
from vutil.db import initInventory
from vutil.db import metricWriter
from vutil.db import writeCombRec
from vutil.db import writeDocRec


# Maybe use?
#from scipy import spatial
#import en_core_web_sm
#import pandas as pd
#import numpy as np 
#import nltk

# determineSimilarities - VJ McHargue/veejer@gmail.com
#
# The purpose of this script is to determine how similar assets in different deployment environments are.  The premise of this is that
# a deployment environment can be described as a collection of assets, each with attributes that describe the characteristics of the asset.
# If we translate this data into a document, where the elements are uninquely formed items comprised of asset attributes, then we
# can build lists/sets/matrices and perform mathematical or data science analysis on those mathematical collections.  This is much simpler than 
# line by line comparitive analysis.
#
# If we can build a document manifest of deployment environments and assets, we perform similarity/ranking/recommendations/etc. via 
# data science techniques very similar to how internet search engines work.
#
# The first comparison test being done here is a very simple artithmetic percentage calculation.  For this POC, the data set is also very simple, 
# and the document elements are composed to not be very granular.  However, the key comparison module processing remains the same if more granularity is needed,
# the data preprocessing will just need adjusted, and scaffolding code modified.
# 
# Next work to POC is implemtation of cosine similarities, Jacquard coefficient index similarities.  More TBD.



def genCombs():
    # Process inventory/determine combinations.
    try:
 
        con = sqlite3.connect('./inventory.db')
        cursor = con.cursor()

        sql_select_query = cursor.execute(
            "SELECT DISTINCT url FROM inventory"
        )
        records = cursor.fetchall()
        urls = []
        for row in records:
            urlR = row[0]
            urls.append(urlR)
        cursor.close()
        
        con = sqlite3.connect('./inventory.db')
        cursor = con.cursor()
        for urlY in urls:
            sql_select_query = cursor.execute(
                "SELECT DISTINCT datacenter FROM inventory WHERE url=?", [urlY]
            )
            records = cursor.fetchall()
            dcs = []
            dcc = []
            for row in records:
                dcR = row[0]
                dcs.append(dcR)
            dcc = rSubset(dcs)
            if len(dcc) == 0:
                metricWriter("SINGLE SITE",urlY,'','','','',1,'','')
                print("SINGLE SITE DETECTED:",urlY)
            for element in dcc:
                writeCombRec(urlY,element)
            
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from inventory table", error)
    finally:
        if con.close():
            print("The SQLite connection is closed")

def genDoc(dc,url):
    # Iterate through inventory, build lists of documents with asset attributes.
    try:
        con = sqlite3.connect('./inventory.db')
        cursor = con.cursor()
        sql_select_query = cursor.execute(
            "SELECT feature FROM inventory WHERE datacenter=? AND url=?", (dc, url)
        )
        records = cursor.fetchall()
        items = []
        for row in records:
            feature = row[0]
            items.append(feature)
        cursor.close()
        return items

    except sqlite3.Error as error:
        print("Failed to read data from inventory table", error)
    finally:
        if con.close():
            print("The SQLite connection is closed")

def getDC():
    try:
        con = sqlite3.connect('./inventory.db')
        cursor = con.cursor()

        sql_select_query = """select distinct datacenter, url from inventory"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        items = []
        for row in records:
            dc = row[0]
            url = row[1]
            items.append([dc,url])
        cursor.close()
        return items

    except sqlite3.Error as error:
        print("Failed to read data from inventory table", error)
    finally:
        if con.close():
            print("The SQLite connection is closed")

def processDocuments():
    items = getDC()

    for i in range(len(items)) : 
        features = genDoc(items[i][0],items[i][1])
        writeDocRec(items[i][0],items[i][1],' ' . join(str(element) for element in features))    
    return

def startSiteSimAnalysis():
    try:
            print(" .    Site similarity analysis starting...")
            con = sqlite3.connect('./inventory.db')
            con2 = sqlite3.connect('./inventory.db')
            cursor = con.cursor()

            sql_select_query = cursor.execute(
                "SELECT url, combination1, combination2 FROM combinations ORDER BY url"
            )
            records = cursor.fetchall()
            items = []
            for row in records:
                u1 = row[0]
                c1 = row[1]
                c2 = row[2]
                cursor2 = con2.cursor()
                sql_select_query_comb = cursor2.execute(
                "SELECT datacenter, url, document FROM documents WHERE (url = ? AND datacenter = ?) OR (url = ? AND datacenter = ?)",(u1,c1,u1,c2))
                records2 = cursor2.fetchall()
                d3 = []
                u3 = []
                doc3 = []
                for row in records2:
                    d3.append(row[0])
                    u3.append(row[1])
                    doc3.append(row[2])
                cursor2.close()
                calcSim(u3,d3,doc3)
            print(" .    Analysis complete.")
            cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from documents table", error)
    finally:
        if con.close():
            print("The SQLite connection is closed")
        if con2.close():
            print("The SQLite connection is closed")

def startLocalHAAnalysis():
    try:
        print(" .    Local HA analysis starting...")
        con2 = sqlite3.connect('./inventory.db')
        cursor2 = con2.cursor()
        sql_select_query_comb = cursor2.execute(
        "SELECT datacenter, url, document FROM documents ORDER BY url")
        records2 = cursor2.fetchall()
        
        for row in records2:
            d3=row[0]
            u3=row[1]
            doc3=row[2]
            calcLocalHA(u3,d3,doc3)
        cursor2.close()
        print(" .    Local HA nalysis complete.")

    except sqlite3.Error as error:
        print("Failed to read data from documents table", error)
    finally:
        if con2.close():
            print("The SQLite connection is closed")

if __name__ == '__main__':

    start = time()
    initInventory()  
    buildfeatures()  
    init()
    combs=genCombs()
    processDocuments()
    startSiteSimAnalysis()
    startLocalHAAnalysis()
    elapsed = time() - start
    print('Similarity analysis processing time: {}'.format(elapsed))

