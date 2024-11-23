from dateutil.relativedelta import relativedelta
import db
from datetime import datetime, date, timedelta

lstmonth = datetime.now() - relativedelta(months=4)
cmonth = lstmonth.strftime('%Y%m')

last_month = datetime.now() - relativedelta(months=3)
lmon = last_month.replace(day=1) - timedelta(days=1)
pmon = lmon.replace(day=1) - timedelta(days=1)
lastmonth = lmon.strftime('%d-%b-%Y')

last_month = datetime.now() - relativedelta(months=3)
lmon = last_month.replace(day=1) - timedelta(days=1)
pmon = lmon.replace(day=1) - timedelta(days=1)
lastmonth = lmon.strftime('%d-%b-%Y')
premonth = pmon.strftime('%d-%b-%Y')
lmonth = lmon.strftime('%m%Y')
lmonthY = lmon.strftime('%Y%m')
pmonthY = pmon.strftime('%Y%m')


# print(lastmonth)
# print(premonth)
#
# print(lmonth)
# print(lmonthY)
# print(pmonthY)

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


class VoiceCommit():
    def voiceCommit(cmonth):
        sql1 = "drop table con2m"
        runDb(sql1)

        sql2 = "CREATE TABLE con2m  AS "\
        "SELECT chp.* ,cps.EFFECTIVE_DTM p_EFFECTIVE_DTM,PRODUCT_STATUS " \
               "FROM custhasproduct@DBLINK_GENEVA chp , custproductstatus@DBLINK_GENEVA cps " \
               "WHERE chp.customer_ref=cps.customer_ref " \
               "AND chp.product_seq=cps.product_seq " \
               "and cps.PRODUCT_STATUS='OK' " \
               "AND chp.product_id in (1055) " \
               "and trunc(cps.EFFECTIVE_DTM)<= \'"+str(lastmonth) + "\'" \
               "and (cps.customer_ref, cps.product_seq , cps.effective_dtm) in " \
               "(SELECT cps.customer_ref, cps.product_seq , MAX (effective_dtm) effective_dtm " \
               "FROM custproductstatus@DBLINK_GENEVA cps,custhasproduct@DBLINK_GENEVA chp " \
               "where trunc(cps.EFFECTIVE_DTM)<= \'"+str(lastmonth) + "\'" \
               "and chp.customer_ref=cps.customer_ref " \
               "AND chp.product_seq=cps.product_seq " \
               "AND chp.product_id in (1055) " \
               "GROUP BY cps.customer_ref, cps.product_seq)"
        runDb(sql2)

        sql3 = "drop table con3m"
        runDb(sql3)

        sql4 = "CREATE TABLE con3m AS " \
               "select distinct c.*,cpd.ACCOUNT_NUM,cpd.PRODUCT_LABEL, cpd.END_DAT ,NEXT_BILL_DTM " \
               "from con2m  c,custproductdetails@DBLINK_GENEVA cpd,account@DBLINK_GENEVA aa " \
               "where c.CUSTOMER_REF=cpd.CUSTOMER_REF " \
               "and c.PRODUCT_SEQ=cpd.PRODUCT_SEQ " \
               "and cpd.ACCOUNT_NUM=aa.ACCOUNT_NUM " \
               "and (cpd.START_DAT) in ( " \
               "select  max(START_DAT)max_START_DAT " \
               "from custproductdetails@DBLINK_GENEVA cpd " \
               "where cpd.CUSTOMER_REF=c.CUSTOMER_REF " \
               "and cpd.PRODUCT_SEQ=c.PRODUCT_SEQ)"
        runDb(sql4)

        sql5 = "drop table con4m"
        runDb(sql5)

        sql6 = "create table con4m as " \
               "select distinct n.*, START_DAT,c.TARIFF_ID,t.TARIFF_NAME " \
               "from custproducttariffdetails@DBLINK_GENEVA c,con3m n,tariff@DBLINK_GENEVA t " \
               "where n.CUSTOMER_REF=c.CUSTOMER_REF " \
               "and n.PRODUCT_SEQ=c.PRODUCT_SEQ " \
               "and c.TARIFF_ID=t.TARIFF_ID " \
               "and (CATALOGUE_CHANGE_ID=(select MAX( CATALOGUE_CHANGE_ID) from cataloguechange@DBLINK_GENEVA where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3)) " \
               "and (n.CUSTOMER_REF,n.PRODUCT_SEQ, START_DAT)in ( " \
               "select distinct n.CUSTOMER_REF,n.PRODUCT_SEQ, max(START_DAT) " \
               "from custproducttariffdetails@DBLINK_GENEVA c,con3m n " \
               "where n.CUSTOMER_REF=c.CUSTOMER_REF " \
               "and n.PRODUCT_SEQ=c.PRODUCT_SEQ " \
               "group by  n.CUSTOMER_REF,n.PRODUCT_SEQ)"
        runDb(sql6)

        sql7 = "drop table con5m"
        runDb(sql7)

        sql8 = "create table con5m  as " \
               "select distinct c.*,t.START_DAT START_DAT1 from tariffelement@DBLINK_GENEVA  t, con4m c " \
               "where (t.CATALOGUE_CHANGE_ID=(select CATALOGUE_CHANGE_ID from cataloguechange@DBLINK_GENEVA " \
               "where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3)) " \
               "and t.product_id=c.product_id and t.TARIFF_ID=c.TARIFF_ID and t.end_dat is null"
        runDb(sql8)

        sql9 = "drop table con6m"
        runDb(sql9)

        sql10 = "create table  con6m as " \
                "select distinct c.*,t.RECURRING_NUMBER/1000 Rental1,t.ONE_OFF_NUMBER/1000 ONE_OFF_NUMBER " \
                "from tariffelementband@DBLINK_GENEVA  t, con5m  c " \
                "where (t.CATALOGUE_CHANGE_ID=(select CATALOGUE_CHANGE_ID from cataloguechange@DBLINK_GENEVA " \
                "where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3)) " \
                "and t.product_id=c.product_id and t.TARIFF_ID=c.TARIFF_ID and t.START_DAT=c.START_DAT1"
        runDb(sql10)

        sql11 = "drop table  con7m"
        runDb(sql11)

        sql12 = "create table con7m  as " \
                "select distinct CUSTOMER_REF,PRODUCT_SEQ,RECURRING_NUMBER/1000 Override_Rental," \
                "ONE_OFF_NUMBER/1000 Override_ONE_OFF_NUMBER from custoverrideprice@DBLINK_GENEVA c " \
                "where c.END_DAT is null " \
                "and (c.CUSTOMER_REF, c.PRODUCT_SEQ,c.START_DAT) in ( " \
                "select c.CUSTOMER_REF,c.PRODUCT_SEQ,max(c.START_DAT)from custoverrideprice@DBLINK_GENEVA c,con6m cc " \
                "where c.END_DAT is null " \
                "and c.CUSTOMER_REF=cc.CUSTOMER_REF " \
                "and c.PRODUCT_SEQ=cc.PRODUCT_SEQ " \
                "group by c.CUSTOMER_REF,c.PRODUCT_SEQ)"
        runDb(sql12)

        sql13 = "create index g8 on con7m(customer_ref)"
        runDb(sql13)

        sql14 = "create index g9 on con7m(product_seq)"
        runDb(sql14)

        sql15 = "drop table  con8m"
        runDb(sql15)

        sql16 = "create table con8m as " \
            "select c.*, " \
                "(select OVERRIDE_RENTAL from con7m  cc where c.CUSTOMER_REF=cc.CUSTOMER_REF " \
                "and c.PRODUCT_SEQ=cc.PRODUCT_SEQ)OVERRIDE_RENTAL, " \
                "(select Override_ONE_OFF_NUMBER from con7m  cc where c.CUSTOMER_REF=cc.CUSTOMER_REF "\
                "and c.PRODUCT_SEQ=cc.PRODUCT_SEQ)Override_ONE_OFF_NUMBER "\
                "from con6m c"
        runDb(sql16)

        sql17 = "create table MSME_VOICECOMMIT_"+ cmonth +" as " \
                "select a.ACCOUNT_MANAGER ,b.* " \
                "from   con8m   b,CUSTOMERATTRIBUTES@DBLINK_GENEVA a " \
                "where  b.CUSTOMER_REF=a.CUSTOMER_REF(+) " \
                "and to_char(b.P_EFFECTIVE_DTM,'mmyyyy')=\'"+str(lmonth) +"\' "
                #"and to_char(b.P_EFFECTIVE_DTM,'mmyyyy')=\'"+str(lmonth) +"\' "
        runDb(sql17)

        try:
            conn = db.DbConnection.dbconnOssMSME(self="")
            with conn.cursor() as cursor:
                sqlInc = "UPDATE MSME_INCENT_STAT SET VOICE_COMIT_READY = :VOICE_COMIT_READY where YMONTH= :YMONTH"
                cursor.execute(sqlInc,['YES',cmonth])
                conn.commit()
        except conn.Error as error:
            print('Error occurred:' + str(error))

