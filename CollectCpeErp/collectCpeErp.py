import json

import requests
import zeep
from log import getLogger
import db

logger = getLogger('collectcpeerp', 'logs/collectcpeerp')
#endpoint = 'http://hq-ginny/CPECollectionManagementPortal/api/Values/AddBasket'
endpoint = 'https://rcmp.intranet.slt.com.lk/rcmp_api/api/Values/AddBasket'
headers = {
    'Content-Type': 'application/json'
}

result = {}
data = []

try:
    conn = db.DbConnection.dbconnOssDev(self="")
    c = conn.cursor()
    sql ="select SO_ID,RTOM,ORDER_TYPE,CIRCUIT,ASSIGNED_TO,COMPLEATED_ON, REG,SER_TYPE " \
         "from ( " \
         "select distinct sn.SO_ID,RTOM,ORDER_TYPE,CIRCUIT,ASSIGNED_TO,COMPLEATED_ON, REGID REG,SER_TYPE " \
         "from COLLECT_CPE_SN sn " \
         "where  CUSRESPONCE =\'AGREE TO COLLECT CPES\' " \
         "and sn.STATUS = \'2\' and ERP_RESULT is null and SER_TYPE NOT IN (\'AB-WIRELESS ACCESS\')  union all " \
         "select distinct sn.SO_ID,RTOM,ORDER_TYPE,CIRCUIT,ASSIGNED_TO,COMPLEATED_ON, CIRCUIT REG,SER_TYPE " \
         "from COLLECT_CPE_SN sn " \
         "where  CUSRESPONCE =\'AGREE TO COLLECT CPES\' " \
         "and sn.STATUS = \'2\' and ERP_RESULT is null and SER_TYPE IN (\'AB-WIRELESS ACCESS\') )" \
         "where rownum <= 10"

    c.execute(sql)


    for row in c:
        print(row)
        # result['service_order_number'] = str(row[0])
        # result['service_order_type'] = str(row[2])
        # result['equipment_capture_date'] =row[5].strftime("%m/%d/%Y, %H:%M:%S")
        # result['contractor'] = 'SLT'
        # result['collected_officer'] = str(row[4])
        # result['collected_officer_mobile'] = ''
        # result['recovery_date'] = str(row[5].strftime("%m/%d/%Y, %H:%M:%S"))
        # result['product_lable'] = str(row[6])
        # result['rtom'] = str(row[1])
        #
        # sql2 ="select *  from COLLECT_CPE_SN_LIST where SO_ID= :sod"
        # c2 = conn.cursor()
        # c2.execute(sql2,[row[0]])
        #
        # for rowatt in c2:
        #     data.append({"equipment_type": str(rowatt[6]),
        #                  "equipment_model": str(rowatt[2]),
        #                  "serial_no": str(rowatt[1])})
        #
        #
        # result['equipment'] = data
        #
        # try:
        #     responce = requests.post(endpoint,headers=headers,verify=False, data=json.dumps(result))
        #     outresult = json.loads(responce.text)
        #     logger.info(row[0]+" - "+str(result))
        #     logger.info(row[0]+" - "+str(outresult))
        #
        #     if outresult['isSuccess'] == True:
        #         outmsg = 'success'
        #     else:
        #         outmsg = 'error'
        #
        #     sqlupdate = "update COLLECT_CPE_SN set ERP_RESULT = :ERP_RESULT where SO_ID = :SO_ID"
        #     with conn.cursor() as cursor2:
        #         cursor2.execute(sqlupdate, [outmsg, row[0]])
        #         conn.commit()
        #         print(cursor2.rowcount)
        # except Exception as e:
        #     logger.info(row[0]+" - "+str(e))


except conn.Error as error:
    print('Error occurred:' + str(error))
    logger.error(" " + str(error))



