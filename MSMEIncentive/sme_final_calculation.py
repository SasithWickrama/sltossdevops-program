from datetime import datetime
from dateutil.relativedelta import relativedelta

import db


#MSME_RETAIL_RESULT
#MSME_SOLPROFIT_RESULT
#MSME_VOICECOMMIT_RESULT
#MSME_DATANEWCON_RESULT
#MSME_DATANEWCON_RESULT2
#MSME_REVENUE_RESULT
#MSME_COLLECTION_RESULT
#FINAL_ELIGEBLE_

class FinalCalc():
    def finalCal(cmonth):
        conn = db.DbConnection.dbconnOssMSME(self="")

        #=====================================
        # CREATE RETAIL INCENTIVE RESULT TABLE
        # print('CREATE RETAIL INCENTIVE RESULT TABLE')
        # try:
        #     with conn.cursor() as cursor:
        #         sqlcreate = "CREATE TABLE MSME_RETAIL_RESULT_" + cmonth + "(AM_SID varchar2(10),AM_NAME varchar2(100), REBM_SID varchar2(20)," \
        #                     "REBM_NAME varchar2(100),SO_COUNT varchar2(10), TOT_COMMISSION varchar2(20), FINAL_COMMISSION varchar2(20)," \
        #                     "FINAL_COMMISSION_REBM varchar2(20))"
        #         cursor.execute(sqlcreate)
        # except conn.Error as error:
        #     print('Error occurred:' + str(error))
        #
        # try:
        #     with conn.cursor() as cursor:
        #         sql = "select distinct SALES_PERSON, count(SO_ID) ,sum(PKG_COMMISSION), sum(INIT_COMMISSION) " \
        #               "from MSME_RETAIL_" + cmonth + " aa " \
        #                                              "where STATUS = '0' " \
        #                                              "and BSS_STATUS = 'OK' " \
        #                                              "group by SALES_PERSON"
        #
        #         cursor.execute(sql)
        #
        #         for row in cursor:
        #             if row[2] is None:
        #                 pkg_com = 0
        #             else:
        #                 pkg_com = row[2]
        #             if row[3] is None:
        #                 ini_com = 0
        #             else:
        #                 ini_com = row[3]
        #
        #             tot = int(pkg_com) + int(ini_com)
        #             finalAM = round(tot * 40 / 100, 2)
        #             finalREBM = round(tot * 20 / 100, 2)
        #             print(tot)
        #
        #             try:
        #                 with conn.cursor() as cursor2:
        #                     sql2 = "select distinct SERVICENO from INCENPRG.CRM_EMP_LIST where NAME = :name"
        #                     cursor2.execute(sql2, [row[0]])
        #                     row2 = cursor2.fetchone()
        #             except conn.Error as error:
        #                 print('Error occurred:' + str(error))
        #
        #             try:
        #                 with conn.cursor() as cursor3:
        #                     sql3 = "select distinct aa.AM_AREA_ID,aa.AM_NAME , bb.AM_SID,bb.AM_NAME " \
        #                            "from AREA_MAP_AM aa, AREA_MAP_REBM bb " \
        #                            "where aa.AM_AREA_ID = bb.AM_AREA_ID " \
        #                            "and aa.AM_SID = :AM_SID"
        #                     cursor3.execute(sql3, [row2[0]])
        #                     row3 = cursor3.fetchone()
        #                     # print(row3,row2[0])
        #
        #
        #                     if row3 is not None:
        #                         print(row2[0], row[0], row3[0], row[1], tot, finalAM, finalREBM)
        #                         with conn.cursor() as cursor4:
        #                             sqlerp = "INSERT INTO MSME_RETAIL_RESULT_" + cmonth + " VALUES( :SID,:SNAME,:REBMSID,:REBMNAME,:SO_COUNT,:TOT_COMMISSION,:FINAL_COMMISSION,:FINAL_COMMISSION_REBM)"
        #                             cursor4.execute(sqlerp, [row2[0], row3[1], row3[2], row3[3], row[1], tot, finalAM, finalREBM])
        #                             conn.commit()
        #
        #             except conn.Error as error:
        #                 print('Error occurred:' + str(error))
        #
        #     try:
        #         with conn.cursor() as cursor:
        #             sqlInc = "UPDATE MSME_INCENT_STAT SET RETAIL_READY= :RETAIL_DONE  WHERE YMONTH= :YMONTH"
        #             cursor.execute(sqlInc,['YES',cmonth])
        #             conn.commit()
        #     except conn.Error as error:
        #         print('Error occurred:' + str(error))
        # except conn.Error as error:
        #     print('Error occurred:' + str(error))




        #==============================================
        # CREATE SOLUTION PROFIT INCENTIVE RESULT TABLE
        # print('CREATE SOLUTION PROFIT INCENTIVE RESULT TABLE')
        # try:
        #     with conn.cursor() as cursor:
        #         sqlcreate = "CREATE TABLE MSME_SOLPROFIT_RESULT_" + cmonth + "(AM_SID varchar2(10),AM_NAME varchar2(100), REBM_SID varchar2(20)," \
        #                      "REBM_NAME varchar2(100),RSSE_SID varchar2(20),RSSE_NAME varchar2(100), TOT_COMMISSION varchar2(20), FINAL_COMMISSION varchar2(20)," \
        #                      "FINAL_COMMISSION_REBM varchar2(20),FINAL_COMMISSION_RSSE varchar2(20))"
        #         cursor.execute(sqlcreate)
        # except conn.Error as error:
        #     print('Error occurred:' + str(error))
        #
        # try:
        #     with conn.cursor() as cursor:
        #         sql = "select ACCOUNT_MANAGER,sum(NVL(PROFIT, 0)) " \
        #               "from MSME_SOLPROFIT_" + cmonth + " where PROFIT >0 " \
        #                                                 "group by ACCOUNT_MANAGER"
        #
        #         cursor.execute(sql)
        #
        #         for row in cursor:
        #             tot = row[1]
        #             finalAM = round(tot * 4 / 100, 2)
        #             finalREBM = round(tot * 4 / 100, 2)
        #             finalRSSE = round(tot * 10 / 100, 2)
        #
        #             try:
        #                 with conn.cursor() as cursor3:
        #                     sql3 = "select distinct aa.AM_SID,aa.AM_NAME , bb.AM_SID,bb.AM_NAME,cc.AM_SID,cc.AM_NAME,aa.AM_AREA_ID " \
        #                            "from AREA_MAP_AM aa, AREA_MAP_REBM bb , AREA_MAP_RSSE cc " \
        #                            "where aa.AM_AREA_ID = bb.AM_AREA_ID " \
        #                            "and aa.AM_AREA_ID = cc.AM_AREA_REBM_ID " \
        #                            "and aa.AM_CODE = :AM_CODE"
        #                     cursor3.execute(sql3, [row[0]])
        #                     row3 = cursor3.fetchone()
        #                     # print(row3,row2[0])
        #
        #
        #                     if row3 is not None:
        #                         print( row[0], row3[0],  tot, finalAM, finalREBM, finalRSSE)
        #                         with conn.cursor() as cursor4:
        #                             sqlresult = "INSERT INTO MSME_SOLPROFIT_RESULT_" + cmonth + " VALUES( :SID,:SNAME,:REBMSID,:REBMNAME,:RSSESID,:RSSENAME,:TOT_COMMISSION,:FINAL_COMMISSION,:FINAL_COMMISSION_REBM,:FINAL_COMMISSION_RSSE)"
        #                             cursor4.execute(sqlresult, [row3[0], row3[1], row3[2], row3[3],row3[4], row3[5], tot, finalAM, finalREBM,finalRSSE])
        #                             conn.commit()
        #
        #             except conn.Error as error:
        #                 print('Error occurred:' + str(error))
        #
        #     try:
        #         with conn.cursor() as cursor:
        #             sqlInc = "UPDATE MSME_INCENT_STAT SET SOL_PROFIT_DONE= :SOL_PROFIT_DONE  WHERE YMONTH= :YMONTH"
        #             cursor.execute(sqlInc,['YES',cmonth])
        #             conn.commit()
        #     except conn.Error as error:
        #         print('Error occurred:' + str(error))
        # except conn.Error as error:
        #     print('Error occurred:' + str(error))
        #
        #
        # #==============================================
        # #CREATE VOICE COMMITMENT INCENTIVE RESULT TABLE
        # print('CREATE VOICE COMMITMENT INCENTIVE RESULT TABLE')
        # try:
        #     with conn.cursor() as cursor:
        #         sqlcreate = "CREATE TABLE MSME_VOICECOMMIT_RESULT_" + cmonth + "(AM_SID varchar2(10),AM_NAME varchar2(100), REBM_SID varchar2(20)," \
        #                     "REBM_NAME varchar2(100),ACC_COUNT varchar2(10), TOT_COMMISSION varchar2(20), FINAL_COMMISSION varchar2(20)," \
        #                      "FINAL_COMMISSION_REBM varchar2(20))"
        #         cursor.execute(sqlcreate)
        # except conn.Error as error:
        #     print('Error occurred:' + str(error))
        #
        # try:
        #     with conn.cursor() as cursor:
        #         sql = "select ACCOUNT_MANAGER,sum(RENTAL1)" \
        #               "from MSME_VOICECOMMIT_" + cmonth + " group by ACCOUNT_MANAGER"
        #
        #         cursor.execute(sql)
        #
        #         for row in cursor:
        #             tot = row[1]
        #             finalAM = round(tot * 40 / 100, 2)
        #             finalREBM = round(tot * 20 / 100, 2)
        #             print(tot)
        #
        #             try:
        #                 with conn.cursor() as cursor3:
        #                     sql3 = "select distinct aa.AM_SID,aa.AM_NAME , bb.AM_SID,bb.AM_NAME,aa.AM_AREA_ID " \
        #                            "from AREA_MAP_AM aa, AREA_MAP_REBM bb " \
        #                            "where aa.AM_AREA_ID = bb.AM_AREA_ID " \
        #                            "and aa.AM_CODE = :AM_CODE"
        #                     cursor3.execute(sql3, [row[0]])
        #                     row3 = cursor3.fetchone()
        #                     # print(row3,row2[0])
        #
        #                     print( row[0], row3[0], row[1], tot, finalAM, finalREBM)
        #
        #                     with conn.cursor() as cursor4:
        #                         sqlresult = "INSERT INTO MSME_VOICECOMMIT_RESULT_" + cmonth + " VALUES( :SID,:SNAME,:REBMSID,:REBMNAME,:ACC_COUNT,:TOT_COMMISSION,:FINAL_COMMISSION,:FINAL_COMMISSION_REBM)"
        #                         cursor4.execute(sqlresult, [row3[0], row3[1], row3[2], row3[3], row[1], tot, finalAM, finalREBM])
        #                         conn.commit()
        #
        #             except conn.Error as error:
        #                 print('Error occurred:' + str(error))
        #
        #     try:
        #         with conn.cursor() as cursor:
        #             sqlInc = "UPDATE MSME_INCENT_STAT SET VOICE_COMIT_DONE= :VOICE_COMIT_DONE  WHERE YMONTH= :YMONTH"
        #             cursor.execute(sqlInc,['YES',cmonth])
        #             conn.commit()
        #     except conn.Error as error:
        #         print('Error occurred:' + str(error))
        # except conn.Error as error:
        #     print('Error occurred:' + str(error))
        #
        #
        # #==================================
        # #CREATE DATA INCENTIVE RESULT TABLE
        # print('CREATE DATA INCENTIVE RESULT TABLE')
        # try:
        #     with conn.cursor() as cursor:
        #         sqlcreate = "CREATE TABLE MSME_DATANEWCON_RESULT_" + cmonth + "(AM_SID varchar2(20),AM_NAME varchar2(100), REBM_SID varchar2(20)," \
        #                     "REBM_NAME varchar2(100),RSSE_SID varchar2(20),RSSE_NAME varchar2(100), TOT_COMMISSION_RENT varchar2(20),TOT_COMMISSION_ONEOFF varchar2(20), FINAL_COMMISSION varchar2(20)," \
        #                     "FINAL_COMMISSION_REBM varchar2(20),FINAL_COMMISSION_RSSE varchar2(20))"
        #         cursor.execute(sqlcreate)
        # except conn.Error as error:
        #     print('Error occurred:' + str(error))
        #
        # try:
        #     with conn.cursor() as cursor:
        #         sqlcreate = "CREATE TABLE MSME_DATANEWCON_RESULT2_" + cmonth + "(ACCOUNT_MANAGER varchar2(20)," \
        #                     "RENTAL varchar2(30),ONE_OFF_NUMBER varchar2(30),DTYPE varchar2(30))"
        #         cursor.execute(sqlcreate)
        # except conn.Error as error:
        #     print('Error occurred:' + str(error))
        #
        # try:
        #     with conn.cursor() as cursor:
        #         sql = "select ACCOUNT_MANAGER, RENTAL,OVERRIDE_RENTAL ,ONE_OFF_NUMBER,OVERRIDE_ONE_OFF_NUMBER " \
        #               "from MSME_DATA_NEWCON2_" + cmonth + " " \
        #               "where PCATEGORY1 = :PCATEGORY1 and PRODUCT_STATUS =:PRODUCT_STATUS"
        #
        #         cursor.execute(sql, ['DATA','OK'])
        #
        #         for row in cursor:
        #
        #             if row[2] == 0 or row[2] is None:
        #                 rent = row[1]
        #             else:
        #                 rent = row[2]
        #
        #             if row[4] == 0 or row[4] is None:
        #                 oneoff = row[3]
        #             else:
        #                 oneoff = row[4]
        #
        #             with conn.cursor() as cursor4:
        #                 sqlresult = "INSERT INTO MSME_DATANEWCON_RESULT2_" + cmonth + " VALUES( :AM,:RENTAL,:ONNOFF,:DTYPE)"
        #                 cursor4.execute(sqlresult, [row[0], rent, oneoff, 'NC'])
        #                 conn.commit()
        # except conn.Error as error:
        #     print('Error occurred:' + str(error))
        #
        # try:
        #     with conn.cursor() as cursor:
        #         sql = "select  ACCOUNT_MANAGER, RENTAL,OVERRIDE_RENTAL ,ONE_OFF_NUMBER,OVERRIDE_ONE_OFF_NUMBER,PREVIOUS_RENTAL " \
        #               "from MSME_DATA_PKGCHG2_" + cmonth + " " \
        #               "where PCATEGORY1 = :PCATEGORY1 and PRODUCT_STATUS =:PRODUCT_STATUS"
        #
        #         cursor.execute(sql, ['DATA','OK'])
        #
        #         for row in cursor:
        #
        #             if row[2] == 0 or row[2] is None:
        #                 rent = row[1]
        #             else:
        #                 rent = row[2]
        #
        #             if row[4] == 0 or row[4] is None:
        #                 oneoff = row[3]
        #             else:
        #                 oneoff = row[4]
        #
        #             if rent > row[5]:
        #                 rent = rent - row[5];
        #                 with conn.cursor() as cursor4:
        #                     sqlresult = "INSERT INTO MSME_DATANEWCON_RESULT2_" + cmonth + " VALUES( :AM,:RENTAL,:ONNOFF,:DTYPE)"
        #                     cursor4.execute(sqlresult, [row[0], rent, oneoff, 'PKG'])
        #                     conn.commit()
        # except conn.Error as error:
        #     print('Error occurred:' + str(error))
        #
        # try:
        #     with conn.cursor() as cursor:
        #         sql = "select ACCOUNT_MANAGER,sum(RENTAL),sum(ONE_OFF_NUMBER) " \
        #               "from MSME_DATANEWCON_RESULT2_" + cmonth + " group by ACCOUNT_MANAGER"
        #
        #         cursor.execute(sql)
        #
        #         for row in cursor:
        #             print(row[0],row[1],row[2])
        #             if row[1] is None:
        #                 rent = 0
        #             else:
        #                 rent = row[1]
        #
        #             if row[2] is None:
        #                 oneOff = 0
        #             else:
        #                 oneOff = row[2]
        #
        #             tot = round(rent + oneOff, 2)
        #
        #             rentAM = round(rent * 40 / 100, 2)
        #             rentREBM = round(rent * 20 / 100, 2)
        #             rentRSSE = round(rent * 5 / 100, 2)
        #
        #             oneOffAM = round(oneOff * 10 / 100, 2)
        #             oneOffREBM = round(oneOff * 5 / 100, 2)
        #             oneOffRSSE = round(oneOff * 5 / 100, 2)
        #
        #             finalAM = round(float(rentAM) + float(oneOffAM), 2)
        #             finalREBM = round(float(rentREBM) + float(oneOffREBM), 2)
        #             finalRSSE = round(float(rentRSSE) + float(oneOffRSSE), 2)
        #
        #             try:
        #                 with conn.cursor() as cursor3:
        #                     sql3 = "select distinct aa.AM_SID,aa.AM_NAME , bb.AM_SID,bb.AM_NAME,cc.AM_SID,cc.AM_NAME,aa.AM_AREA_ID " \
        #                            "from AREA_MAP_AM aa, AREA_MAP_REBM bb , AREA_MAP_RSSE cc " \
        #                            "where aa.AM_AREA_ID = bb.AM_AREA_ID " \
        #                            "and aa.AM_AREA_ID = cc.AM_AREA_REBM_ID " \
        #                            "and aa.AM_CODE = :AM_CODE"
        #                     cursor3.execute(sql3, [row[0]])
        #                     row3 = cursor3.fetchone()
        #                     print(row3)
        #
        #                     if row3 is not None :
        #                         print(row[0], row3[0], tot, finalAM, finalREBM, finalRSSE)
        #                         with conn.cursor() as cursor4:
        #                             sqlresult = "INSERT INTO MSME_DATANEWCON_RESULT_" + cmonth + " VALUES( :SID,:SNAME,:REBMSID,:REBMNAME,:RSSESID,:RSSENAME,:TOT_COMMISSION_RENT,:TOT_COMMISSION_ONEOFF,:FINAL_COMMISSION,:FINAL_COMMISSION_REBM,:FINAL_COMMISSION_RSSE)"
        #                             cursor4.execute(sqlresult,
        #                                             [row3[0], row3[1], row3[2], row3[3], row3[4], row3[5], rent,oneOff, finalAM,
        #                                              finalREBM, finalRSSE])
        #                             conn.commit()
        #
        #             except conn.Error as error:
        #                 print('Error occurred:' + str(error))
        #
        #     try:
        #         with conn.cursor() as cursor:
        #             sqlInc = "UPDATE MSME_INCENT_STAT SET DATA_DONE= :DATA_DONE  WHERE YMONTH= :YMONTH"
        #             cursor.execute(sqlInc,['YES',cmonth])
        #             conn.commit()
        #     except conn.Error as error:
        #         print('Error occurred:' + str(error))
        # except conn.Error as error:
        #     print('Error occurred:' + str(error))
        #
        #
        # #=====================================
        # # CREATE REVENUE INCENTIVE RESULT TABLE
        # print('CREATE REVENUE INCENTIVE RESULT TABLE')
        # try:
        #     with conn.cursor() as cursor:
        #         sqlcreate = "CREATE TABLE MSME_REVENUE_RESULT_" + cmonth + "(USR_SID varchar2(10),USR_NAME varchar2(100), USR_CATAGORY varchar2(20)," \
        #                                                                      "FINAL_COMMISSION varchar2(20))"
        #         cursor.execute(sqlcreate)
        #
        #     with conn.cursor() as cursor:
        #         sqlcreate = "CREATE TABLE MSME_COLLECTION_RESULT_" + cmonth + "(USR_SID varchar2(10),USR_NAME varchar2(100), USR_CATAGORY varchar2(20)," \
        #                                                                    "FINAL_COMMISSION varchar2(20))"
        #         cursor.execute(sqlcreate)
        # except conn.Error as error:
        #     print('Error occurred:' + str(error))
        #
        # #REVENUE COLLECTION
        # print('CREATE COLLECTION TABLE')
        # try:
        #     with conn.cursor() as cursor:
        #         sql = "select AM_CODE,AM_CAT,NVL(COLLECTION_RATIO, 0) " \
        #               "from MSME_COLLECTION_" + cmonth + " "
        #
        #         cursor.execute(sql)
        #
        #         for row in cursor:
        #             if row[1] == 'AM':
        #                 if float(row[2]) > 89.99 :
        #                     finalAM = '10000.00'
        #                 elif float(row[2]) > 79.99 :
        #                     finalAM = '5000.00'
        #                 else:
        #                     finalAM = '0.00'
        #
        #                 with conn.cursor() as cursor3:
        #                     sql3 = "select distinct AM_SID,AM_NAME from AREA_MAP_AM where AM_CODE = :AM_CODE"
        #                     cursor3.execute(sql3, [row[0]])
        #                     row3 = cursor3.fetchone()
        #
        #
        #             if row[1] == 'REBM':
        #                 if float(row[2]) > 89.99 :
        #                     finalAM = '15000.00'
        #                 elif float(row[2]) > 79.99 :
        #                     finalAM = '10000.00'
        #                 else:
        #                     finalAM = '0.00'
        #
        #                 with conn.cursor() as cursor3:
        #                     sql3 = "select a.AM_SID,a.AM_NAME from area_map_rebm a, area_map b " \
        #                            "where a.am_area_id = b.area_id and b.AREA_REBM = :AREA_REBM"
        #                     cursor3.execute(sql3, [row[0]])
        #                     row3 = cursor3.fetchone()
        #
        #             try:
        #                 if row3 is not None:
        #                     with conn.cursor() as cursor4:
        #                         sqlresult = "INSERT INTO MSME_COLLECTION_RESULT_" + cmonth + " VALUES( :SID,:SNAME,:CAT,:REVENUE)"
        #                         cursor4.execute(sqlresult, [row3[0], row3[1], row[1], finalAM])
        #                         conn.commit()
        #
        #             except conn.Error as error:
        #                 print('Error occurred:' + str(error))
        #
        #     try:
        #         with conn.cursor() as cursor:
        #             sqlInc = "UPDATE MSME_INCENT_STAT SET SOL_PROFIT_DONE= :SOL_PROFIT_DONE  WHERE YMONTH= :YMONTH"
        #             cursor.execute(sqlInc,['YES',cmonth])
        #             conn.commit()
        #     except conn.Error as error:
        #         print('Error occurred:' + str(error))
        # except conn.Error as error:
        #     print('Error occurred:' + str(error))
        #
        # #TOTAL REVENUE
        # print('CREATE REVENUE TABLE')
        # try:
        #     with conn.cursor() as cursor:
        #         sql = "select aa.ACC_MGR,aa.AM_CATAGORY, nvl(aa.TOT_PERC,0) , nvl(bb.TOT_PERC,0) " \
        #               "from MSME_REV2_" + cmonth + " aa,MSME_YTD_" + cmonth + " bb " \
        #                                                                       "where aa.ACC_MGR = bb.ACC_MGR "
        #
        #         cursor.execute(sql)
        #
        #         for row in cursor:
        #             if row[1] == 'AM':
        #                 if row[1] == 'AM':
        #                     if float(row[2]) > 105 or float(row[3]) > 105:
        #                         finalAM = '20000.00'
        #                     elif float(row[2]) > 99.99 or float(row[3]) > 99.99:
        #                         finalAM = '15000.00'
        #                     elif float(row[2]) > 95.99 or float(row[3]) > 95.99:
        #                         finalAM = '7500.00'
        #                     else:
        #                         finalAM = '0.00'
        #                     print(row[0])
        #                     with conn.cursor() as cursor3:
        #                         sql3 = "select distinct AM_SID,AM_NAME from AREA_MAP_AM where AM_CODE = :AM_CODE"
        #                         cursor3.execute(sql3, [row[0]])
        #                         row3 = cursor3.fetchone()
        #                         print(row[0],row3)
        #
        #
        #             if row[1] == 'REBM':
        #                 if float(row[2]) > 105 or float(row[3]) > 105:
        #                     finalAM = '30000.00'
        #                 elif float(row[2]) > 99 or float(row[3]) > 99:
        #                     finalAM = '25000.00'
        #                 elif float(row[2]) > 95 or float(row[3]) > 99:
        #                     finalAM = '15000.00'
        #                 else:
        #                     finalAM = '0.00'
        #
        #                 with conn.cursor() as cursor3:
        #                     sql3 = "select a.AM_SID,a.AM_NAME from area_map_rebm a, area_map b " \
        #                            "where a.am_area_id = b.area_id and b.AREA_REBM = :AREA_REBM"
        #                     cursor3.execute(sql3, [row[0]])
        #                     row3 = cursor3.fetchone()
        #
        #             print(row[0],row3)
        #             try:
        #                 if row3 is not None:
        #                     with conn.cursor() as cursor4:
        #                         sqlresult = "INSERT INTO MSME_REVENUE_RESULT_" + cmonth + " VALUES( :SID,:SNAME,:CAT,:REVENUE)"
        #                         cursor4.execute(sqlresult, [row3[0], row3[1], row[1], finalAM])
        #                         conn.commit()
        #
        #             except conn.Error as error:
        #                 print('Error occurred:' + str(error))
        #
        #     try:
        #         with conn.cursor() as cursor:
        #             sqlInc = "UPDATE MSME_INCENT_STAT SET SOL_PROFIT_DONE= :SOL_PROFIT_DONE  WHERE YMONTH= :YMONTH"
        #             cursor.execute(sqlInc,['YES',cmonth])
        #             conn.commit()
        #     except conn.Error as error:
        #         print('Error occurred:' + str(error))
        # except conn.Error as error:
        #     print('Error occurred:' + str(error))


        # #FINAL ELIGEBLE CALCULATION
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


