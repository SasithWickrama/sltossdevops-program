import db

class Revenue():
    def totalRevenue(cmonth):
        print(cmonth[0:4],cmonth[4:6])
        try:
            conn = db.DbConnection.dbconnOssMSME(self="")

            try:
                with conn.cursor() as cursor:
                    sqlRetail = "create table MSME_REVENUE_RE_" + cmonth + " as "\
                                "select distinct aa.CUSTOMER_TYPE,aa.CUSTOMER_REF,aa.ACCOUNT_NO,aa.COST_CENTRE,aa.ACC_MGR, " \
                                "aa.BILLING_MONTH_DESCRIPTION,aa.CODE_NAME,aa.CODE_DESC,aa.REVENUE_AMOUNT, bb.REV_SERVICE,bb.REV_CATAGORY " \
                                "from MSME_REVENUE_" + cmonth + " aa, MSME_REVENUE_CODE bb " \
                                "where aa.CODE_NAME = bb.REV_CODE"
                    cursor.execute(sqlRetail)
            except conn.Error as error:
                print('Error occurred:' + str(error))

            try:
                with conn.cursor() as cursor:
                    sqlmic = "create table MSME_REVENUE_MICRO_" + cmonth + " as  " \
                             "SELECT * FROM( " \
                             "select ACC_MGR , REVENUE_AMOUNT , REV_CATAGORY " \
                             "from MSME_REVENUE_RE_" + cmonth + " " \
                             "where CUSTOMER_TYPE IN ( 'Registered-Micro Biz','Individual-Micro Biz') " \
                             "and REV_CATAGORY <> 'TAX') " \
                             "PIVOT( " \
                             "sum(REVENUE_AMOUNT/1000000) " \
                             "FOR REV_CATAGORY " \
                             "IN ( 'DATA' as dat_ret,'RETAIL' as ret)) " \
                             "where ACC_MGR IN ( select distinct AM_CODE from AREA_MAP_AM)"
                    cursor.execute(sqlmic)
            except conn.Error as error:
                print('Error occurred:' + str(error))

            try:
                with conn.cursor() as cursor:
                    sqlsme = "create table MSME_REVENUE_SME_" + cmonth + " as  " \
                                "SELECT * FROM( " \
                                "select ACC_MGR , REVENUE_AMOUNT , REV_CATAGORY " \
                                "from MSME_REVENUE_RE_" + cmonth + " " \
                                "where CUSTOMER_TYPE NOT IN ( 'Registered-Micro Biz','Individual-Micro Biz') " \
                                "and REV_CATAGORY <> 'TAX') " \
                                "PIVOT( " \
                                "sum(REVENUE_AMOUNT/1000000) " \
                                "FOR REV_CATAGORY " \
                                "IN ( 'DATA' as dat_ret,'RETAIL' as ret)) " \
                                "where ACC_MGR IN ( select distinct AM_CODE from AREA_MAP_AM)"
                    cursor.execute(sqlsme)
            except conn.Error as error:
                print('Error occurred:' + str(error))

            try:
                with conn.cursor() as cursor:
                    sqlcreate = "CREATE TABLE MSME_REV_" + cmonth + " as "\
                                "select aa.ACC_MGR, aa.DAT_RET SME_DATA,aa.RET SME_RETAIL, bb.DAT_RET MICRO_DATA,bb.RET MICRO_RETAIL "\
                                "from MSME_REVENUE_SME_" + cmonth + " aa,MSME_REVENUE_MICRO_" + cmonth + " bb "\
                                "where aa.ACC_MGR = bb.ACC_MGR(+)"
                    cursor.execute(sqlcreate)
            except conn.Error as error:
                print('Error occurred:' + str(error))

            try:
                with conn.cursor() as cursor:
                    ryear= cmonth[0:4]
                    rmon = cmonth[4:6]
                    sql = "create table MSME_REV2_" + cmonth + " as " \
                          "select bb.USR_SID, aa.ACC_MGR,bb.REV_SEG_SMEDATA TGT_SME_DATA,aa.SME_DATA ACH_SME_DATA,round((nvl(aa.SME_DATA,0)/nvl(bb.REV_SEG_SMEDATA,0))*100) SME_DATA_PERC, " \
                          "bb.REV_SEG_SMERETAIL TGT_SME_RETAIL,aa.SME_RETAIL ACH_SME_RETAIL,round((nvl(aa.SME_RETAIL,0)/nvl(bb.REV_SEG_SMERETAIL,0))*100) SME_RETAIL_PERC, " \
                          "(nvl(bb.REV_SEG_SMEDATA,0)+nvl(bb.REV_SEG_SMERETAIL,0)) TGT_TOT_SME, (nvl(aa.SME_DATA,0)+nvl(aa.SME_RETAIL,0))ACH_TOT_SME, " \
                          "round((nvl(aa.SME_DATA,0)+nvl(aa.SME_RETAIL,0)) / (nvl(bb.REV_SEG_SMEDATA,0)+nvl(bb.REV_SEG_SMERETAIL,0) )*100) SME_TOT_PERC, " \
                          "bb.REV_SEG_MICRODATA TGT_MICRO_DATA,aa.MICRO_DATA ACH_MICRO_DATA,round((nvl(aa.MICRO_DATA,0)/nvl(bb.REV_SEG_MICRODATA,0))*100) MICRO_DATA_PERC, " \
                          "bb.REV_SEG_MICRORETAIL TGT_MICRO_RETAIL,aa.MICRO_RETAIL ACH_MICRO_RETAIL,round((nvl(aa.MICRO_RETAIL,0)/nvl(bb.REV_SEG_MICRORETAIL,0))*100) MICRO_RETAIL_PERC, " \
                          "(nvl(bb.REV_SEG_MICRODATA,0)+nvl(bb.REV_SEG_MICRORETAIL,0)) TGT_TOT_MICRO, (nvl(aa.MICRO_DATA,0)+nvl(aa.MICRO_RETAIL,0))ACH_TOT_MICRO, " \
                          "round((nvl(aa.MICRO_DATA,0)+nvl(aa.MICRO_RETAIL,0)) / (nvl(bb.REV_SEG_MICRODATA,0)+nvl(bb.REV_SEG_MICRORETAIL,0) )*100) MICRO_TOT_PERC, " \
                          "(nvl(bb.REV_SEG_SMEDATA,0)+nvl(bb.REV_SEG_SMERETAIL,0)+nvl(bb.REV_SEG_MICRODATA,0)+nvl(bb.REV_SEG_MICRORETAIL,0)) TGT_TOT, " \
                          "(nvl(aa.SME_DATA,0)+nvl(aa.SME_RETAIL,0)+nvl(aa.MICRO_DATA,0)+nvl(aa.MICRO_RETAIL,0)) ACH_TOT, " \
                          "round(((nvl(aa.SME_DATA,0)+nvl(aa.SME_RETAIL,0)+nvl(aa.MICRO_DATA,0)+nvl(aa.MICRO_RETAIL,0))/(nvl(bb.REV_SEG_SMEDATA,0)+nvl(bb.REV_SEG_SMERETAIL,0)+nvl(bb.REV_SEG_MICRODATA,0)+nvl(bb.REV_SEG_MICRORETAIL,0))*100)) TOT_PERC " \
                          "from MSME_REV_" + cmonth + " aa,MSME_REV_TARGETS bb " \
                          "where aa.ACC_MGR = bb.AM_CODE" \
                          "and bb.REV_YEAR = \'"+str(ryear) + "\' " \
                          "and bb.REV_MON =\'"+str(rmon) + "\'"

                    print(sql)
                    cursor.execute(sql)

            except Exception as error:
                print('Error occurred:' + str(error))



        except conn.Error as error:
            print('Error occurred:' + str(error))
