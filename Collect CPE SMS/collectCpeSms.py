import zeep
from log import getLogger
import db

logger = getLogger('collectcpesms', 'logs/collectcpesms')
wsdl = 'http://172.25.37.196:8080/Smssystem/smsSending?WSDL'
client = zeep.Client(wsdl=wsdl)

try:
    conn = db.DbConnection.dbconnOssDev(self="")
    c = conn.cursor()
    sql ="select distinct aa.SO_ID, bb.A_VAL,aa.NEW_CUS_MOBILE from COLLECT_CPE_SN aa, COLLECT_CPE_ATTRIBUTES bb " \
        "where aa.SO_ID = bb.SO_ID and A_NAME= 'REGISTRATION ID' and CUSRESPONCE = 'AGREE TO COLLECT CPES' " \
         "and CUS_SMS is null and NEW_CUS_MOBILE is not null " \
         "union all select distinct aa.SO_ID, aa.CIRCUIT,aa.NEW_CUS_MOBILE from COLLECT_CPE_SN aa " \
         "where CUSRESPONCE = 'AGREE TO COLLECT CPES' and CUS_SMS is null and NEW_CUS_MOBILE is not null    "
    c.execute(sql)


    for row in c:
        print(row[0])
        msg = "Installed CPEs for "+str(row[1])+" collected under order reference "+str(row[0])+" by SLTMOBITEL. Thank you for using SLTMOBITEL- Home services."

        if row[2][0:2] == '07' and len(row[2]) == 10:
            result = client.service.smsdirectx(str(row[2]), msg, 'OSS', 'SLTCMS', '!23qweASD')

        try:
            sql = "update COLLECT_CPE_SN set CUS_SMS=:CUS_SMS where  SO_ID= :SO_ID"
            with conn.cursor() as cursor:
                cursor.execute(sql, [str(result), str(row[0])])
                conn.commit()

        except conn.Error as error:
            print('DB Error:' + str(error))
            logger.error(" " + str(error))


except conn.Error as error:
    print('Error occurred:' + str(error))
    logger.error(" " + str(error))



