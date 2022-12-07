import sqlite3
import csv
import random
from time import time
from decimal import Decimal

def init():
    #print("Initializing tables....")
    try:
            con = sqlite3.connect('./inventory.db')
            cursor = con.cursor()
            
            sql = ''' DELETE FROM combinations'''
            cursor.execute(sql)
            con.commit()
            sql = ''' DELETE FROM documents'''
            cursor.execute(sql)
            con.commit()
            sql = ''' DELETE FROM metrics'''
            cursor.execute(sql)
            con.commit()
    except sqlite3.Error as error:
        print("Failed to delete data to sqlite table", error)
        return
    finally:
        if con.close():
            print("The SQLite connection is closed")
        return

def buildfeatures():
    
    with open('./features.csv', 'w', newline='') as csvfile1:
        fieldnames = ['DATACENTER','GUID','URL','NAME','FUNCTION', 'MEM','CPU','FEATURE']
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)
        writer.writeheader()

        with open('./inventory.csv', 'r', newline='') as csvfile2:
            reader = csv.reader(csvfile2, delimiter=',')
            for row in reader:
                if row[1] != 'GUID':
                    dc = str(row[0])
                    gu = str(row[1])
                    ur = str(row[2])
                    fn = str(row[3])
                    nm = str(row[4])
                    mm = str(row[5])
                    cp = str(row[6])
                    feature_attribute =fn+'MEM'+mm+'CPU'+cp 
                    writer.writerow(
                    {
                        'DATACENTER': dc,
                        'GUID': gu,
                        'URL': ur,
                        'NAME': nm,
                        'FUNCTION': fn,
                        'MEM': mm,
                        'CPU': cp,
                        'FEATURE': feature_attribute
                    } )          
    return

def initInventory():
    con = sqlite3.connect('./inventory.db')
    cur = con.cursor()

    # Delete records
    cur.execute('''DELETE FROM inventory''')
    con.commit()
    with open('./features.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    if row[1] != 'GUID':
                        dc = str(row[0])
                        gu = str(row[1])
                        ur = str(row[2])
                        nm = str(row[3])
                        fn = str(row[4])
                        mm = str(row[5])
                        cp = str(row[6])
                        fa = str(row[7])
                        # Insert data
                        sql = ''' INSERT INTO inventory(datacenter,guid,url,name,function,mem,cpu,feature)
                            VALUES(?,?,?,?,?,?,?,?) '''
                        rec = (dc,gu,ur,nm,fn,mm,cp,fa)
                        cur.execute(sql,rec)
                                        
    # Save (commit) the changes
    con.commit()

    # Print table contents
    #cur = con.cursor()
    #for row in cur.execute('SELECT * FROM inventory ORDER BY guid'):
    #        print(row)

    # Close the connection
    #con.close()
    return

def metricWriter(metric, url, site1, site2, sitepair, function, result, document1, document2):
    con = sqlite3.connect('./inventory.db')
    cursor = con.cursor()
    sql = ''' INSERT INTO metrics(metric, url, site1, site2, sitepair, function, result, document1, document2)
                VALUES(?,?,?,?,?,?,?,?,?) '''
                
    rec = (metric, url, site1, site2, sitepair, function, result, document1, document2)
    cursor.execute(sql,rec)
    con.commit()
    return

def writeCombRec(url,comb):
    # Persist the combinations to the DB.
    try:
        con = sqlite3.connect('./inventory.db')
        cursor = con.cursor()

        sql = ''' INSERT INTO combinations(url,combination1,combination2)
                        VALUES(?,?,?) '''
        rec = (url,comb[0],comb[1])
        cursor.execute(sql,rec)
        con.commit()
    except sqlite3.Error as error:
        print("Failed to write combination data to sqlite table", error)
    finally:
        if con.close():
            print("The SQLite connection is closed")
        return

def writeDocRec(dc,ur,doc):
    # Persist the document list to the db.
    try:
        con = sqlite3.connect('./inventory.db')
        cursor = con.cursor()

        sql = ''' INSERT INTO documents(datacenter,url,document)
                        VALUES(?,?,?) '''
        rec = (dc,ur,doc)
        cursor.execute(sql,rec)
        con.commit()
    except sqlite3.Error as error:
        print("Failed to write document data to sqlite table", error)
    finally:
        if con.close():
            print("The SQLite connection is closed")
        return

