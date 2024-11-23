
import db
from dateutil.relativedelta import relativedelta
import db
from datetime import datetime, date, timedelta
conn = db.DbConnection.dbconnOssMSME(self="")

cmonth = '202210'

#
# print('CREATE FINAL ELIGEBLE TABLE')
# try:
#     with conn.cursor() as cursor:
#         sqlRetail = "create table MSME_FINAL_ELIGEBLE_" + cmonth + " as " \
#             "select am.am_sid,'AM' AM_CATAGORY, " \
#             "(select FINAL_COMMISSION from MSME_RETAIL_RESULT_" + cmonth + " where AM_SID = am.am_sid) RETAIL, " \
#             "(select FINAL_COMMISSION from MSME_DATANEWCON_RESULT_" + cmonth + " where AM_SID = am.am_sid) DATA, " \
#             "(select FINAL_COMMISSION from MSME_VOICECOMMIT_RESULT_" + cmonth + " where AM_SID = am.am_sid) VOICE, " \
#             "(select FINAL_COMMISSION from MSME_SOLPROFIT_RESULT_" + cmonth + " where AM_SID = am.am_sid) SOLPROFIT, " \
#             "(select FINAL_COMMISSION from MSME_REVENUE_RESULT_" + cmonth + " where USR_SID = am.am_sid) REVENUE, " \
#             "(select FINAL_COMMISSION from MSME_COLLECTION_RESULT_" + cmonth + " where USR_SID = am.am_sid) COLLECTION " \
#             "from area_map_am am " \
#             "union " \
#             "select am.am_sid,'REBM' AM_CATAGORY, " \
#             "(select to_char(sum(FINAL_COMMISSION_REBM)) from MSME_RETAIL_RESULT_" + cmonth + " where REBM_SID = am.am_sid group by REBM_SID) RETAIL, " \
#             "(select to_char(sum(FINAL_COMMISSION_REBM)) from MSME_DATANEWCON_RESULT_" + cmonth + " where REBM_SID = am.am_sid group by REBM_SID) DATA, " \
#             "(select to_char(sum(FINAL_COMMISSION_REBM)) from MSME_VOICECOMMIT_RESULT_" + cmonth + " where REBM_SID = am.am_sid group by REBM_SID) VOICE, " \
#             "(select to_char(sum(FINAL_COMMISSION_REBM)) from MSME_SOLPROFIT_RESULT_" + cmonth + " where REBM_SID = am.am_sid group by REBM_SID) SOLPROFIT, " \
#             "(select FINAL_COMMISSION from MSME_REVENUE_RESULT_" + cmonth + " where USR_SID = am.am_sid) REVENUE, " \
#             "(select FINAL_COMMISSION from MSME_COLLECTION_RESULT_" + cmonth + " where USR_SID = am.am_sid) COLLECTION " \
#             "from area_map_rebm am " \
#             "order by AM_CATAGORY "
#         print(sqlRetail)
#         cursor.execute(sqlRetail)
# except conn.Error as error:
#     print('Error occurred:' + str(error))

