
#ftp.retrbinary('ftp://172.25.2.142/ONT_Optical_Power_Reports/Huawei/Access_Service_Statistics_ONT_Status_In_Huawei_OLTs.zip', flo.write)

        

import ftplib
import sys
from zipfile import ZipFile
import pandas as pd
import xlrd
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True

def getFile(ftp, filename):
    try:
        ftp.retrbinary("RETR " + filename ,open("HUAWEIfiletest.zip", 'wb').write)
    except:
        print ("Error")
 
#ftp = ftplib.FTP("172.25.2.142")
#ftp.login("anonymous", "ftplib-example-1")
 
#ftp.cwd('ONT_Optical_Power_Reports/Huawei/')       
#getFile(ftp,'Access_Service_Statistics_ONT_Status_In_Huawei_OLTs.zip')
 
#ftp.quit()

#with ZipFile('HUAWEIfiletest.zip', 'r') as zf:
#    zf.extractall('HuaweiFiletest')

fields = ['Subnet', 'ONU Alias' , 'Operation Status' , 'Rx Optical Power(dBm)' , 'OLT Rx ONU Optical Power(dBm)']

df = pd.read_excel(r'HuaweiFiletest/Access_Service_Statistics_ONT_Status_In_Huawei_OLTs.xlsx', index_col=None, na_values=['NA'],  usecols=fields, skiprows=[0,1,2,3,4,5,6])
#print(df)

for index, row in df.iterrows():
    if index == 450:
        print(index, row)




