import sqlite3
import csv

con = sqlite3.connect('./inventory.db')
cur = con.cursor()

# Create table
#cur.execute('''CREATE TABLE documents
#               (datacenter text, url text, document str)''')

cur.execute('''CREATE TABLE combinations
               (url text, combination1 str, combination2 str)''')

                                      
# Save (commit) the changes
con.commit()

# Close the connection
con.close()
