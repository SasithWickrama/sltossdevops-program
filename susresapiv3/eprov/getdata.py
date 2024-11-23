import traceback
import json

from sqlalchemy import false, true
from log import getLogger
from db import DbConnection
import requests
import cx_Oracle

logger = getLogger('eprov', 'logs/getData')

class GetData:
    def get_records(self):
        data = self
        circuit = data['cct']
        circuitType = data['type']
        logger.info("Request : %s" % data)

        conn = DbConnection.dbconn(self="")
        if conn is None:
            return {"error":"true" ,"data": "", "message":DbConnection.dberror}
        
        c = conn.cursor()
        sql = 'SELECT  TO_CHAR(SYSDATE,\'YYYY\') ,TO_CHAR(SYSDATE,\'MM\') FROM DUAL'
        c.execute(sql)
        for row in c:
            tableyear = row[0]
            tablemonth = row[1]

        
        count = 0
        returnValue = {"error":"true" ,"data": "", "message":"No Data Found"}
        

        while(True):
            if circuitType == "VOICE":
                sql = "SELECT *  FROM ( SELECT REQ_ID, REQ_BY, REF_ID, LEA, CR, ACCNO, ORDER_TYPE, SERVICE_TYPE, EX_ID, " \
        "SERVICE_ID, CCT,  (SELECT CODE_DISCRIPTION FROM EXPROV_STATUS WHERE STATUS_CODE= STATUS) STATUS , IN_DATE, "\
            " STATUS_DATE, BSS_STAT FROM OSSPRG.EXPROV_VOICE_"+tableyear+tablemonth+" "\
            " WHERE CCT = '"+circuit+"' ORDER BY STATUS_DATE DESC) WHERE ROWNUM = 1"

            elif circuitType == "BB":
                sql = "SELECT *  FROM ( SELECT REQ_ID, REQ_BY, REF_ID, LEA, CR, ACCNO, ORDER_TYPE, SERVICE_TYPE, EX_ID, " \
        "SERVICE_ID, CCT,  (SELECT CODE_DISCRIPTION FROM EXPROV_STATUS WHERE STATUS_CODE= STATUS) STATUS , IN_DATE, "\
            " STATUS_DATE, BSS_STAT FROM OSSPRG.EXPROV_BB_"+tableyear+tablemonth+" "\
            " WHERE CCT = '"+circuit+"' ORDER BY STATUS_DATE DESC) WHERE ROWNUM = 1"

            elif circuitType == "IPTV":
                sql = "SELECT *  FROM ( SELECT REQ_ID, REQ_BY, REF_ID, LEA, CR, ACCNO, ORDER_TYPE, SERVICE_TYPE, EX_ID, " \
        "SERVICE_ID, CCT,  (SELECT CODE_DISCRIPTION FROM EXPROV_STATUS WHERE STATUS_CODE= STATUS) STATUS , IN_DATE, "\
            " STATUS_DATE, BSS_STAT FROM OSSPRG.EXPROV_IPTV_"+tableyear+tablemonth+" "\
            " WHERE CCT = '"+circuit+"' ORDER BY STATUS_DATE DESC) WHERE ROWNUM = 1"

            else:
                returnValue = {"error":"true" ,"data": "", "message":"Invalid Type"}
                break

            print(str(count)+"   "+str(tableyear+tablemonth) )            
            c.execute(sql)
            for row in c:
                returnValue = {"error":"false" ,"data": '{"REQ_ID":"'+str(row[0])+' \
                ","REQ_BY":"'+str(row[1])+'","REF_ID":"'+str(row[2])+'","LEA":"'+str(row[3])+'","CR":"'+str(row[4])+'"\
                ,"ACCNO":"'+str(row[5])+'","ORDER_TYPE":"'+str(row[6])+'","SERVICE_TYPE":"'+str(row[7])+'","EX_ID":"'+str(row[8])+'"\
                ,"SERVICE_ID":"'+str(row[9])+'","CCT":"'+str(row[10])+'","STATUS":"'+str(row[11])+'","IN_DATE":"'+str(row[12])+'"\
                ,"STATUS_DATE":"'+str(row[13])+'","BSS_STAT":"'+str(row[14])+'"\
                }', "message":"Success"}
                break

            count = count +1
            tempmonth = int(tablemonth)-1
            tablemonth = str(tempmonth).zfill(2)
            if tempmonth == 0:
                tablemonth = "12"
                tableyear = str(int(tableyear)-1)
            
            if str(tableyear+tablemonth) == "202207": 
                break
            
            if count == 12:
                break       

        return returnValue