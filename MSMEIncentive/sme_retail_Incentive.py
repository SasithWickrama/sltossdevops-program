import db

BBCOMLATEST = ""
IPTVCOMLATEST = ""
PRODCOMLATEST = ""
RTOMCATLATEST = ""
INCENLATEST = ""
TARGETLATEST = ""


def runDb(self):
    print(self)
    print('\n')
    conn = db.DbConnection.dbconnOssMSME(self="")
    try:
        with conn.cursor() as cursor:
            cursor.execute(self)
            conn.commit()

    except conn.Error as error:
        print('Error occurred:' + str(error))

class Retail():
    def retailData(cmonth):
        try:
            conn = db.DbConnection.dbconnOssMSME(self="")

            # COPY DATA FROM RETAIL INCENTIVE TABLE
            try:
                with conn.cursor() as cursor:
                    sqlRetail = "CREATE TABLE MSME_RETAIL_" + cmonth + " as select distinct * " \
                                "from INCENPRG.SALES_" + cmonth + " where SALES_PERSON IN ( " \
                                "select distinct name from INCENPRG.CRM_EMP_LIST " \
                                "where SERVICENO IN (select distinct AM_SID from AREA_MAP_AM))"
                    cursor.execute(sqlRetail)
            except conn.Error as error:
                print('Error occurred:' + str(error))


            # #PACKAGE AND INITIAL CHARGE COMMISION
            # query = "UPDATE MSME_RETAIL_" + cmonth + " SET STATUS = 0"
            # runDb(query)
            #
            # query = "UPDATE MSME_RETAIL_" + cmonth + " SET STATUS = 301 WHERE  CUSROMER_TYPE  LIKE '%SLT%'"
            # runDb(query)
            #
            # query = "UPDATE MSME_RETAIL_" + cmonth + " SET STATUS = 302 WHERE  DSP  IS NULL"
            # runDb(query)
            #
            # query = "UPDATE MSME_RETAIL_" + cmonth + " SET STATUS = 303 WHERE  RTOM  IS NULL"
            # runDb(query)
            #
            # query = "UPDATE MSME_RETAIL_" + cmonth + " SET STATUS = 305 WHERE  SALES_PERSON  IS NULL"
            # runDb(query)
            #
            # query = "UPDATE MSME_RETAIL_" + cmonth + " SET STATUS = 500 WHERE  SERVICE_TYPE  in ('V-VOICE COPPER','V-VOICE','V-VOICE FTTH','BB-INTERNET')"
            # runDb(query)
            #
            # query = "UPDATE MSME_RETAIL_" + cmonth + " SET STATUS = 500 WHERE SERVICE_TYPE <> 'AB-FTTH' AND ORDER_TYPE ='CREATE-UPGRD SAME NO'"
            # runDb(query)
            #
            # query = "UPDATE MSME_RETAIL_" + cmonth + " " \
            #         "SET UPGRADE_TYPE = (SELECT DISTINCT SEOA_DEFAULTVALUE FROM SERVICE_ORDER_ATTRIBUTES " \
            #         "WHERE SEOA_SERO_ID = SO_ID " \
            #         "AND SEOA_NAME = 'TYPE OF MEGA TO FTTH MIGRATION') " \
            #         "WHERE ORDER_TYPE = 'CREATE-UPGRD SAME NO' " \
            #         "AND STATUS = 0 AND SERVICE_TYPE = 'AB-FTTH'"
            # runDb(query)
            #
            # query = "UPDATE MSME_RETAIL_" + cmonth + " SET STATUS = 0 " \
            #         "WHERE ORDER_TYPE = 'CREATE-UPGRD SAME NO' " \
            #         "AND SERVICE_TYPE = 'E-IPTV FTTH' " \
            #         "AND SUBSTR(SERO_OEID,0,INSTR(SERO_OEID,'_')-1) IN  " \
            #         "(SELECT SUBSTR(X.SERO_OEID,0,INSTR(X.SERO_OEID,'_')-1)  FROM MSME_RETAIL_" + cmonth + "  X " \
            #         "WHERE X.ORDER_TYPE = 'CREATE-UPGRD SAME NO' " \
            #         "AND X.SERVICE_TYPE = 'AB-FTTH' " \
            #         "AND X.UPGRADE_TYPE IN ( 'SP to DP PEO','SP to TP','DP BB to TP'))"
            # runDb(query)
            #
            # query = "UPDATE MSME_RETAIL_" + cmonth + " SET STATUS = 0 " \
            #         + "WHERE ORDER_TYPE = 'CREATE-UPGRD SAME NO' " \
            #         + "AND SERVICE_TYPE = 'BB-INTERNET FTTH' " \
            #         + "AND SUBSTR(SERO_OEID,0,INSTR(SERO_OEID,'_')-1) IN " \
            #         + "(SELECT SUBSTR(X.SERO_OEID,0,INSTR(X.SERO_OEID,'_')-1)  FROM MSME_RETAIL_" + cmonth + "  X " \
            #         + "WHERE X.ORDER_TYPE = 'CREATE-UPGRD SAME NO'" \
            #         + "AND X.SERVICE_TYPE = 'AB-FTTH' " \
            #         + "AND X.UPGRADE_TYPE IN ( 'SP to DP BB','SP to TP','DP PEO to TP'))"
            # runDb(query)
            #
            # query = "UPDATE MSME_RETAIL_" + cmonth + " SET SERVICE_PACKAGE = ( " \
            #         "SELECT DISTINCT SEOA_DEFAULTVALUE FROM SERVICE_ORDER_ATTRIBUTES " \
            #         "WHERE SEOA_SERO_ID = SO_ID " \
            #         "AND SEOA_NAME IN ( 'SA_PACKAGE_NAME','IPTV_PACKAGE' , 'BB_PACKAGE_NAME' )    " \
            #         "AND SEOA_DEFAULTVALUE IS NOT NULL) " \
            #         "WHERE SERVICE_PACKAGE IS NULL"
            # runDb(query)
            #
            # try:
            #     with conn.cursor() as cursor:
            #         query = "SELECT TABLE_NAME  FROM INCENPRG.SETTING_TABLE " \
            #                 "WHERE DISCRIPTION = 'BB_COM' " \
            #                 "AND CREATE_DATE < LAST_DAY( ADD_MONTHS(SYSDATE, -4)) " \
            #                 "AND (END_DATE > LAST_DAY( ADD_MONTHS(SYSDATE, -4)) OR END_DATE IS NULL)"
            #         cursor.execute(query)
            #
            #         for row in cursor:
            #             BBCOMLATEST = row[0]
            #
            #     with conn.cursor() as cursor:
            #         query = "SELECT TABLE_NAME   FROM INCENPRG.SETTING_TABLE "\
            #                 "WHERE DISCRIPTION = 'IPTV_COM'  " \
            #                 "AND CREATE_DATE < LAST_DAY( ADD_MONTHS(SYSDATE, -4)) " \
            #                 "AND (END_DATE > LAST_DAY( ADD_MONTHS(SYSDATE, -4)) OR END_DATE IS NULL)"
            #         cursor.execute(query)
            #
            #         for row in cursor:
            #             IPTVCOMLATEST = row[0]
            #
            #     with conn.cursor() as cursor:
            #         query = "SELECT TABLE_NAME  FROM INCENPRG.SETTING_TABLE " \
            #                 "WHERE DISCRIPTION = 'PROD_COM' " \
            #                 "AND CREATE_DATE < LAST_DAY( ADD_MONTHS(SYSDATE, -4)) " \
            #                 "AND (END_DATE > LAST_DAY( ADD_MONTHS(SYSDATE, -4)) OR END_DATE IS NULL)"
            #         cursor.execute(query)
            #
            #         for row in cursor:
            #             PRODCOMLATEST = row[0]
            #
            #     with conn.cursor() as cursor:
            #         query = "SELECT TABLE_NAME   FROM INCENPRG.SETTING_TABLE " \
            #                 "WHERE DISCRIPTION = 'INCEN_RATE' " \
            #                 "AND CREATE_DATE < LAST_DAY( ADD_MONTHS(SYSDATE, -4)) " \
            #                 "AND (END_DATE > LAST_DAY( ADD_MONTHS(SYSDATE, -4)) OR END_DATE IS NULL)"
            #         cursor.execute(query)
            #
            #         for row in cursor:
            #             INCENLATEST = row[0]
            #
            #     with conn.cursor() as cursor:
            #         query = "SELECT TABLE_NAME   FROM INCENPRG.SETTING_TABLE " \
            #                 "WHERE DISCRIPTION = 'TARGET_NONSALE' " \
            #                 "AND CREATE_DATE < LAST_DAY( ADD_MONTHS(SYSDATE, -4)) " \
            #                 "AND (END_DATE > LAST_DAY( ADD_MONTHS(SYSDATE, -4)) OR END_DATE IS NULL)"
            #         cursor.execute(query)
            #
            #         for row in cursor:
            #             TARGETLATEST = row[0]
            #
            #     with conn.cursor() as cursor:
            #         query = "SELECT TABLE_NAME   FROM INCENPRG.SETTING_TABLE " \
            #                 "WHERE DISCRIPTION = 'RTOM_CAT' " \
            #                 "AND CREATE_DATE < LAST_DAY( ADD_MONTHS(SYSDATE, -4)) " \
            #                 "AND (END_DATE > LAST_DAY( ADD_MONTHS(SYSDATE, -4)) OR END_DATE IS NULL)"
            #         cursor.execute(query)
            #
            #         for row in cursor:
            #             RTOMCATLATEST = row[0]
            # except conn.Error as error:
            #     print('Error occurred:' + str(error))
            #
            # #BSS UPDATE
            # svcode = ""
            # try:
            #     with conn.cursor() as cursor:
            #         query = "SELECT SO_ID , REPLACE(CIRCUIT,'(N)','')CIRCUIT , SERVICE_TYPE ,ACC_NO, REG_NO,DSP  " \
            #                 "FROM MSME_RETAIL_" + cmonth + " "\
            #                 "WHERE  DSP is not null AND STATUS = 0 and BSS_STATUS is null"
            #         cursor.execute(query)
            #
            #         for row in cursor:
            #             try:
            #                 with conn.cursor() as cursor2:
            #                     query2 = "SELECT BSS_ID FROM INCENPRG.BSS_PRODUCTMAPPING " \
            #                              "WHERE OSS_SERVICE = :OSS_SERVICE "
            #                     cursor2.execute(query2, [row[2]])
            #
            #                     for row2 in cursor2:
            #                         svcode = row2[0]
            #             except conn.Error as error:
            #                 print('Error occurred:' + str(error))
            #
            #             try:
            #                 with conn.cursor() as cursor3:
            #                     query3 = " SELECT PRODUCT_STATUS ,EFFECTIVE_DTM FROM ( " \
            #                              "SELECT DISTINCT  CPD.CUSTOMER_REF, CHP.PRODUCT_SEQ, AC.ACCOUNT_NUM, " \
            #                              "CHP.PARENT_PRODUCT_SEQ,CHP.PRODUCT_ID, CPS.EFFECTIVE_DTM, " \
            #                              "CPS.PRODUCT_STATUS, CPS.STATUS_REASON_TXT, AC.LAST_BILL_DTM , PRODUCT_LABEL " \
            #                              "FROM  CUSTPRODUCTSTATUS@DBLINK_GENEVA CPS, CUSTHASPRODUCT@DBLINK_GENEVA CHP, " \
            #                              "CUSTPRODUCTDETAILS@DBLINK_GENEVA CPD, PRODUCT@DBLINK_GENEVA PR, ACCOUNT@DBLINK_GENEVA AC " \
            #                              "WHERE CPS.CUSTOMER_REF = CPD.CUSTOMER_REF " \
            #                              "AND CPS.PRODUCT_SEQ = CPD.PRODUCT_SEQ " \
            #                              "AND CHP.CUSTOMER_REF = CPD.CUSTOMER_REF " \
            #                              "AND CHP.PRODUCT_SEQ = CPD.PRODUCT_SEQ " \
            #                              "AND AC.ACCOUNT_NUM = CPD.ACCOUNT_NUM " \
            #                              "AND CHP.PRODUCT_ID  = PR.PRODUCT_ID " \
            #                              "AND CHP.PRODUCT_ID = :PRODUCTID " \
            #                              "AND CHP.PARENT_PRODUCT_SEQ IS NULL " \
            #                              "AND CPS.EFFECTIVE_DTM = (SELECT MAX(EFFECTIVE_DTM) FROM CUSTPRODUCTSTATUS@DBLINK_GENEVA CPQ " \
            #                              "WHERE CPS.CUSTOMER_REF = CPQ.CUSTOMER_REF " \
            #                              "AND CPS.PRODUCT_SEQ = CPQ.PRODUCT_SEQ " \
            #                              "AND EFFECTIVE_DTM < (TO_DATE(:DSP, 'DD-MON-YYYY HH24:MI:SS ')+90) )  " \
            #                              "AND AC.ACCOUNT_NUM  = :ACCOUNT_NUM " \
            #                              "AND (PRODUCT_LABEL = :PRODUCT_LABEL or PRODUCT_LABEL = :PRODUCT_LABEL2)  " \
            #                              "ORDER BY EFFECTIVE_DTM DESC) " \
            #                              "WHERE ROWNUM<2"
            #                     cursor3.execute(query3, [svcode, row[5], row[3], row[1], row[4]])
            #
            #                     for row3 in cursor3:
            #                         print(row3[0],row3[1].strftime("%Y-%m-%d %H:%M:%S")) #2022-06-15 22:00:49
            #                         try:
            #                             with conn.cursor() as cursor4:
            #                                 query4 = "UPDATE MSME_RETAIL_" + cmonth + " SET BSS_STATUS = :BSS_STATUS ," \
            #                                          "BSS_STATUS_DATE =TO_DATE(:BSS_STATUS_DATE, 'YYYY-MM-DD HH24:MI:SS') , " \
            #                                          "ACTIVE_DAYS = ROUND(SYSDATE - TO_DATE(:ACTIVE_DAYS, 'YYYY-MM-DD HH24:MI:SS'))" \
            #                                          "WHERE SO_ID = :SO_ID "
            #                                 cursor4.execute(query4, [row3[0], row3[1].strftime("%Y-%m-%d %H:%M:%S"), row3[1].strftime("%Y-%m-%d %H:%M:%S"), row[0]])
            #                                 conn.commit()
            #                         except conn.Error as error:
            #                             print('Error occurred:' + str(error))
            #             except conn.Error as error:
            #                 print('Error occurred:' + str(error))
            #
            # except conn.Error as error:
            #     print('Error occurred:' + str(error))
            #
            # #PACKAGE COMMISSION UPDATE
            # query = "ALTER TABLE MSME_RETAIL_" + cmonth + "  ADD PKG_COMMISSION VARCHAR2(50)"
            # runDb(query)
            #
            # query="UPDATE MSME_RETAIL_" + cmonth + "  SET PKG_COMMISSION = ( "\
            #       "SELECT  COMMISSION  FROM  INCENPRG."+BBCOMLATEST + " " \
            #       "WHERE SUBSTR(SERVICE_PACKAGE, INSTR(SERVICE_PACKAGE,'_')+1,LENGTH(SERVICE_PACKAGE)) = OSS_NAME) "\
            #       "WHERE  SERVICE_TYPE IN ('BB-INTERNET FTTH' , 'BB-INTERNET COPPER') "\
            #       "AND BSS_STATUS ='OK'"\
            #       "AND STATUS = 0"
            # runDb(query)
            #
            # query= "UPDATE MSME_RETAIL_" + cmonth + "  SET PKG_COMMISSION = (" \
            #        "SELECT  COMMISSION  FROM  INCENPRG."+IPTVCOMLATEST+" " \
            #        "WHERE UPPER(SERVICE_PACKAGE) =  UPPER(PACKAGE_NAME) )" \
            #        "WHERE  SERVICE_TYPE LIKE 'E-IPTV%'" \
            #        "AND BSS_STATUS ='OK'" \
            #        "AND STATUS = 0"
            # runDb(query)


            #CRM PACKAGE UPDATE



            try:
                with conn.cursor() as cursor:
                    sqlInc = "INSERT INTO MSME_INCENT_STAT (YMONTH, RETAIL_READY)  VALUES (:YMONTH, :RETAIL_READY)"
                    cursor.execute(sqlInc,[cmonth,'YES'])
                    conn.commit()
            except conn.Error as error:
                print('Error occurred:' + str(error))


            try:
                with conn.cursor() as cursor:
                    sqlcreate = "CREATE TABLE MSME_SOLPROFIT_" + cmonth + "(CUSTOMER_REF varchar2(20),PSM varchar2(20)," \
                                "ACCOUNT_MANAGER varchar2(30),ACCOUNT_NUM varchar2(30),PRODUCT_LABEL varchar2(100) ," \
                                "PRODUCT_ID varchar2(30),PRODUCT_NAME varchar2(30),PRODUCT varchar2(30) ,SERVICE_NEW1 varchar2(30) ," \
                                "PCATEGORY1 varchar2(30), ONE_TIME varchar2(30),PROFIT varchar2(30))"

                    cursor.execute(sqlcreate)
            except conn.Error as error:
                print('Error occurred:' + str(error))


        except conn.Error as error:
            print('Error occurred:' + str(error))
