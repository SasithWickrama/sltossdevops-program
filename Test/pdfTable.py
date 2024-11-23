import csv
import MySQLdb
from tabula import convert_into

file2 = "SLTCHQR210105134.pdf"
convert_into(file2,"test.csv",pages="all", output_format="csv")


mydb = MySQLdb.connect(host='localhost',
                       user='root',
                       passwd='',
                       db='pdftest')
cursor = mydb.cursor()
csv_data = csv.reader(open('test.csv'))
next(csv_data)
for row in csv_data:

    cursor.execute('INSERT INTO test(COL1,COL2, COL3,COL4,COL5, COL6,COL7,COL8, COL9,COL10,COL11, COL12,COL13,COL14, COL15 )'
                   'VALUES("%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s")',
                   row)
#close the connection to the database.
mydb.commit()
cursor.close()
print ("Done")