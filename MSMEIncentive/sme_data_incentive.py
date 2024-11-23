from dateutil.relativedelta import relativedelta
import db
from datetime import datetime, date, timedelta

last_month = datetime.now() - relativedelta(months=3)
lmon = last_month.replace(day=1) - timedelta(days=1)
pmon = lmon.replace(day=1) - timedelta(days=1)
lastmonth = lmon.strftime('%d-%b-%Y')
premonth = pmon.strftime('%d-%b-%Y')
lmonth = lmon.strftime('%m%Y')
lmonthY = lmon.strftime('%Y%m')
pmonthY = pmon.strftime('%Y%m')


print('lmon'+lastmonth)
print('pmon'+premonth)

print('l2mon'+lmonth)
print('l2monY'+lmonthY)
print('p2monY'+pmonthY)


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

class Data():
    def dataData(cmonth):

        sql1 = "drop table  sme1"
        runDb(sql1)

        sql2 = "drop table  sme2"
        runDb(sql2)

        sql3 = "drop table  sme3"
        runDb(sql3)

        sql4 = "drop table  sme4"
        runDb(sql4)

        sql5 = "drop table  sme5"
        runDb(sql5)

        sql6 = "drop table  sme6"
        runDb(sql6)

        sql7 = "drop table  sme_31_may_2012"
        runDb(sql7)

        sqlc1 = "create table sme1 as select CUSTOMER_REF,ACCOUNT_MANAGER " \
                "from customerattributes@DBLINK_GENEVA " \
                "where ACCOUNT_MANAGER like \'SME%\'"
        runDb(sqlc1)

        sqlc2 = "CREATE TABLE sme2 AS " \
                "SELECT cps.customer_ref, product_seq ,ACCOUNT_MANAGER, MAX (effective_dtm) effective_dtm " \
                "FROM custproductstatus@DBLINK_GENEVA cps,sme1  s " \
                "where s.CUSTOMER_REF=cps.CUSTOMER_REF and " \
                "trunc(cps.EFFECTIVE_DTM)<= \'"+str(premonth) + "\'"\
                " GROUP BY cps.customer_ref, product_seq,ACCOUNT_MANAGER"
        runDb(sqlc2)

        sqlc3 = "CREATE TABLE sme3  AS " \
                "SELECT  chp.* ,me.EFFECTIVE_DTM p_EFFECTIVE_DTM,PRODUCT_STATUS ,ACCOUNT_MANAGER,cps.STATUS_REASON_TXT " \
                "FROM custhasproduct@DBLINK_GENEVA chp , custproductstatus@DBLINK_GENEVA cps , sme2  me " \
                "WHERE chp.customer_ref=cps.customer_ref " \
                "AND chp.product_seq=cps.product_seq " \
                "AND cps.customer_ref=me.customer_ref " \
                "AND cps.product_seq=me.product_seq " \
                "AND cps.effective_dtm=me.effective_dtm " \
                "and cps.PRODUCT_STATUS in ('OK','SU','TX') " \
                "and trunc(cps.EFFECTIVE_DTM)<=\'"+str(premonth)+"\'"
        runDb(sqlc3)

        sqlc4 = "create table sme4 as " \
                "select distinct a.CUSTOMER_REF,a.PRODUCT_SEQ,a.PRODUCT_ID,a.P_EFFECTIVE_DTM,PRODUCT_STATUS ,ACCOUNT_MANAGER,STATUS_REASON_TXT,  max(START_DAT)max_START_DAT " \
                "from sme3 a,custproductdetails@DBLINK_GENEVA c " \
                "where a.CUSTOMER_REF=c.CUSTOMER_REF " \
                "and a.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                "group by a.CUSTOMER_REF,a.PRODUCT_SEQ,a.PRODUCT_ID,a.P_EFFECTIVE_DTM,PRODUCT_STATUS,ACCOUNT_MANAGER,STATUS_REASON_TXT "
        runDb(sqlc4)

        sqlc5 = "create table sme5 as " \
                "select distinct c.*,cpd.ACCOUNT_NUM,cpd.PRODUCT_LABEL, cpd.END_DAT " \
                "from sme4  c,custproductdetails@DBLINK_GENEVA cpd " \
                "where c.CUSTOMER_REF=cpd.CUSTOMER_REF " \
                "and c.PRODUCT_SEQ=cpd.PRODUCT_SEQ " \
                "and c.MAX_START_DAT=cpd.START_DAT "
        runDb(sqlc5)

        sqlc6 = "create table sme6  as " \
                "select distinct c.*,a.CUSTOMER_SEGMENT,a.BILLING_CENTRE from sme5  c,accountattributes@DBLINK_GENEVA a " \
                "where c.ACCOUNT_NUM=a.ACCOUNT_NUM "
        runDb(sqlc6)

        sqlc7 = "create table sme_31_may_2012 as select * from sme6"
        runDb(sqlc7)


        sql22 = "drop table  sme2"
        runDb(sql22)

        sql23 = "drop table  sme3"
        runDb(sql23)

        sql24 = "drop table  sme4"
        runDb(sql24)

        sql25 = "drop table  sme5"
        runDb(sql25)

        sql26 = "drop table  sme6"
        runDb(sql26)

        sql27 = "drop table sme_30_jun_2012"
        runDb(sql27)


        sqlc22 = "CREATE TABLE sme2 AS " \
                "SELECT cps.customer_ref, product_seq ,ACCOUNT_MANAGER, MAX (effective_dtm) effective_dtm " \
                "FROM custproductstatus@DBLINK_GENEVA cps,sme1  s " \
                "where s.CUSTOMER_REF=cps.CUSTOMER_REF and " \
                "trunc(cps.EFFECTIVE_DTM)<=\'"+ str(lastmonth) +"\' "\
                " GROUP BY cps.customer_ref, product_seq,ACCOUNT_MANAGER"
        runDb(sqlc22)

        sqlc23 = "CREATE TABLE sme3  AS " \
                "SELECT  chp.* ,me.EFFECTIVE_DTM p_EFFECTIVE_DTM,PRODUCT_STATUS ,ACCOUNT_MANAGER,cps.STATUS_REASON_TXT " \
                "FROM custhasproduct@DBLINK_GENEVA chp , custproductstatus@DBLINK_GENEVA cps , sme2  me " \
                "WHERE chp.customer_ref=cps.customer_ref " \
                "AND chp.product_seq=cps.product_seq " \
                "AND cps.customer_ref=me.customer_ref " \
                "AND cps.product_seq=me.product_seq " \
                "AND cps.effective_dtm=me.effective_dtm " \
                "and cps.PRODUCT_STATUS in ('OK','SU','TX') " \
                "and trunc(cps.EFFECTIVE_DTM)<=\'"+str(lastmonth)+"\' "
        runDb(sqlc23)

        sqlc24 = "create table sme4 as " \
                "select distinct a.CUSTOMER_REF,a.PRODUCT_SEQ,a.PRODUCT_ID,a.P_EFFECTIVE_DTM,PRODUCT_STATUS ,ACCOUNT_MANAGER,STATUS_REASON_TXT,  max(START_DAT)max_START_DAT " \
                "from sme3 a,custproductdetails@DBLINK_GENEVA c " \
                "where a.CUSTOMER_REF=c.CUSTOMER_REF " \
                "and a.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                "group by a.CUSTOMER_REF,a.PRODUCT_SEQ,a.PRODUCT_ID,a.P_EFFECTIVE_DTM,PRODUCT_STATUS,ACCOUNT_MANAGER,STATUS_REASON_TXT "
        runDb(sqlc24)

        sqlc25 = "create table sme5 as " \
                "select distinct c.*,cpd.ACCOUNT_NUM,cpd.PRODUCT_LABEL, cpd.END_DAT " \
                "from sme4  c,custproductdetails@DBLINK_GENEVA cpd " \
                "where c.CUSTOMER_REF=cpd.CUSTOMER_REF " \
                "and c.PRODUCT_SEQ=cpd.PRODUCT_SEQ " \
                "and c.MAX_START_DAT=cpd.START_DAT "
        runDb(sqlc25)

        sqlc26 = "create table sme6  as " \
                "select distinct c.*,a.CUSTOMER_SEGMENT,a.BILLING_CENTRE from sme5  c,accountattributes@DBLINK_GENEVA a " \
                "where c.ACCOUNT_NUM=a.ACCOUNT_NUM "
        runDb(sqlc26)

        sqlc27 = "create table sme_30_jun_2012 as select * from sme6"
        runDb(sqlc27)


        sqln2 = "drop table  sme_n2"
        runDb(sqln2)

        sqln3 = "drop table  sme_n3"
        runDb(sqln3)

        sqln4 = "drop table  sme_n4"
        runDb(sqln4)

        sqln5 = "drop table  sme_n5"
        runDb(sqln5)

        sqln6 = "drop table  sme_n6"
        runDb(sqln6)

        sqln7 = "drop table  sme_n7"
        runDb(sqln7)

        sqln8 = "drop table  sme_n8"
        runDb(sqln8)

        sqln9 = "drop table  sme_n9"
        runDb(sqln9)

        sqln61 = "drop table  sme_n6_1"
        runDb(sqln61)

        sqln71 = "drop table  sme_n7_1"
        runDb(sqln71)

        sqln81 = "drop table  sme_n8_1"
        runDb(sqln81)

        sqlb2 = "drop table  b2"
        runDb(sqlb2)

        sqln911 = "drop table  sme_n9_11"
        runDb(sqln911)

        sqln912 = "drop table  sme_n9_12"
        runDb(sqln912)

        sqln913 = "drop table  sme_n9_13"
        runDb(sqln913)


        sqlcn2 = "CREATE TABLE sme_n2 as " \
                 "SELECT cps. customer_ref, product_seq ,  effective_dtm  ,ACCOUNT_MANAGER " \
                 "FROM custproductstatus@DBLINK_GENEVA cps,sme1 s " \
                 "where  cps.CUSTOMER_REF=s.CUSTOMER_REF " \
                 "and to_char(trunc(cps.EFFECTIVE_DTM),'mmyyyy')= \'"+ str(lmonth) +"\' " \
                 "and cps.PRODUCT_STATUS in ('OK','TX','SU')"
        runDb(sqlcn2)

        sqlcn3 = "CREATE TABLE sme_n3 AS " \
                 "SELECT /*+ parallel(chp,10) parallel(cps,10) parallel(me,10) */ chp.* ,me.effective_dtm p_effective_dtm,cps.PRODUCT_STATUS,STATUS_REASON_TXT,ACCOUNT_MANAGER " \
                 "FROM custhasproduct@DBLINK_GENEVA chp , custproductstatus@DBLINK_GENEVA cps , sme_n2 me " \
                 "WHERE chp.customer_ref=cps.customer_ref " \
                 "AND chp.product_seq=cps.product_seq " \
                 "AND cps.customer_ref=me.customer_ref " \
                 "AND cps.product_seq=me.product_seq " \
                 "AND cps.effective_dtm=me.effective_dtm " \
                 "and cps.PRODUCT_STATUS in ('OK','TX','SU') " \
                 "and chp.CUSTOMER_REF=me.CUSTOMER_REF " \
                 "and chp.PRODUCT_SEQ=me.PRODUCT_SEQ " \
                 "and to_char(trunc(cps.EFFECTIVE_DTM),'mmyyyy')= \'"+ str(lmonth) +"\' "
        runDb(sqlcn3)

        sqlcn4 = "create table sme_n4  as " \
                 "select distinct a.CUSTOMER_REF,a.PRODUCT_SEQ,a.PRODUCT_ID,a.P_EFFECTIVE_DTM,PRODUCT_STATUS ,ACCOUNT_MANAGER,STATUS_REASON_TXT,  max(START_DAT)max_START_DAT " \
                 "from sme_n3  a,custproductdetails@DBLINK_GENEVA c " \
                 "where a.CUSTOMER_REF=c.CUSTOMER_REF " \
                 "and a.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                 "group by a.CUSTOMER_REF,a.PRODUCT_SEQ,a.PRODUCT_ID,a.P_EFFECTIVE_DTM,PRODUCT_STATUS,ACCOUNT_MANAGER,STATUS_REASON_TXT"
        runDb(sqlcn4)

        sqlcn5 = "create table sme_n5  as " \
                 "select distinct c.*,cpd.ACCOUNT_NUM,cpd.PRODUCT_LABEL, cpd.END_DAT " \
                 "from sme_n4   c,custproductdetails@DBLINK_GENEVA cpd " \
                 "where c.CUSTOMER_REF=cpd.CUSTOMER_REF " \
                 "and c.PRODUCT_SEQ=cpd.PRODUCT_SEQ " \
                 "and c.MAX_START_DAT=cpd.START_DAT"
        runDb(sqlcn5)

        sqlcn6 = "create table sme_n6 as " \
                 "select distinct s.*,p.PRODUCT_NAME from sme_n5 s,product@DBLINK_GENEVA p " \
                 "where s.PRODUCT_ID=p.PRODUCT_ID " \
                 "and s.PRODUCT_STATUS in ('OK') "
        runDb(sqlcn6)

        sqlcn7 = "create table sme_n7 as " \
                 "select ACCOUNT_MANAGER,CUSTOMER_REF,PRODUCT_SEQ,PRODUCT_STATUS,P_EFFECTIVE_DTM,a.ACCOUNT_NUM,PRODUCT_LABEL,PRODUCT_ID,PRODUCT_NAME,s.STATUS_REASON_TXT,max(a.EFFECTIVE_DTM)a_EFFECTIVE_DTM " \
                 "from sme_n6 s,accountstatus@DBLINK_GENEVA a " \
                 "where s.ACCOUNT_NUM=a.ACCOUNT_NUM " \
                 "group by ACCOUNT_MANAGER,CUSTOMER_REF,PRODUCT_SEQ,PRODUCT_STATUS,P_EFFECTIVE_DTM,a.ACCOUNT_NUM,PRODUCT_LABEL,PRODUCT_ID,PRODUCT_NAME,s.STATUS_REASON_TXT"
        runDb(sqlcn7)
        #
        sqlcn8 = "create table sme_n8 as " \
                 "select ACCOUNT_MANAGER,CUSTOMER_REF,PRODUCT_SEQ,PRODUCT_STATUS,P_EFFECTIVE_DTM Product_start_date,a.ACCOUNT_NUM,PRODUCT_LABEL,PRODUCT_ID,PRODUCT_NAME,a_EFFECTIVE_DTM Account_startdate ,a.ACCOUNT_STATUS,s.STATUS_REASON_TXT " \
                 "from sme_n7 s,accountstatus@DBLINK_GENEVA a " \
                 "where s.ACCOUNT_NUM=a.ACCOUNT_NUM " \
                 "and s.A_EFFECTIVE_DTM=a.EFFECTIVE_DTM"
        runDb(sqlcn8)

        sqlcn9 = "create table sme_n9 as " \
                 "select distinct * from sme_n8"
        runDb(sqlcn9)

        sqlcn61 = "create table sme_n6_1 as " \
                  "select distinct s.*,p.PRODUCT_NAME from sme_n5 s,product@DBLINK_GENEVA p " \
                  "where s.PRODUCT_ID=p.PRODUCT_ID " \
                  "and s.PRODUCT_STATUS in ('TX') "
        runDb(sqlcn61)

        sqlcn71 = "create table sme_n7_1 as " \
                  "select ACCOUNT_MANAGER,CUSTOMER_REF,PRODUCT_SEQ,PRODUCT_STATUS,P_EFFECTIVE_DTM,a.ACCOUNT_NUM,PRODUCT_ID,PRODUCT_NAME,s.STATUS_REASON_TXT,max(a.EFFECTIVE_DTM)a_EFFECTIVE_DTM " \
                  "from sme_n6_1 s,accountstatus@DBLINK_GENEVA a " \
                  "where s.ACCOUNT_NUM=a.ACCOUNT_NUM " \
                  "group by ACCOUNT_MANAGER,CUSTOMER_REF,PRODUCT_SEQ,PRODUCT_STATUS,P_EFFECTIVE_DTM,a.ACCOUNT_NUM,PRODUCT_ID,PRODUCT_NAME,s.STATUS_REASON_TXT"
        runDb(sqlcn71)

        sqlcn81 = "create table sme_n8_1 as " \
                  "select ACCOUNT_MANAGER,CUSTOMER_REF,PRODUCT_SEQ,PRODUCT_STATUS,P_EFFECTIVE_DTM Product_Disconnection_date,a.ACCOUNT_NUM,PRODUCT_ID,PRODUCT_NAME,a_EFFECTIVE_DTM Account_startdate ,a.ACCOUNT_STATUS,s.STATUS_REASON_TXT " \
                  "from sme_n7_1 s,accountstatus@DBLINK_GENEVA a " \
                  "where s.ACCOUNT_NUM=a.ACCOUNT_NUM " \
                  "and s.A_EFFECTIVE_DTM=a.EFFECTIVE_DTM"
        runDb(sqlcn81)

        sqlcb2 = "create table b2 as " \
                 "select distinct s.CUSTOMER_REF,s.PRODUCT_SEQ,s.PRODUCT_ID,ss.PRODUCT_STATUS " \
                 "from sme_n6_1 s,sme_30_jun_2012 ss " \
                 "where  s.CUSTOMER_REF=ss.CUSTOMER_REF " \
                 "and s.PRODUCT_ID=ss.PRODUCT_ID " \
                 "and s.PRODUCT_LABEL= ss.PRODUCT_LABEL " \
                 "and ss.PRODUCT_STATUS in ('OK','SU') "
        runDb(sqlcb2)

        sqlcn911 = "create table sme_n9_11 as " \
                "select distinct * from  sme_n8_1 " \
                "where (CUSTOMER_REF,PRODUCT_SEQ,PRODUCT_ID) not in " \
                "(select distinct CUSTOMER_REF,PRODUCT_SEQ,PRODUCT_ID from b2)"
        runDb(sqlcn911)

        sqlcn912 = "create table sme_n9_12 as " \
                "select distinct p.*,c.EFFECTIVE_DTM Latest_ProductActivation11,c.PRODUCT_STATUS Latest_active_STATUS11  from custproductstatus@DBLINK_GENEVA c, sme_n9_11 p " \
                "where c.CUSTOMER_REF=p.CUSTOMER_REF " \
                "and c.PRODUCT_SEQ=p.PRODUCT_SEQ " \
                "and (c.CUSTOMER_REF,c.PRODUCT_SEQ,c.EFFECTIVE_DTM) in ( " \
                "select c.CUSTOMER_REF,c.PRODUCT_SEQ,max(c.EFFECTIVE_DTM) from custproductstatus@DBLINK_GENEVA c, sme_n9_11 p " \
                "where c.CUSTOMER_REF=p.CUSTOMER_REF " \
                "and c.PRODUCT_SEQ=p.PRODUCT_SEQ " \
                "and to_char(c.EFFECTIVE_DTM,'yyyymmdd')<to_char(p.PRODUCT_DISCONNECTION_DATE,'yyyymmdd') " \
                "group by c.CUSTOMER_REF,c.PRODUCT_SEQ)"
        runDb(sqlcn912)

        sqlcn913 = "create table sme_n9_13 as " \
                "select * from sme_n9_12 " \
                "where LATEST_ACTIVE_STATUS11 !=\'PE\' "
        runDb(sqlcn913)


        sqli11 = "drop table  i11"
        runDb(sqli11)

        sqlh1 = "drop table  h1"
        runDb(sqlh1)

        sql50 = "drop table  sme_31_jan_2011_t"
        runDb(sql50)

        sql51 = "drop table  sme_31_jan_2011_t1"
        runDb(sql51)

        sql52 = "drop table  sme_31_dec_2010_t"
        runDb(sql52)

        sql53 = "drop table  sme_28_feb_2011_t1"
        runDb(sql53)

        sql54 = "drop table  sme_pack_change"
        runDb(sql54)

        sqlh12 = "drop table  h1_2"
        runDb(sqlh12)

        sqlh13 = "drop table  h1_3"
        runDb(sqlh13)

        sqlh14 = "drop table  h1_4"
        runDb(sqlh14)

        sqlch15 = "drop table  h1_5"
        runDb(sqlch15)

        sqlh16 = "drop table  h1_6"
        runDb(sqlh16)

        sqlh17 = "drop table  h1_7"
        runDb(sqlh17)

        sqlh18 = "drop table  h1_8"
        runDb(sqlh18)

        sqlh19 = "drop table  h1_9"
        runDb(sqlh19)

        sqlci11 = "create table i11 as " \
                  "select distinct s.CUSTOMER_REF,s.PRODUCT_SEQ,s.PRODUCT_ID " \
                  "from sme_n6 s,sme_31_may_2012 ss " \
                  "where  s.product_id not in (1139) " \
                  "and s.CUSTOMER_REF=ss.CUSTOMER_REF " \
                  "and s.PRODUCT_ID=ss.PRODUCT_ID " \
                  "and s.PRODUCT_LABEL=ss.PRODUCT_LABEL " \
                  "and s.PRODUCT_SEQ=ss.PRODUCT_SEQ " \
                  "and s.PRODUCT_ID !=1139"
        runDb(sqlci11)

        sqlch1 = "create table h1 as " \
                 "select * from sme_n8 " \
                 "where product_id  not in (1139,585,1005,101) " \
                 "and PRODUCT_STATUS='OK' " \
                 "and (CUSTOMER_REF,PRODUCT_label,PRODUCT_ID) in ( " \
                 "select CUSTOMER_REF,PRODUCT_label,PRODUCT_ID from sme_n8 " \
                 "where product_id  not in (1139,585,1005,101) " \
                 "and PRODUCT_STATUS='OK' " \
                 "minus " \
                 "select CUSTOMER_REF,PRODUCT_label,PRODUCT_ID from  sme_31_may_2012 where PRODUCT_STATUS in ('OK','SU'))"
        runDb(sqlch1)

        sqlc50 = "create table sme_31_jan_2011_t as " \
                 "select  n.CUSTOMER_REF,n.PRODUCT_SEQ,ACCOUNT_NUM,PRODUCT_ID,P_EFFECTIVE_DTM,PRODUCT_STATUS,PRODUCT_LABEL, " \
                 "BILLING_CENTRE,CUSTOMER_SEGMENT,ACCOUNT_MANAGER,STATUS_REASON_TXT, max(START_DAT)t_START_DAT " \
                 "from custproducttariffdetails@DBLINK_GENEVA c,sme_30_jun_2012 n " \
                 "where n.CUSTOMER_REF=c.CUSTOMER_REF " \
                 "and n.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                 "and to_char(START_DAT,'yyyymm')<= \'"+ str(lmonthY) +"\' " \
                 "group by  n.CUSTOMER_REF,n.PRODUCT_SEQ,ACCOUNT_NUM,PRODUCT_ID,P_EFFECTIVE_DTM,PRODUCT_STATUS,PRODUCT_LABEL, " \
                 "BILLING_CENTRE,CUSTOMER_SEGMENT,ACCOUNT_MANAGER,n.PRODUCT_SEQ,STATUS_REASON_TXT"
        runDb(sqlc50)

        sqlc51 = "create table sme_31_jan_2011_t1 as " \
                 "select distinct p.*,c.TARIFF_ID,t.TARIFF_NAME " \
                 "from  sme_31_jan_2011_t  p,custproducttariffdetails@DBLINK_GENEVA c,tariff@DBLINK_GENEVA t " \
                 "where p.CUSTOMER_REF=c.CUSTOMER_REF " \
                 "and p.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                 "and p.T_START_DAT=c.START_DAT " \
                 "and c.TARIFF_ID=t.TARIFF_ID " \
                 "and (CATALOGUE_CHANGE_ID=(select CATALOGUE_CHANGE_ID from cataloguechange@DBLINK_GENEVA where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3))"
        runDb(sqlc51)

        sqlc52 = "create table sme_31_dec_2010_t as " \
                 "select  n.CUSTOMER_REF,n.PRODUCT_SEQ,ACCOUNT_NUM,PRODUCT_ID,P_EFFECTIVE_DTM,PRODUCT_STATUS,PRODUCT_LABEL, " \
                 "BILLING_CENTRE,CUSTOMER_SEGMENT,ACCOUNT_MANAGER,STATUS_REASON_TXT, max(START_DAT)t_START_DAT " \
                 "from custproducttariffdetails@DBLINK_GENEVA c,sme_31_may_2012  n " \
                 "where n.CUSTOMER_REF=c.CUSTOMER_REF " \
                 "and n.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                 "and to_char(START_DAT,'yyyymm')<= \'" + str(pmonthY) + "\' "\
                 "group by  n.CUSTOMER_REF,n.PRODUCT_SEQ,ACCOUNT_NUM,PRODUCT_ID,P_EFFECTIVE_DTM,PRODUCT_STATUS,PRODUCT_LABEL, " \
                 "BILLING_CENTRE,CUSTOMER_SEGMENT,ACCOUNT_MANAGER,STATUS_REASON_TXT,n.PRODUCT_SEQ"
        runDb(sqlc52)

        sqlc53 = "create table sme_28_feb_2011_t1 as " \
                 "select distinct p.*,c.TARIFF_ID,t.TARIFF_NAME ,c.end_dat " \
                 "from  sme_31_dec_2010_t  p,custproducttariffdetails@DBLINK_GENEVA c,tariff@DBLINK_GENEVA t " \
                 "where p.CUSTOMER_REF=c.CUSTOMER_REF " \
                 "and p.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                 "and p.T_START_DAT=c.START_DAT " \
                 "and c.TARIFF_ID=t.TARIFF_ID " \
                 "and (CATALOGUE_CHANGE_ID=(select CATALOGUE_CHANGE_ID from cataloguechange@DBLINK_GENEVA where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3))"
        runDb(sqlc53)

        sqlc54 = "create  table sme_pack_change as " \
                 "select s.* ,b.TARIFF_ID PREVIOUS_TARIFF_ID,b.TARIFF_NAME PREVIOUS_PRODUCT,b.end_dat " \
                 "from  sme_31_jan_2011_t1 s, sme_28_feb_2011_t1 b " \
                 "where s.CUSTOMER_REF=b.CUSTOMER_REF " \
                 "and s.PRODUCT_SEQ=b.PRODUCT_SEQ " \
                 "and s.TARIFF_ID !=b.TARIFF_ID " \
                 "and s.TARIFF_NAME !=b.TARIFF_NAME"
        runDb(sqlc54)

        sqlch12 = "create table  h1_2 as " \
                  "select  distinct n.*, START_DAT,c.TARIFF_ID,t.TARIFF_NAME " \
                  "from custproducttariffdetails@DBLINK_GENEVA c, h1 n,tariff@DBLINK_GENEVA t " \
                  "where n.CUSTOMER_REF=c.CUSTOMER_REF " \
                  "and n.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                  "and c.TARIFF_ID=t.TARIFF_ID " \
                  "and (CATALOGUE_CHANGE_ID=(select CATALOGUE_CHANGE_ID from cataloguechange@DBLINK_GENEVA where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3)) " \
                  "and (n.CUSTOMER_REF,n.PRODUCT_SEQ, START_DAT)in ( " \
                  "select  distinct n.CUSTOMER_REF,n.PRODUCT_SEQ, max(START_DAT) " \
                  "from custproducttariffdetails@DBLINK_GENEVA c, h1 n " \
                  "where n.CUSTOMER_REF=c.CUSTOMER_REF " \
                  "and n.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                  "group by  n.CUSTOMER_REF,n.PRODUCT_SEQ)"
        runDb(sqlch12)

        sqlch13 = "create table  h1_3 as " \
                  "select n.CUSTOMER_REF,n.PRODUCT_SEQ, sum(CHARGE_COST_MNY/1000) CHARGE_COST_MNY from h1_2 n,billproductcharge@DBLINK_GENEVA c " \
                  "where n.CUSTOMER_REF=c.CUSTOMER_REF " \
                  "and n.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                  "and (n.CUSTOMER_REF,n.PRODUCT_SEQ,CHARGE_SEQ) in ( " \
                  "select n.CUSTOMER_REF,n.PRODUCT_SEQ,max(CHARGE_SEQ) from h1_2 n,billproductcharge@DBLINK_GENEVA c " \
                  "where n.CUSTOMER_REF=c.CUSTOMER_REF " \
                  "and n.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                  "group by n.CUSTOMER_REF,n.PRODUCT_SEQ) " \
                  "group by n.CUSTOMER_REF,n.PRODUCT_SEQ"
        runDb(sqlch13)

        sqlch14 = "create table  h1_4 as " \
                  "select c.*, CHARGE_COST_MNY  from h1_3 n,h1_2 c " \
                  "where n.CUSTOMER_REF(+)=c.CUSTOMER_REF " \
                  "and n.PRODUCT_SEQ(+)=c.PRODUCT_SEQ"
        runDb(sqlch14)

        sqlch15 = "create table h1_5  as " \
                  "select distinct c.*,t.START_DAT START_DAT1 from tariffelement@DBLINK_GENEVA  t, h1_4 c " \
                  "where (t.CATALOGUE_CHANGE_ID=(select CATALOGUE_CHANGE_ID from cataloguechange@DBLINK_GENEVA where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3)) " \
                  "and t.product_id=c.product_id and t.TARIFF_ID=c.TARIFF_ID and t.end_dat is null"
        runDb(sqlch15)

        sqlch16 = "create table  h1_6 as " \
                  "select distinct c.*,t.RECURRING_NUMBER/1000 Rental,t.ONE_OFF_NUMBER/1000 ONE_OFF_NUMBER from tariffelementband@DBLINK_GENEVA  t, h1_5  c " \
                  "where (t.CATALOGUE_CHANGE_ID=(select CATALOGUE_CHANGE_ID from cataloguechange@DBLINK_GENEVA where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3)) " \
                  "and t.product_id=c.product_id and t.TARIFF_ID=c.TARIFF_ID and t.START_DAT=c.START_DAT1"
        runDb(sqlch16)

        sqlch17 = "create table h1_7  as " \
                  "select distinct CUSTOMER_REF,PRODUCT_SEQ,RECURRING_NUMBER/1000 Override_Rental,ONE_OFF_NUMBER/1000 Override_ONE_OFF_NUMBER from custoverrideprice@DBLINK_GENEVA c " \
                  "where c.END_DAT is null " \
                  "and (c.CUSTOMER_REF, c.PRODUCT_SEQ,c.START_DAT) in ( " \
                  "select c.CUSTOMER_REF,c.PRODUCT_SEQ,max(c.START_DAT)from custoverrideprice@DBLINK_GENEVA c,h1_6 cc " \
                  "where c.END_DAT is null " \
                  "and c.CUSTOMER_REF=cc.CUSTOMER_REF " \
                  "and c.PRODUCT_SEQ=cc.PRODUCT_SEQ " \
                  "group by c.CUSTOMER_REF,c.PRODUCT_SEQ)"
        runDb(sqlch17)

        sqlch18 = "create table h1_8 as " \
                  "select c.*, " \
                  "(select OVERRIDE_RENTAL from h1_7   cc where c.CUSTOMER_REF=cc.CUSTOMER_REF " \
                  "and c.PRODUCT_SEQ=cc.PRODUCT_SEQ)OVERRIDE_RENTAL, " \
                  "(select Override_ONE_OFF_NUMBER from h1_7   cc where c.CUSTOMER_REF=cc.CUSTOMER_REF " \
                  "and c.PRODUCT_SEQ=cc.PRODUCT_SEQ)Override_ONE_OFF_NUMBER " \
                  "from h1_6 c"
        runDb(sqlch18)

        sqlch19 = "create table h1_9 as " \
                  "select h.* from h1_8 h,product@DBLINK_GENEVA t,PRODUCTHASPARENTPRODUCT@DBLINK_GENEVA p " \
                  "where h.PRODUCT_ID=t.PRODUCT_ID " \
                  "and p.PRODUCT_ID(+)=t.PRODUCT_ID"
        runDb(sqlch19)

        sqlc1 = "drop table  sme_c_1"
        runDb(sqlc1)

        sqlc2 = "drop table  sme_c_2"
        runDb(sqlc2)

        sqlc3 = "drop table  sme_c_3"
        runDb(sqlc3)

        sqlc4 = "drop table  sme_c_4"
        runDb(sqlc4)

        sqlc5 = "drop table  sme_c_5"
        runDb(sqlc5)

        sqlc6 = "drop table  sme_c_6"
        runDb(sqlc6)

        sqlc7 = "drop table  sme_c_7"
        runDb(sqlc7)

        sqlcc1 = "create table  sme_c_1 as "\
        "select n.CUSTOMER_REF,n.PRODUCT_SEQ, sum(CHARGE_COST_MNY/1000) CHARGE_COST_MNY from sme_pack_change n,billproductcharge@DBLINK_GENEVA c " \
                 "where n.CUSTOMER_REF=c.CUSTOMER_REF " \
                 "and n.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                 "and (n.CUSTOMER_REF,n.PRODUCT_SEQ,CHARGE_SEQ) in ( " \
                 "select n.CUSTOMER_REF,n.PRODUCT_SEQ,max(CHARGE_SEQ) from sme_pack_change n,billproductcharge@DBLINK_GENEVA c " \
                 "where n.CUSTOMER_REF=c.CUSTOMER_REF " \
                 "and n.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                 "group by n.CUSTOMER_REF,n.PRODUCT_SEQ) " \
                 "group by n.CUSTOMER_REF,n.PRODUCT_SEQ"
        runDb(sqlcc1)

        sqlcc2 = "create table  sme_c_2 as " \
                 "select c.*, CHARGE_COST_MNY latest_month_rental  from sme_c_1 n,sme_pack_change c " \
                 "where n.CUSTOMER_REF(+)=c.CUSTOMER_REF " \
                 "and n.PRODUCT_SEQ(+)=c.PRODUCT_SEQ"
        runDb(sqlcc2)

        sqlcc3 = "create table  sme_c_3 as " \
                 "select h.* from sme_c_2 h,product@DBLINK_GENEVA t,PRODUCTHASPARENTPRODUCT@DBLINK_GENEVA p " \
                 "where h.PRODUCT_ID=t.PRODUCT_ID " \
                 "and p.PRODUCT_ID(+)=t.PRODUCT_ID"
        runDb(sqlcc3)

        sqlcc4 = "create table sme_c_4  as " \
                 "select distinct c.*,t.START_DAT START_DAT1 from tariffelement@DBLINK_GENEVA  t, sme_c_3 c " \
                 "where (t.CATALOGUE_CHANGE_ID=(select CATALOGUE_CHANGE_ID from cataloguechange@DBLINK_GENEVA where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3)) " \
                 "and t.product_id=c.product_id and t.TARIFF_ID=c.TARIFF_ID and t.end_dat is null"
        runDb(sqlcc4)

        sqlcc5 = "create table  sme_c_5 as " \
                 "select distinct c.*,t.RECURRING_NUMBER/1000 Rental,t.ONE_OFF_NUMBER/1000 ONE_OFF_NUMBER from tariffelementband@DBLINK_GENEVA  t, sme_c_4  c " \
                 "where (t.CATALOGUE_CHANGE_ID=(select CATALOGUE_CHANGE_ID from cataloguechange@DBLINK_GENEVA where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3)) " \
                 "and t.product_id=c.product_id and t.TARIFF_ID=c.TARIFF_ID and t.START_DAT=c.START_DAT1"
        runDb(sqlcc5)

        sqlcc6 = "create table sme_c_6  as " \
                 "select distinct CUSTOMER_REF,PRODUCT_SEQ,RECURRING_NUMBER/1000 Override_Rental,ONE_OFF_NUMBER/1000 Override_ONE_OFF_NUMBER from custoverrideprice@DBLINK_GENEVA c " \
                 "where c.END_DAT is null " \
                 "and (c.CUSTOMER_REF, c.PRODUCT_SEQ,c.START_DAT) in ( " \
                 "select c.CUSTOMER_REF,c.PRODUCT_SEQ,max(c.START_DAT)from custoverrideprice@DBLINK_GENEVA c,sme_c_5 cc " \
                 "where c.END_DAT is null " \
                 "and c.CUSTOMER_REF=cc.CUSTOMER_REF " \
                 "and c.PRODUCT_SEQ=cc.PRODUCT_SEQ " \
                 "group by c.CUSTOMER_REF,c.PRODUCT_SEQ)"
        runDb(sqlcc6)

        sqlcc7 = "create table sme_c_7 as " \
                 "select c.*, " \
                 "(select OVERRIDE_RENTAL from sme_c_6   cc where c.CUSTOMER_REF=cc.CUSTOMER_REF " \
                 "and c.PRODUCT_SEQ=cc.PRODUCT_SEQ)OVERRIDE_RENTAL, " \
                 "(select Override_ONE_OFF_NUMBER from sme_c_6   cc where c.CUSTOMER_REF=cc.CUSTOMER_REF " \
                 "and c.PRODUCT_SEQ=cc.PRODUCT_SEQ)Override_ONE_OFF_NUMBER " \
                 "from sme_c_5 c"
        runDb(sqlcc7)

        sqln914 = "drop table sme_n9_14"
        runDb(sqln914)

        sqlcn914= "create table sme_n9_14 as "\
                 "select *  from sme_n9_13 "\
                 "where product_id not in (1139,101)"
        runDb(sqlcn914)

        sqln9141 = "drop tABLE sme_n9_14_1"
        runDb(sqln9141)

        sqlcn9141 = "CREATE TABLE sme_n9_14_1 AS " \
                    "select distinct c.*,cpd.PRODUCT_LABEL, cpd.END_DAT ,NEXT_BILL_DTM " \
                    "from sme_n9_14  c,custproductdetails@DBLINK_GENEVA cpd,account@DBLINK_GENEVA aa " \
                    "where c.CUSTOMER_REF=cpd.CUSTOMER_REF " \
                    "and c.PRODUCT_SEQ=cpd.PRODUCT_SEQ " \
                    "and cpd.ACCOUNT_NUM=aa.ACCOUNT_NUM " \
                    "and (cpd.START_DAT) in ( " \
                    "select  max(START_DAT)max_START_DAT " \
                    "from custproductdetails@DBLINK_GENEVA cpd " \
                    "where cpd.CUSTOMER_REF=c.CUSTOMER_REF " \
                    "and cpd.PRODUCT_SEQ=c.PRODUCT_SEQ)"
        runDb(sqlcn9141)

        sqln915 = "drop table sme_n9_15"
        runDb(sqln915)

        sqlcn915 = "create table  sme_n9_15 as " \
                   "select  distinct n.*, START_DAT,c.TARIFF_ID,t.TARIFF_NAME " \
                   "from custproducttariffdetails@DBLINK_GENEVA c, sme_n9_14_1 n,tariff@DBLINK_GENEVA t " \
                   "where n.CUSTOMER_REF=c.CUSTOMER_REF " \
                   "and n.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                   "and c.TARIFF_ID=t.TARIFF_ID " \
                   "and (CATALOGUE_CHANGE_ID=(select CATALOGUE_CHANGE_ID from cataloguechange@DBLINK_GENEVA where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3)) " \
                   "and (n.CUSTOMER_REF,n.PRODUCT_SEQ, START_DAT)in ( " \
                   "select  distinct n.CUSTOMER_REF,n.PRODUCT_SEQ, max(START_DAT) " \
                   "from custproducttariffdetails@DBLINK_GENEVA c, sme_n9_14_1 n " \
                   "where n.CUSTOMER_REF=c.CUSTOMER_REF " \
                   "and n.PRODUCT_SEQ=c.PRODUCT_SEQ " \
                   "group by  n.CUSTOMER_REF,n.PRODUCT_SEQ) "
        runDb(sqlcn915)

        sqln916 = "drop table sme_n9_16"
        runDb(sqln916)

        sqlcn916 = "create table sme_n9_16  as " \
                   "select distinct c.*,t.START_DAT START_DAT1 from tariffelement@DBLINK_GENEVA  t, sme_n9_15 c " \
                   "where t.CATALOGUE_CHANGE_ID=(select CATALOGUE_CHANGE_ID from cataloguechange@DBLINK_GENEVA where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3) " \
                   "and t.product_id=c.product_id and t.TARIFF_ID=c.TARIFF_ID and t.end_dat is null"
        runDb(sqlcn916)

        sqln917 = "drop table sme_n9_17"
        runDb(sqln917)

        sqlcn917 = "create table  sme_n9_17 as " \
                   "select distinct c.*,t.RECURRING_NUMBER/1000 Rental,t.ONE_OFF_NUMBER/1000 ONE_OFF_NUMBER from tariffelementband@DBLINK_GENEVA  t, sme_n9_16  c " \
                   "where (t.CATALOGUE_CHANGE_ID=(select CATALOGUE_CHANGE_ID from cataloguechange@DBLINK_GENEVA where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3)) " \
                   "and t.product_id=c.product_id and t.TARIFF_ID=c.TARIFF_ID and t.START_DAT=c.START_DAT1"
        runDb(sqlcn917)

        sqln918 = "drop table sme_n9_18"
        runDb(sqln918)

        sqlcn918 = "creATE TABLE sme_n9_18 AS " \
                   "select h.* ,m.connection_medium " \
                   "from sme_n9_17 h " \
                   "left join  edw_tgt.DIM_CUSTPRODUCT_TAB@SLTDWH_OSS1 m " \
                   "on h.customer_ref=m.customer_ref and h.product_seq=m.product_seq and m.EXPIRATION_DATE is null"
        runDb(sqlcn918)

        sqlup1 = "alter table sme_c_7 add(Product_NAME varchar(50))"
        runDb(sqlup1)

        sqlup2 ="update sme_c_7 t1 set t1.Product_NAME = " \
                "(select am.product_name from product@DBLINK_GENEVA am where t1.product_id = am.product_id)"
        runDb(sqlup2)

        sqlup3 ="alter table sme_c_7 add(Product1 varchar(50))"
        runDb(sqlup3)

        sqlup4 = "update sme_c_7 t1 set t1.Product1 = " \
                 "(select am.product from repo.product_mapping@DBLINK_GENEVA am where t1.product_id = am.product_id)"
        runDb(sqlup4)

        sqlup5 ="alter table sme_c_7 add(Service_new1 varchar(50))"
        runDb(sqlup5)

        sqlup6 = "update sme_c_7 t1 set t1.Service_new1 = " \
                 "(select distinct am.Service_new from repo.product_mapping@DBLINK_GENEVA  am where t1.product1 = am.product)"
        runDb(sqlup6)

        sqlup7 = "alter table sme_c_7 add(PCategory1 varchar(20))"
        runDb(sqlup7)

        sqlup8 = "update sme_c_7 t1 set t1.PCategory1 = " \
                 "(select distinct  am.PCategory from repo.product_mapping@DBLINK_GENEVA  am where t1.product1 = am.product)"
        runDb(sqlup8)

        sqlup9= "alter table sme_c_7 add( PSM varchar(20))"
        runDb(sqlup9)

        sqlup10= "update sme_c_7 t1 set t1.PSM = " \
                 "(select am.PSM from repo.PSM_AM_Jun2019@DBLINK_GENEVA am where t1.account_manager = am.SME_AM_Code)"
        runDb(sqlup10)

        sqlup11= "alter table sme_c_7 add(AM_NAME varchar(50))"
        runDb(sqlup11)

        sqlup12= "update sme_c_7 t1 set t1.AM_NAME = " \
                 "(select am.NEW_NAME AM_NAME from repo.PSM_AM_Jun2019@DBLINK_GENEVA am where t1.account_manager = am.SME_AM_Code)"
        runDb(sqlup12)

        sqlc71 = "drop table sme_c_71"
        runDb(sqlc71)

        sqlc71 = "create table sme_c_71  as " \
                 "select distinct c.*,t.START_DAT START_DAT2 from tariffelement@DBLINK_GENEVA  t, sme_c_7 c " \
                 "where (t.CATALOGUE_CHANGE_ID=(select CATALOGUE_CHANGE_ID from cataloguechange@DBLINK_GENEVA where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3)) " \
                 "and t.product_id=C.product_Id and t.TARIFF_ID=c.PREVIOUS_TARIFF_ID --and t.end_dat is null"
        runDb(sqlc71)

        sqlc72 = "drop table sme_c_72"
        runDb(sqlc72)

        sqlcc72 = "create table  sme_c_72 as " \
                  "select distinct c.*,t.RECURRING_NUMBER/1000 Previous_Rental from tariffelementband@DBLINK_GENEVA  t, sme_c_71  c " \
                  "where (t.CATALOGUE_CHANGE_ID=(select CATALOGUE_CHANGE_ID from cataloguechange@DBLINK_GENEVA where CURRENCY_CODE ='LKR' and CATALOGUE_STATUS=3)) " \
                  "and t.product_id=c.product_Id and t.TARIFF_ID=c.PREVIOUS_TARIFF_ID and t.START_DAT=c.START_DAT2"
        runDb(sqlcc72)

        sqlc73 = "drop table sme_c_73"
        runDb(sqlc73)

        sqlcc73 = "create table sme_c_73 as " \
                  "select CUSTOMER_REF ,   PRODUCT_SEQ ,   ACCOUNT_NUM ,   PRODUCT_ID ,   P_EFFECTIVE_DTM ,   PRODUCT_STATUS  ,  PRODUCT_LABEL ,   BILLING_CENTRE, " \
                  "CUSTOMER_SEGMENT   , ACCOUNT_MANAGER  , T_START_DAT ,   TARIFF_ID ,   TARIFF_NAME   , PREVIOUS_TARIFF_ID   , PREVIOUS_PRODUCT ,   END_DAT  , " \
                  "LATEST_MONTH_RENTAL  ,  START_DAT1   , RENTAL  ,  ONE_OFF_NUMBER   ,OVERRIDE_RENTAL  ,  OVERRIDE_ONE_OFF_NUMBER  ,  PSM    ,AM_NAME    ,PRODUCT_NAME, " \
                  "PRODUCT1   , SERVICE_NEW1,    PCATEGORY1,    START_DAT2  ,  PREVIOUS_RENTAL " \
                  "from sme_c_72"
        runDb(sqlcc73)

        sqlc701 = "drop table sme_c_7_1"
        runDb(sqlc701)

        sqlcc701 = "create table sme_c_7_1 as " \
                   "select c.customer_ref,c.product_seq,account_num,product_label,PREVIOUS_TARIFF_ID,max(start_dat) previous_tariff_start_date " \
                   "from sme_c_73 c,custproducttariffdetails@DBLINK_GENEVA b " \
                   "where c.customer_ref=b.customer_ref " \
                   "and c.product_seq=b.product_seq " \
                   "and c.PREVIOUS_TARIFF_ID=b.tariff_id " \
                   "and b.end_dat is not null " \
                   "and C.END_DAT> b.start_dat " \
                   "group by c.customer_ref,c.product_seq,account_num,product_label,PREVIOUS_TARIFF_Id"
        runDb(sqlcc701)

        sqlh191="drop table h1_91"
        runDb(sqlh191)

        sqlch191="create table h1_91 as select * from h1_9 " \
                 "where STATUS_REASON_TXT != 'CAB Migration CR298' or STATUS_REASON_TXT is null"
        runDb(sqlch191)

        sqlu20="alter table h1_91 add(PSM varchar(20))"
        runDb(sqlu20)

        sqlu21="update h1_91 t1 set t1.PSM = " \
               "(select am.PSM from repo.PSM_AM_Jun2019@DBLINK_GENEVA am where t1.account_manager = am.SME_AM_Code)"
        runDb(sqlu21)

        sqlu22="alter table h1_91 add(AM_NAME varchar(50))"
        runDb(sqlu22)

        sqlu23="update h1_91 t1 set t1.AM_NAME = " \
               "(select am.NEW_NAME AM_NAME from repo.PSM_AM_Jun2019@DBLINK_GENEVA am where t1.account_manager = am.SME_AM_Code)"
        runDb(sqlu23)

        sqlu24="alter table h1_91 add( product1 varchar(50))"
        runDb(sqlu24)

        sqlu25="update h1_91 t1 set t1.product1 = " \
               "(select distinct am.product from repo.product_mapping@DBLINK_GENEVA am where t1.product_id=am.product_id)"
        runDb(sqlu25)

        sqlu26="alter table h1_91 add(Service_new1 varchar(50))"
        runDb(sqlu26)

        sqlu27="update h1_91 t1 set t1.Service_new1 = " \
               "(select distinct am.Service_new from repo.product_mapping@DBLINK_GENEVA  am where t1.product1 = am.product " \
               "and t1.product_id=am.product_id)"
        runDb(sqlu27)

        sqlu28="alter table h1_91 add( PCategory1 varchar(20))"
        runDb(sqlu28)

        sqlu29="update h1_91 t1 set t1.PCategory1 = " \
               "(select distinct  am.PCategory from repo.product_mapping@DBLINK_GENEVA  am where t1.product1 = am.product)"
        runDb(sqlu29)

        sqlu30="alter table h1_91 add customer_type_id number(10)"
        runDb(sqlu30)

        sqlu31="create index h1 on h1_91(customer_ref)"
        runDb(sqlu31)

        sqlu32="update h1_91 t set t.customer_type_id = " \
               "(select c.CUSTOMER_TYPE_ID from customer@DBLINK_GENEVA c where t.customer_ref=c.customer_ref)"
        runDb(sqlu32)

        sqlu33="alter table h1_91 add customer_type varchar(50)"
        runDb(sqlu33)

        sqlu34="create index h2 on h1_91(CUSTOMER_TYPE_ID)"
        runDb(sqlu34)

        sqlu35="update h1_91 t set t.customer_type = " \
               "(select c.CUSTOMER_TYPE_NAME from customertype@DBLINK_GENEVA c where t.CUSTOMER_TYPE_ID=c.CUSTOMER_TYPE_ID)"
        runDb(sqlu35)

        sqlh192 = "drop table h1_92"
        runDb(sqlh192)

        sqlch192="create TABLE H1_92 AS select h. *, m.connection_medium from h1_91 h " \
                 "left join edw_tgt.DIM_CUSTPRODUCT_TAB@SLTDWH_OSS1 m on " \
                 "h.customer_ref = m.customer_ref and h.product_seq = m.product_seq and m.EXPIRATION_DATE is null"
        runDb(sqlch192)

        sqlactive="create table data_active as " \
                  "select distinct p.*,c.EFFECTIVE_DTM latest_EFFECTIVE_DTM ,C.PRODUCT_STATUS latest_PRODUCT_STATUS " \
                  "from custproductstatus@DBLINK_GENEVA c, H1_92  p " \
                  "where c.CUSTOMER_REF=p.CUSTOMER_REF " \
                  "and c.PRODUCT_SEQ=p.PRODUCT_SEQ " \
                  "and  c.PRODUCT_STATUS='OK' " \
                  "and (c.CUSTOMER_REF,c.PRODUCT_SEQ,c.EFFECTIVE_DTM) in ( " \
                  "select c.CUSTOMER_REF,c.PRODUCT_SEQ,max(c.EFFECTIVE_DTM) " \
                  "from custproductstatus@DBLINK_GENEVA c, H1_92  p " \
                  "where c.CUSTOMER_REF=p.CUSTOMER_REF " \
                  "and c.PRODUCT_SEQ=p.PRODUCT_SEQ " \
                  "and trunc(c.EFFECTIVE_DTM)<=\'"+str(lastmonth) +"\' " \
                  "group by c.CUSTOMER_REF,c.PRODUCT_SEQ)"
        runDb(sqlactive)

        sqlpkg="create table pkg_chg as " \
                "select distinct c.*,previous_tariff_start_date  " \
                "from sme_c_73 c  " \
                "left join sme_c_7_1 a  " \
                "on c.customer_ref=a.customer_ref  " \
                "and C.PRODUCT_SEQ=a.product_seq " \
                "where C.PCATEGORY1 = 'DATA'  " \
                "and SERVICE_NEW1 <> 'SME Solution'  " \
                "AND ACCOUNT_MANAGER IN (SELECT DISTINCT AM_CODE FROM AREA_MAP_AM) " \
                "AND NVL(RENTAL,0) + NVL(ONE_OFF_NUMBER,0) + NVL(OVERRIDE_RENTAL,0) +NVL(OVERRIDE_ONE_OFF_NUMBER,0) > 0"
        runDb(sqlpkg)

        sqlpkgactive="create table pkg_chg_active as " \
        "select distinct p.*,c.EFFECTIVE_DTM latest_EFFECTIVE_DTM ,C.PRODUCT_STATUS latest_PRODUCT_STATUS " \
        "from custproductstatus@DBLINK_GENEVA c, pkg_chg  p " \
        "where c.CUSTOMER_REF=p.CUSTOMER_REF " \
        "and c.PRODUCT_SEQ=p.PRODUCT_SEQ " \
        "and  c.PRODUCT_STATUS='OK' " \
        "and (c.CUSTOMER_REF,c.PRODUCT_SEQ,c.EFFECTIVE_DTM) in ( " \
        "select c.CUSTOMER_REF,c.PRODUCT_SEQ,max(c.EFFECTIVE_DTM) " \
        "from custproductstatus@DBLINK_GENEVA c, pkg_chg  p " \
        "where c.CUSTOMER_REF=p.CUSTOMER_REF " \
        "and c.PRODUCT_SEQ=p.PRODUCT_SEQ " \
        "and trunc(c.EFFECTIVE_DTM)<=\'"+str(lastmonth) +"\' " \
        "group by c.CUSTOMER_REF,c.PRODUCT_SEQ)"
        runDb(sqlpkgactive)

        sqlpkg = "create table MSME_DATA_PKGCHG_"+cmonth+" as " \
                 "select distinct * " \
                 "from pkg_chg_active c "
        runDb(sqlpkg)

        sqlnew = "create table MSME_DATA_NEWCON_"+cmonth+" as " \
                 "SELECT DISTINCT * FROM data_active " \
                 "WHERE PCATEGORY1 = 'DATA' " \
                 "AND SERVICE_NEW1 <> 'SME Solution' " \
                 "AND ACCOUNT_MANAGER IN (SELECT DISTINCT AM_CODE FROM AREA_MAP_AM) " \
                 "AND NVL(RENTAL,0) + NVL(ONE_OFF_NUMBER,0) + NVL(OVERRIDE_RENTAL,0) +NVL(OVERRIDE_ONE_OFF_NUMBER,0) > 0"
        runDb(sqlnew)

        sqlch193="create TABLE MSME_DATA_NEWCON2_"+cmonth+" as "\
                 "select * from MSME_DATA_NEWCON_"+cmonth+" where ACCOUNT_MANAGER = ''"
        runDb(sqlch193)

        sqlch194="create TABLE MSME_DATA_PKGCHG2_"+cmonth+" as " \
                 "select * from MSME_DATA_PKGCHG_"+cmonth+" where ACCOUNT_MANAGER = ''"
        runDb(sqlch194)


        try:
            conn = db.DbConnection.dbconnOssMSME(self="")
            with conn.cursor() as cursor:
                sql = "select * from MSME_DATA_NEWCON_"+cmonth+""
                cursor.execute(sql)

                for row in cursor:

                    if row[17] is not None:
                         if row[19] == 0:
                            pass
                         else:
                             print("Rental",row[17],row[18],row[19],row[20],)
                             with conn.cursor() as cursor:
                                 sqlnc="INSERT INTO MSME_DATA_NEWCON2_"+cmonth+" VALUES (:ACCOUNT_MANAGER, :CUSTOMER_REF," \
                                       " :PRODUCT_SEQ,:PRODUCT_STATUS, :PRODUCT_START_DATE, :ACCOUNT_NUM, :PRODUCT_LABEL," \
                                       " :PRODUCT_ID, :PRODUCT_NAME, :ACCOUNT_STARTDATE, :ACCOUNT_STATUS, " \
                                       ":STATUS_REASON_TXT, :START_DAT, :TARIFF_ID, :TARIFF_NAME, :CHARGE_COST_MNY," \
                                       " :START_DAT1, :RENTAL, :ONE_OFF_NUMBER, :OVERRIDE_RENTAL, :OVERRIDE_ONE_OFF_NUMBER," \
                                       " :PSM, :AM_NAME, :PRODUCT1, :SERVICE_NEW1, :PCATEGORY1, :CUSTOMER_TYPE_ID," \
                                       " :CUSTOMER_TYPE, :CONNECTION_MEDIUM, :LATESTDTM ,:LATESTSTAT)"
                                 cursor.execute(sqlnc, [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],
                                                        row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],
                                                        row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],
                                                        row[28],row[29],row[30]])
                                 conn.commit()
                                 print(cursor.rowcount)


                    elif row[18] is not None:
                         if row[20] == 0:
                             pass
                         else:
                            print("onnoff",row[17],row[18],row[19],row[20],)
                            with conn.cursor() as cursor:
                                sqlnc="INSERT INTO MSME_DATA_NEWCON2_"+cmonth+" VALUES (:ACCOUNT_MANAGER, :CUSTOMER_REF," \
                                      " :PRODUCT_SEQ,:PRODUCT_STATUS, :PRODUCT_START_DATE, :ACCOUNT_NUM, :PRODUCT_LABEL," \
                                      " :PRODUCT_ID, :PRODUCT_NAME, :ACCOUNT_STARTDATE, :ACCOUNT_STATUS, " \
                                      ":STATUS_REASON_TXT, :START_DAT, :TARIFF_ID, :TARIFF_NAME, :CHARGE_COST_MNY," \
                                      " :START_DAT1, :RENTAL, :ONE_OFF_NUMBER, :OVERRIDE_RENTAL, :OVERRIDE_ONE_OFF_NUMBER," \
                                      " :PSM, :AM_NAME, :PRODUCT1, :SERVICE_NEW1, :PCATEGORY1, :CUSTOMER_TYPE_ID," \
                                      " :CUSTOMER_TYPE, :CONNECTION_MEDIUM, :LATESTDTM ,:LATESTSTAT)"
                                cursor.execute(sqlnc, [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],
                                                       row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],
                                                       row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],
                                                       row[28],row[29],row[30]])
                                conn.commit()
                                print(cursor.rowcount)




                    else:
                        if row[19] != '0':
                            print("Override Rental",row[17],row[18],row[19],row[20],)

        except conn.Error as error:
            print('Error occurred:' + str(error))


        try:
            conn = db.DbConnection.dbconnOssMSME(self="")
            with conn.cursor() as cursor:
                sql = "select * from MSME_DATA_PKGCHG_"+cmonth+""
                cursor.execute(sql)

                for row in cursor:

                    if row[18] is not None:
                        if row[20] == 0:
                            pass
                        else:
                            if row[20] is not None:
                                pkgval =row[20] - row[29]
                                if pkgval > 0:
                                    print("Rental over",row[18],row[19],row[20],row[21],)
                                    with conn.cursor() as cursor:
                                        sqlnc="INSERT INTO MSME_DATA_PKGCHG2_"+cmonth+" VALUES (:CUSTOMER_REF, :PRODUCT_SEQ, :ACCOUNT_NUM, " \
                                              " :PRODUCT_ID, :P_EFFECTIVE_DTM, :PRODUCT_STATUS, :PRODUCT_LABEL, :BILLING_CENTRE, :CUSTOMER_SEGMENT, " \
                                              " :ACCOUNT_MANAGER, :T_START_DAT, :TARIFF_ID, :TARIFF_NAME, :PREVIOUS_TARIFF_ID, :PREVIOUS_PRODUCT," \
                                              " :END_DAT, :LATEST_MONTH_RENTAL, :START_DAT1, :RENTAL, :ONE_OFF_NUMBER, :OVERRIDE_RENTAL," \
                                              " :OVERRIDE_ONE_OFF_NUMBER, :PSM, :AM_NAME, :PRODUCT_NAME, :PRODUCT1, :SERVICE_NEW1," \
                                              " :PCATEGORY1, :START_DAT2, :PREVIOUS_RENTAL, :PREVIOUS_TARIFF_START_DATE, :LATESTDTM ,:LATESTSTAT)"
                                        cursor.execute(sqlnc, [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],
                                                               row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],
                                                               row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],
                                                               row[28],row[29],row[30],row[31],row[32]])
                                        conn.commit()
                                        print(cursor.rowcount)

                            else:
                                pkgval =row[18] - row[29]

                                if pkgval > 0:
                                    print("Rental",row[18],row[19],row[20],row[21],)
                                    with conn.cursor() as cursor:
                                        sqlnc="INSERT INTO MSME_DATA_PKGCHG2_"+cmonth+" VALUES (:CUSTOMER_REF, :PRODUCT_SEQ, :ACCOUNT_NUM, " \
                                              " :PRODUCT_ID, :P_EFFECTIVE_DTM, :PRODUCT_STATUS, :PRODUCT_LABEL, :BILLING_CENTRE, :CUSTOMER_SEGMENT, " \
                                              " :ACCOUNT_MANAGER, :T_START_DAT, :TARIFF_ID, :TARIFF_NAME, :PREVIOUS_TARIFF_ID, :PREVIOUS_PRODUCT," \
                                              " :END_DAT, :LATEST_MONTH_RENTAL, :START_DAT1, :RENTAL, :ONE_OFF_NUMBER, :OVERRIDE_RENTAL," \
                                              " :OVERRIDE_ONE_OFF_NUMBER, :PSM, :AM_NAME, :PRODUCT_NAME, :PRODUCT1, :SERVICE_NEW1," \
                                              " :PCATEGORY1, :START_DAT2, :PREVIOUS_RENTAL, :PREVIOUS_TARIFF_START_DATE, :LATESTDTM ,:LATESTSTAT)"
                                        cursor.execute(sqlnc, [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],
                                                               row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],
                                                               row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],
                                                               row[28],row[29],row[30],row[31],row[32]])
                                        conn.commit()
                                        print(cursor.rowcount)


                    elif row[19] is not None:
                        if row[21] == 0:
                            pass
                        else:
                            print("onnoff",row[17],row[18],row[19],row[20],)

                    else:
                        if row[19] != '0':
                            print("Override Rental",row[17],row[18],row[19],row[20],)

        except conn.Error as error:
            print('Error occurred:' + str(error))

        try:
            conn = db.DbConnection.dbconnOssMSME(self="")
            with conn.cursor() as cursor:
                sqlInc = "UPDATE MSME_INCENT_STAT SET DATA_READY = :DATA_READY where YMONTH= :YMONTH"
                cursor.execute(sqlInc,['YES',cmonth])
                conn.commit()
        except conn.Error as error:
            print('Error occurred:' + str(error))
