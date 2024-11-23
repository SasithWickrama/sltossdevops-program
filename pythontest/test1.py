import shutil
import urllib.request as request
from contextlib import closing
import pandas as pd
import xlrd
from db import DbConnection
import re
"""
with closing(request.urlopen('ftp://172.25.2.142/ONT_Optical_Power_Reports/ZTE/ZTE-OLT.xlsx')) as r:
    with open('ZTEfile.xlsx', 'wb') as f:
        shutil.copyfileobj(r, f)

with closing(request.urlopen('ftp://172.25.2.142/ONT_Optical_Power_Reports/Huawei/Access_Service_Statistics_ONT_Status_In_Huawei_OLTs.zip')) as r:
    with open('HUAWEIfile.zip', 'wb') as f:
        shutil.copyfileobj(r, f)
"""
fields = ['Location', 'ONU Name' , 'Operational Status' , 'Receive Optical Power(dBm)' , 'OLT Receive Optical Power(dBm)']
df = pd.read_excel('ZTEfile.xlsx', index_col=None, na_values=['NA'],  usecols=fields)
#print (df.iloc[1,1] )

conn = DbConnection.dbconn(self="")
#    if conn is None:
#        return {"error":"true" ,"data": "", "message":DbConnection.dberror}
        
c = conn.cursor()
for index, row in df.iterrows():

    loc = row["Location"]
    locArr = loc.split('.')
    area = locArr[5]
    areaNArr = area.split('-')
    rtom = areaNArr[0]
    optSt = re.sub(r'[^a-zA-Z0-9]','',row["Operational Status"])
    onuNr = str(row["ONU Name"]).replace("'",'')
    onuN = onuNr.replace(".0",'')
    sql = "INSERT INTO OSSPRG.LINE_QUALITY_TEST (LOCATION, OLT_ROP,SEVICE_TYPE, UP_FILE_TYPE, DATA_IN_DATE, PW_LEVEL, CIRCUIT_NAME, OPERATIONAL_ST, OPMC) VALUES ('{0}','{1}','FTTH','ZTE',SYSDATE,'{2}','{3}','{4}','{5}')".format(loc ,row["OLT Receive Optical Power(dBm)"],row["Receive Optical Power(dBm)"],onuN,optSt,rtom)  
    print(sql)
    c.execute(sql)
    c.execute("commit")
    
c.close()
conn.close()


