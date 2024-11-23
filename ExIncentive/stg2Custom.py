from db import DbConnection
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

conn = DbConnection.dbconn(self="")
c = conn.cursor()
engine = DbConnection.dbengin()

sql = "SELECT TO_CHAR(ADD_MONTHS(TRUNC(SYSDATE,'mm'),-4),'YYYYMM') TBNAME FROM DUAL";  
c.execute(sql)
for TBNAME in c:
    TableName = str(TBNAME[0])


#GET ACTIVE DELER TABLE
sql = "SELECT TABLE_NAME  FROM EX_SETTING WHERE DISCRIPTION = 'DEALER' AND END_DATE IS NULL";  
c.execute(sql)
for TABLE_NAME in c:
    DealerTableName = str(TABLE_NAME[0]) 

#GET ACTIVE BB TABLE
sql = "SELECT TABLE_NAME  FROM EX_SETTING WHERE DISCRIPTION = 'COM_BB' AND END_DATE IS NULL";  
c.execute(sql)
for TABLE_NAME in c:
    BBTableName = str(TABLE_NAME[0]) 

#GET ACTIVE IPTV TABLE
sql = "SELECT TABLE_NAME  FROM EX_SETTING WHERE DISCRIPTION = 'COM_IPTV' AND END_DATE IS NULL";  
c.execute(sql)
for TABLE_NAME in c:
    IPTVTableName = str(TABLE_NAME[0]) 

#GET ACTIVE BEARER TABLE
sql = "SELECT TABLE_NAME  FROM EX_SETTING WHERE DISCRIPTION = 'COM_BEARER' AND END_DATE IS NULL";  
c.execute(sql)
for TABLE_NAME in c:
    BearerTableName = str(TABLE_NAME[0]) 

#GET ACTIVE SLAB TABLE
sql = "SELECT TABLE_NAME  FROM EX_SETTING WHERE DISCRIPTION = 'SALES_SLAB' AND END_DATE IS NULL";  
c.execute(sql)
for TABLE_NAME in c:
    SlabTableName = str(TABLE_NAME[0]) 

#ADDBSS STATUS TO SLAES COUNT TABLE
# sql = "ALTER TABLE SALES_"+TableName+" ADD BSSSTATUS VARCHAR(10)"
# c.execute(sql)


sql = "SELECT PRODUCT_ID,BSSDSP,ACCOUNT_NUM,EVENT_SOURCE,PRODUCT_LABEL,SUPPLIER_ORDER_NUM FROM SALES_"+TableName+"  WHERE BSSSTATUS IS NULL ";  
c.execute(sql)
for REC in c:
    Dealer = str(REC[0])
    x = conn.cursor()
    sql = "UPDATE SALES_"+TableName+" X SET X.BSSSTATUS = ( SELECT PRODUCT_STATUS  FROM ( "\
                        "SELECT DISTINCT  CPD.CUSTOMER_REF, CHP.PRODUCT_SEQ, AC.ACCOUNT_NUM, "\
                        "CHP.PARENT_PRODUCT_SEQ,CHP.PRODUCT_ID, CPS.EFFECTIVE_DTM, "\
                        "CPS.PRODUCT_STATUS, CPS.STATUS_REASON_TXT, AC.LAST_BILL_DTM , PRODUCT_LABEL "\
                        "FROM  CUSTPRODUCTSTATUS@DBLINK_GENEVA CPS, CUSTHASPRODUCT@DBLINK_GENEVA CHP, "\
                        "CUSTPRODUCTDETAILS@DBLINK_GENEVA CPD, PRODUCT@DBLINK_GENEVA PR, ACCOUNT@DBLINK_GENEVA AC "\
                        "WHERE CPS.CUSTOMER_REF = CPD.CUSTOMER_REF "\
                        "AND CPS.PRODUCT_SEQ = CPD.PRODUCT_SEQ "\
                        "AND CHP.CUSTOMER_REF = CPD.CUSTOMER_REF "\
                        "AND CHP.PRODUCT_SEQ = CPD.PRODUCT_SEQ "\
                        "AND AC.ACCOUNT_NUM = CPD.ACCOUNT_NUM "\
                        "AND CHP.PRODUCT_ID  = PR.PRODUCT_ID "\
                        "AND CHP.PRODUCT_ID = "+str(REC[0])+" "\
                        "AND CHP.PARENT_PRODUCT_SEQ IS NULL "\
                        "AND CPS.EFFECTIVE_DTM = (SELECT MAX(EFFECTIVE_DTM) FROM CUSTPRODUCTSTATUS@DBLINK_GENEVA CPQ "\
                                                  "WHERE CPS.CUSTOMER_REF = CPQ.CUSTOMER_REF "\
                                                   " AND CPS.PRODUCT_SEQ = CPQ.PRODUCT_SEQ "\
                                                   " AND EFFECTIVE_DTM < (TO_DATE('"+str(REC[1])+"', 'yyyy-mm-dd HH24:MI:SS')+60) ) "\
                        " AND AC.ACCOUNT_NUM  = '"+str(REC[2])+"' "\
                        "AND (PRODUCT_LABEL = '"+str(REC[3])+"' OR PRODUCT_LABEL = '"+str(REC[4])+"')  "\
                        "ORDER BY EFFECTIVE_DTM DESC) "\
                        "WHERE ROWNUM<2 ) WHERE SUPPLIER_ORDER_NUM = '"+str(REC[5])+"' "
    print (str(REC[1]))
    x.execute(sql)
    x.execute("commit")
    x.close();

print ("end loop")
# #CHECK FOR BB ACTIVE STATUS FOR LTE BEARER SUSPENDED CASES -> IF BB IS ACTIVE CALCULATE BEARER
# sql = "SELECT PRODUCT_ID,BSSDSP,ACCOUNT_NUM,EVENT_SOURCE,PRODUCT_LABEL,SUPPLIER_ORDER_NUM FROM SALES_"+TableName+" WHERE MEDIUM = 'LTE' AND BSSSTATUS = 'SU' AND COM_TYPE = 'LTE'";  
# c.execute(sql)
# for REC in c:
#     Dealer = str(REC[0])
#     x = conn.cursor()
#     sql = "UPDATE SALES_"+TableName+" X SET X.BSSSTATUS = ( SELECT PRODUCT_STATUS  FROM ( "\
#                         "SELECT DISTINCT  CPD.CUSTOMER_REF, CHP.PRODUCT_SEQ, AC.ACCOUNT_NUM, "\
#                         "CHP.PARENT_PRODUCT_SEQ,CHP.PRODUCT_ID, CPS.EFFECTIVE_DTM, "\
#                         "CPS.PRODUCT_STATUS, CPS.STATUS_REASON_TXT, AC.LAST_BILL_DTM , PRODUCT_LABEL "\
#                         "FROM  CUSTPRODUCTSTATUS@DBLINK_GENEVA CPS, CUSTHASPRODUCT@DBLINK_GENEVA CHP, "\
#                         "CUSTPRODUCTDETAILS@DBLINK_GENEVA CPD, PRODUCT@DBLINK_GENEVA PR, ACCOUNT@DBLINK_GENEVA AC "\
#                         "WHERE CPS.CUSTOMER_REF = CPD.CUSTOMER_REF "\
#                         "AND CPS.PRODUCT_SEQ = CPD.PRODUCT_SEQ "\
#                         "AND CHP.CUSTOMER_REF = CPD.CUSTOMER_REF "\
#                         "AND CHP.PRODUCT_SEQ = CPD.PRODUCT_SEQ "\
#                         "AND AC.ACCOUNT_NUM = CPD.ACCOUNT_NUM "\
#                         "AND CHP.PRODUCT_ID  = PR.PRODUCT_ID "\
#                         "AND CHP.PRODUCT_ID = 1524 "\
#                         "AND CHP.PARENT_PRODUCT_SEQ IS NULL "\
#                         "AND CPS.EFFECTIVE_DTM = (SELECT MAX(EFFECTIVE_DTM) FROM CUSTPRODUCTSTATUS@DBLINK_GENEVA CPQ "\
#                                                   "WHERE CPS.CUSTOMER_REF = CPQ.CUSTOMER_REF "\
#                                                    " AND CPS.PRODUCT_SEQ = CPQ.PRODUCT_SEQ "\
#                                                    " AND EFFECTIVE_DTM < (TO_DATE('"+str(REC[1])+"', 'yyyy-mm-dd HH24:MI:SS')+60) ) "\
#                         " AND AC.ACCOUNT_NUM  = '"+str(REC[2])+"' "\
#                         "AND (PRODUCT_LABEL = '"+str(REC[3])+"' OR PRODUCT_LABEL = '"+str(REC[4])+"')  "\
#                         "ORDER BY EFFECTIVE_DTM DESC) "\
#                         "WHERE ROWNUM<2 ) WHERE SUPPLIER_ORDER_NUM = '"+str(REC[5])+"' "
#     print (str(REC[1]))
#     x.execute(sql)
#     x.execute("commit")
#     x.close();
# print ("CHECK FOR BB ACTIVE STATUS FOR LTE BEARER SUSPENDED CASES -> IF BB IS ACTIVE CALCULATE BEARER")



# #CHECK FOR VOICE PAL ACTIVE STATUS FOR LTE BEARER SUSPENDED CASES -> IF VOICE PAL IS ACTIVE CALCULATE BEARER
# sql = "SELECT PRODUCT_ID,BSSDSP,ACCOUNT_NUM,EVENT_SOURCE,PRODUCT_LABEL,SUPPLIER_ORDER_NUM FROM SALES_"+TableName+" , SERVICES_ATTRIBUTES "
# " WHERE MEDIUM = 'LTE' AND BSSSTATUS = 'SU' AND COM_TYPE = 'LTE'"\
# " AND SATT_SERV_ID = SUPPLIER_ORDER_NUM"\
# " AND SATT_ATTRIBUTE_NAME = 'SA_PACKAGE_NAME'"\
# " AND UPPER(SATT_DEFAULTVALUE) LIKE 'VOICE PAL'";  
# c.execute(sql)
# for REC in c:
#     Dealer = str(REC[0])
#     x = conn.cursor()
#     sql = "UPDATE SALES_"+TableName+" X SET X.BSSSTATUS = ( SELECT PRODUCT_STATUS  FROM ( "\
#                         "SELECT DISTINCT  CPD.CUSTOMER_REF, CHP.PRODUCT_SEQ, AC.ACCOUNT_NUM, "\
#                         "CHP.PARENT_PRODUCT_SEQ,CHP.PRODUCT_ID, CPS.EFFECTIVE_DTM, "\
#                         "CPS.PRODUCT_STATUS, CPS.STATUS_REASON_TXT, AC.LAST_BILL_DTM , PRODUCT_LABEL "\
#                         "FROM  CUSTPRODUCTSTATUS@DBLINK_GENEVA CPS, CUSTHASPRODUCT@DBLINK_GENEVA CHP, "\
#                         "CUSTPRODUCTDETAILS@DBLINK_GENEVA CPD, PRODUCT@DBLINK_GENEVA PR, ACCOUNT@DBLINK_GENEVA AC "\
#                         "WHERE CPS.CUSTOMER_REF = CPD.CUSTOMER_REF "\
#                         "AND CPS.PRODUCT_SEQ = CPD.PRODUCT_SEQ "\
#                         "AND CHP.CUSTOMER_REF = CPD.CUSTOMER_REF "\
#                         "AND CHP.PRODUCT_SEQ = CPD.PRODUCT_SEQ "\
#                         "AND AC.ACCOUNT_NUM = CPD.ACCOUNT_NUM "\
#                         "AND CHP.PRODUCT_ID  = PR.PRODUCT_ID "\
#                         "AND CHP.PRODUCT_ID = 1529 "\
#                         "AND CHP.PARENT_PRODUCT_SEQ IS NULL "\
#                         "AND CPS.EFFECTIVE_DTM = (SELECT MAX(EFFECTIVE_DTM) FROM CUSTPRODUCTSTATUS@DBLINK_GENEVA CPQ "\
#                                                   "WHERE CPS.CUSTOMER_REF = CPQ.CUSTOMER_REF "\
#                                                    " AND CPS.PRODUCT_SEQ = CPQ.PRODUCT_SEQ "\
#                                                    " AND EFFECTIVE_DTM < (TO_DATE('"+str(REC[1])+"', 'yyyy-mm-dd HH24:MI:SS')+60) ) "\
#                         " AND AC.ACCOUNT_NUM  = '"+str(REC[2])+"' "\
#                         "AND (PRODUCT_LABEL = '"+str(REC[3])+"' OR PRODUCT_LABEL = '"+str(REC[4])+"')  "\
#                         "ORDER BY EFFECTIVE_DTM DESC) "\
#                         "WHERE ROWNUM<2 ) WHERE SUPPLIER_ORDER_NUM = '"+str(REC[5])+"' "
#     print (str(REC[1]))
#     x.execute(sql)
#     x.execute("commit")
#     x.close();




# # #ADD STG2COUNT
# sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD SALES_COUNT_STG2 NUMBER"
# c.execute(sql)
# c.execute("commit")

# #ADD STG2COUNT
sql = "UPDATE SALES_COUNT_"+TableName+" SET SALES_COUNT_STG2 = 0"
c.execute(sql)
c.execute("commit")

#ADD STG2COUNT
sql = "UPDATE  SALES_COUNT_"+TableName+"  A SET SALES_COUNT_STG2 = (SELECT  COUNT (*) SALES_COUNT "\
"FROM  SALES_"+TableName+" "\
"WHERE  COM_TYPE IN ('MEGALINE' , 'LTE' , 'FTTH')  AND BSSSTATUS = 'OK' AND SALES_PERSON11 = SUB_DEALER  )"\
"WHERE SALES_COUNT_STG2 =0"
c.execute(sql)
c.execute("commit")

#ADD STG2COUNT
sql = "UPDATE  SALES_COUNT_"+TableName+"  A SET SALES_COUNT_STG2 = (SELECT  COUNT (*) SALES_COUNT "\
"FROM  SALES_"+TableName+" "\
"WHERE  COM_TYPE IN ('MEGALINE' , 'LTE' , 'FTTH')  AND BSSSTATUS = 'OK' AND  SALES_CHANNEL1 = SUB_DEALER) "\
"WHERE SALES_COUNT_STG2 =0"
c.execute(sql)
c.execute("commit")

# # #ADD SLAB
# sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD SLAB_STG2 varchar(2)"
# c.execute(sql)
# c.execute("commit")

# #UPDATE SLAB
sql = "UPDATE SALES_COUNT_"+TableName+" SET SLAB_STG2 = (SELECT SLAB FROM  "+SlabTableName+" WHERE SALES_COUNT_STG2  BETWEEN MIN_SALES AND MAX_SALES)"
c.execute(sql)
c.execute("commit")


# #UPDATE SLAB FOR Freelancers SLAB IS B AND ALL AMMOUNT SHOULD BE 65% OF SLAB B VALUE
sql = "UPDATE SALES_COUNT_"+TableName+" SET SLAB_STG2 = 'B' WHERE DEALER_NAME = 'Freelancers'"
c.execute(sql)
c.execute("commit")

# # #ADD COM_STG2
# sql = "ALTER TABLE SALES_"+TableName+" ADD COM_STG2 NUMBER"
# c.execute(sql)
# c.execute("commit")

#ADD COM_STG2
sql = "UPDATE SALES_"+TableName+" SET COM_STG2 = (SELECT DISTINCT COMMISSION FROM "+BBTableName+" "\
" WHERE UPPER(PACKAGE) = UPPER(REPLACE(BB_PACKAGE_NAME,'LTE_','') ) "\
" AND SLAB = (SELECT SLAB_STG2 FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = SALES_CHANNEL1 OR SUB_DEALER = SALES_PERSON11 ) ) "\
" WHERE COM_TYPE = 'BB' AND BSSSTATUS = 'OK'"
c.execute(sql)
c.execute("commit")


#ADD COM_STG2 - FREELANCER 
sql = "UPDATE SALES_"+TableName+" SET COM_STG2 = (SELECT DISTINCT COMMISSION FROM "+BBTableName+" "\
" WHERE UPPER(PACKAGE) = UPPER(REPLACE(BB_PACKAGE_NAME,'LTE_','') ) "\
" AND SLAB = (SELECT SLAB_STG2 FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = SALES_CHANNEL1 OR SUB_DEALER = SALES_PERSON11 ) ) * 0.65 "\
" WHERE COM_TYPE = 'BB' AND BSSSTATUS = 'OK' AND SALES_CHANNEL1 = 'Freelancers'"
c.execute(sql)
c.execute("commit")

#ADD COM_STG2
sql = "UPDATE SALES_"+TableName+" SET COM_STG2 = (SELECT DISTINCT COMMISSION FROM "+IPTVTableName+" WHERE UPPER(PACKAGE) = UPPER(REPLACE(BB_PACKAGE_NAME,' Rental','')) "\
" AND SLAB = (SELECT SLAB_STG2 FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = SALES_CHANNEL1 OR SUB_DEALER = SALES_PERSON11 ) ) "\
" WHERE COM_TYPE = 'IPTV' AND BSSSTATUS = 'OK'"
c.execute(sql)
c.execute("commit")

#ADD COM_STG2 - FREELANCER 
sql = "UPDATE SALES_"+TableName+" SET COM_STG2 = (SELECT DISTINCT COMMISSION FROM "+IPTVTableName+" WHERE UPPER(PACKAGE) = UPPER(REPLACE(BB_PACKAGE_NAME,' Rental','')) "\
" AND SLAB = (SELECT SLAB_STG2 FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = SALES_CHANNEL1 OR SUB_DEALER = SALES_PERSON11 ) ) * 0.65 "\
" WHERE COM_TYPE = 'IPTV' AND BSSSTATUS = 'OK' AND SALES_CHANNEL1 = 'Freelancers'"
c.execute(sql)
c.execute("commit")

#ADD COM_STG2
sql = "UPDATE SALES_"+TableName+" SET COM_STG2 = (SELECT DISTINCT COMMISSION FROM "+BearerTableName+" WHERE PRODUCT = 'FTTH New' "\
" AND SLAB = (SELECT SLAB_STG2 FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = SALES_CHANNEL1 OR SUB_DEALER = SALES_PERSON11 ) ) "\
" WHERE COM_TYPE = 'FTTH' AND SERO_ORDT_TYPE = 'CREATE'  AND BSSSTATUS = 'OK'"
c.execute(sql)
c.execute("commit")

#ADD COM_STG2 - FREELANCER 
sql = "UPDATE SALES_"+TableName+" SET COM_STG2 = (SELECT DISTINCT COMMISSION FROM "+BearerTableName+" WHERE PRODUCT = 'FTTH New' "\
" AND SLAB = (SELECT SLAB_STG2 FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = SALES_CHANNEL1 OR SUB_DEALER = SALES_PERSON11 ) ) * 0.65 "\
" WHERE COM_TYPE = 'FTTH' AND SERO_ORDT_TYPE = 'CREATE'  AND BSSSTATUS = 'OK' AND SALES_CHANNEL1 = 'Freelancers'"
c.execute(sql)
c.execute("commit")

#ADD COM_STG2
sql = "UPDATE SALES_"+TableName+" SET COM_STG2 = (SELECT DISTINCT COMMISSION FROM "+BearerTableName+" WHERE PRODUCT = 'FTTH Migration' "\
" AND SLAB = (SELECT SLAB_STG2 FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = SALES_CHANNEL1 OR SUB_DEALER = SALES_PERSON11 ) ) "\
" WHERE COM_TYPE = 'FTTH' AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO'  AND BSSSTATUS = 'OK'"
c.execute(sql)
c.execute("commit")

#ADD COM_STG2 - FREELANCER 
sql = "UPDATE SALES_"+TableName+" SET COM_STG2 = (SELECT DISTINCT COMMISSION FROM "+BearerTableName+" WHERE PRODUCT = 'FTTH Migration' "\
" AND SLAB = (SELECT SLAB_STG2 FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = SALES_CHANNEL1 OR SUB_DEALER = SALES_PERSON11 ) ) * 0.65 "\
" WHERE COM_TYPE = 'FTTH' AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO'  AND BSSSTATUS = 'OK' AND SALES_CHANNEL1 = 'Freelancers'"
c.execute(sql)
c.execute("commit")

#ADD COM_STG2
sql = "UPDATE SALES_"+TableName+" SET COM_STG2 = (SELECT DISTINCT COMMISSION FROM "+BearerTableName+" WHERE PRODUCT = 'Megaline'  "\
" AND SLAB = (SELECT SLAB_STG2 FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = SALES_CHANNEL1 OR SUB_DEALER = SALES_PERSON11 ) ) "\
" WHERE COM_TYPE = 'MEGALINE' AND BSSSTATUS = 'OK'" 
c.execute(sql)
c.execute("commit")

#ADD COM_STG2 - FREELANCER 
sql = "UPDATE SALES_"+TableName+" SET COM_STG2 = (SELECT DISTINCT COMMISSION FROM "+BearerTableName+" WHERE PRODUCT = 'Megaline'  "\
" AND SLAB = (SELECT SLAB_STG2 FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = SALES_CHANNEL1 OR SUB_DEALER = SALES_PERSON11 ) ) * 0.65 "\
" WHERE COM_TYPE = 'MEGALINE' AND BSSSTATUS = 'OK' AND SALES_CHANNEL1 = 'Freelancers'" 
c.execute(sql)
c.execute("commit")

#ADD COM_STG2
sql = "UPDATE SALES_"+TableName+" SET COM_STG2 = (SELECT DISTINCT COMMISSION FROM "+BearerTableName+" WHERE PRODUCT = 'LTE'  "\
" AND SLAB = (SELECT SLAB_STG2 FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = SALES_CHANNEL1 OR SUB_DEALER = SALES_PERSON11 ) ) "\
" WHERE COM_TYPE = 'LTE' AND BSSSTATUS = 'OK'" 
c.execute(sql)
c.execute("commit")

#ADD COM_STG2 - FREELANCER
sql = "UPDATE SALES_"+TableName+" SET COM_STG2 = (SELECT DISTINCT COMMISSION FROM "+BearerTableName+" WHERE PRODUCT = 'LTE'  "\
" AND SLAB = (SELECT SLAB_STG2 FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = SALES_CHANNEL1 OR SUB_DEALER = SALES_PERSON11 ) )  * 0.65"\
" WHERE COM_TYPE = 'LTE' AND BSSSTATUS = 'OK' AND SALES_CHANNEL1 = 'Freelancers'" 
c.execute(sql)
c.execute("commit")

#ADD COM_STG2
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD FTTH_STG2 VARCHAR2(20)"
c.execute(sql)
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD BB_STG2 VARCHAR2(20)"
c.execute(sql)
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD MEGALINE_STG2 VARCHAR2(20)"
c.execute(sql)
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD LTE_STG2 VARCHAR2(20)"
c.execute(sql)
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD IPTV_STG2 VARCHAR2(20)"
c.execute(sql)
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD TOT_STG2 VARCHAR2(20)"
c.execute(sql)
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD PAYMRNT_STG2 VARCHAR2(20)"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1
sql = "UPDATE SALES_COUNT_"+TableName+" SET  FTTH_STG2 = (SELECT  SUM(COM_STG2) FROM SALES_"+TableName+" WHERE COM_TYPE = 'FTTH' AND ((DEALER_NAME = SALES_CHANNEL1 AND SUB_DEALER =  SALES_PERSON11 )) )"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  LTE_STG2 = (SELECT  SUM(COM_STG2) FROM SALES_"+TableName+" WHERE COM_TYPE = 'LTE' AND ((DEALER_NAME = SALES_CHANNEL1 AND SUB_DEALER =  SALES_PERSON11 )) )"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  MEGALINE_STG2 = (SELECT  SUM(COM_STG2) FROM SALES_"+TableName+" WHERE COM_TYPE = 'MEGALINE' AND ((DEALER_NAME = SALES_CHANNEL1 AND SUB_DEALER =  SALES_PERSON11 )) )"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  BB_STG2 = (SELECT  SUM(COM_STG2) FROM SALES_"+TableName+" WHERE COM_TYPE = 'BB' AND ((DEALER_NAME = SALES_CHANNEL1 AND SUB_DEALER =  SALES_PERSON11 )) )"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  IPTV_STG2 = (SELECT  SUM(COM_STG2) FROM SALES_"+TableName+" WHERE COM_TYPE = 'IPTV' AND ((DEALER_NAME = SALES_CHANNEL1 AND SUB_DEALER =  SALES_PERSON11 )) )"
c.execute(sql)
c.execute("commit")
sql = "UPDATE SALES_COUNT_"+TableName+" SET  TOT_STG2 = (SELECT  SUM(COM_STG2) FROM SALES_"+TableName+" WHERE ((DEALER_NAME = SALES_CHANNEL1 AND SUB_DEALER =  SALES_PERSON11 )) )"
c.execute(sql)
c.execute("commit")


sql = "UPDATE SALES_COUNT_"+TableName+" SET  FTTH_STG2 = (SELECT  SUM(COM_STG2) FROM SALES_"+TableName+" WHERE COM_TYPE = 'FTTH' AND DEALER_NAME = SALES_CHANNEL1 ) WHERE  SUB_DEALER =  DEALER_NAME"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  LTE_STG2 = (SELECT  SUM(COM_STG2) FROM SALES_"+TableName+" WHERE COM_TYPE = 'LTE' AND DEALER_NAME = SALES_CHANNEL1 ) WHERE  SUB_DEALER =  DEALER_NAME"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  MEGALINE_STG2 = (SELECT  SUM(COM_STG2) FROM SALES_"+TableName+" WHERE COM_TYPE = 'MEGALINE' AND DEALER_NAME = SALES_CHANNEL1 ) WHERE  SUB_DEALER =  DEALER_NAME"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  BB_STG2 = (SELECT  SUM(COM_STG2) FROM SALES_"+TableName+" WHERE COM_TYPE = 'BB' AND DEALER_NAME = SALES_CHANNEL1 ) WHERE  SUB_DEALER =  DEALER_NAME"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  IPTV_STG2 = (SELECT  SUM(COM_STG2) FROM SALES_"+TableName+" WHERE COM_TYPE = 'IPTV' AND DEALER_NAME = SALES_CHANNEL1) WHERE  SUB_DEALER =  DEALER_NAME"
c.execute(sql)
c.execute("commit")
sql = "UPDATE SALES_COUNT_"+TableName+" SET  TOT_STG2 = (SELECT  SUM(COM_STG2) FROM SALES_"+TableName+" WHERE DEALER_NAME = SALES_CHANNEL1  ) WHERE  SUB_DEALER =  DEALER_NAME "
c.execute(sql)
c.execute("commit")




sql = "UPDATE SALES_COUNT_"+TableName+" SET  PAYMRNT_STG2 = ROUND(TOT_STG2 - NVL(PAYMRNT_STG1,0),2)"
c.execute(sql)
c.execute("commit")


#create dir
Path(TableName).mkdir(parents=True, exist_ok=True)
Path(TableName+"/STG2").mkdir(parents=True, exist_ok=True)


#exporting data to excel
sql = "SELECT DEALER_NAME FROM "+DealerTableName+" WHERE DEALER_TYPE ='X'";  
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    data = pd.read_sql("SELECT RTOM , EVENT_SOURCE,SERO_ORDT_TYPE,TARIFF_NAME,BSSDSP ACTIVE_DATE ,SALES_CHANNEL1 ,SALES_PERSON11,BSSSTATUS,MEDIUM ,COM_STG1 STAGE1_COMMISSION_PAYED,COM_STG2 STAGE2_COMMISSION FROM SALES_"+TableName+" WHERE SALES_CHANNEL1 = '"+Dealer+"'", engine)
    data.to_excel(TableName+"/STG2/"+Dealer.replace(".", " ")+"_"+TableName+"_STG2.xlsx")


sql = "SELECT SUB_DEALER FROM SALES_COUNT_"+TableName;  
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    data = pd.read_sql("SELECT RTOM , EVENT_SOURCE,SERO_ORDT_TYPE,TARIFF_NAME,BSSDSP ACTIVE_DATE ,SALES_CHANNEL1 ,SALES_PERSON11,BSSSTATUS,MEDIUM ,COM_STG1 STAGE1_COMMISSION_PAYED,COM_STG2 STAGE2_COMMISSION FROM SALES_"+TableName+" WHERE ( SALES_CHANNEL1 = '"+Dealer+"' OR SALES_PERSON11 =  '"+Dealer+"')", engine)
    data.to_excel(TableName+"/STG2/"+Dealer.replace(".", " ")+"_"+TableName+"_STG2.xlsx")
    
c.close()
conn.close()



# #CHECK FOR BB ACTIVE STATUS FOR LTE BEARER SUSPENDED CASES -> IF BB IS ACTIVE CALCULATE BEARER
# sql = "SELECT PRODUCT_ID,BSSDSP,ACCOUNT_NUM,EVENT_SOURCE,PRODUCT_LABEL,SUPPLIER_ORDER_NUM FROM SALES_"+TableName+" WHERE MEDIUM = 'LTE' AND FINALSTATUS = 'SU' AND COM_TYPE = 'LTE'";  
# c.execute(sql)
# for REC in c:
#     Dealer = str(REC[0])
#     x = conn.cursor()
#     sql = "UPDATE SALES_"+TableName+" X SET X.FINALSTATUS = ( SELECT PRODUCT_STATUS  FROM ( "\
#                         "SELECT DISTINCT  CPD.CUSTOMER_REF, CHP.PRODUCT_SEQ, AC.ACCOUNT_NUM, "\
#                         "CHP.PARENT_PRODUCT_SEQ,CHP.PRODUCT_ID, CPS.EFFECTIVE_DTM, "\
#                         "CPS.PRODUCT_STATUS, CPS.STATUS_REASON_TXT, AC.LAST_BILL_DTM , PRODUCT_LABEL "\
#                         "FROM  CUSTPRODUCTSTATUS@DBLINK_GENEVA CPS, CUSTHASPRODUCT@DBLINK_GENEVA CHP, "\
#                         "CUSTPRODUCTDETAILS@DBLINK_GENEVA CPD, PRODUCT@DBLINK_GENEVA PR, ACCOUNT@DBLINK_GENEVA AC "\
#                         "WHERE CPS.CUSTOMER_REF = CPD.CUSTOMER_REF "\
#                         "AND CPS.PRODUCT_SEQ = CPD.PRODUCT_SEQ "\
#                         "AND CHP.CUSTOMER_REF = CPD.CUSTOMER_REF "\
#                         "AND CHP.PRODUCT_SEQ = CPD.PRODUCT_SEQ "\
#                         "AND AC.ACCOUNT_NUM = CPD.ACCOUNT_NUM "\
#                         "AND CHP.PRODUCT_ID  = PR.PRODUCT_ID "\
#                         "AND CHP.PRODUCT_ID = 1524 "\
#                         "AND CHP.PARENT_PRODUCT_SEQ IS NULL "\
#                         "AND CPS.EFFECTIVE_DTM = (SELECT MAX(EFFECTIVE_DTM) FROM CUSTPRODUCTSTATUS@DBLINK_GENEVA CPQ "\
#                                                   "WHERE CPS.CUSTOMER_REF = CPQ.CUSTOMER_REF "\
#                                                    " AND CPS.PRODUCT_SEQ = CPQ.PRODUCT_SEQ "\
#                                                    " AND EFFECTIVE_DTM < (TO_DATE('"+str(REC[1])+"', 'yyyy-mm-dd HH24:MI:SS')+60) ) "\
#                         " AND AC.ACCOUNT_NUM  = '"+str(REC[2])+"' "\
#                         "AND (PRODUCT_LABEL = '"+str(REC[3])+"' OR PRODUCT_LABEL = '"+str(REC[4])+"')  "\
#                         "ORDER BY EFFECTIVE_DTM DESC) "\
#                         "WHERE ROWNUM<2 ) WHERE SUPPLIER_ORDER_NUM = '"+str(REC[5])+"' "
#     print (str(REC[1]))
#     x.execute(sql)
#     x.execute("commit")
#     x.close();




# #CHECK FOR VOICE PAL ACTIVE STATUS FOR LTE BEARER SUSPENDED CASES -> IF VOICE PAL IS ACTIVE CALCULATE BEARER
# sql = "SELECT PRODUCT_ID,BSSDSP,ACCOUNT_NUM,EVENT_SOURCE,PRODUCT_LABEL,SUPPLIER_ORDER_NUM FROM SALES_"+TableName+" , SERVICES_ATTRIBUTES "
# " WHERE MEDIUM = 'LTE' AND FINALSTATUS = 'SU' AND COM_TYPE = 'LTE'"\
# " AND SATT_SERV_ID = SUPPLIER_ORDER_NUM"\
# " AND SATT_ATTRIBUTE_NAME = 'SA_PACKAGE_NAME'"\
# " AND UPPER(SATT_DEFAULTVALUE) LIKE 'VOICE PAL'";  
# c.execute(sql)
# for REC in c:
#     Dealer = str(REC[0])
#     x = conn.cursor()
#     sql = "UPDATE SALES_"+TableName+" X SET X.FINALSTATUS = ( SELECT PRODUCT_STATUS  FROM ( "\
#                         "SELECT DISTINCT  CPD.CUSTOMER_REF, CHP.PRODUCT_SEQ, AC.ACCOUNT_NUM, "\
#                         "CHP.PARENT_PRODUCT_SEQ,CHP.PRODUCT_ID, CPS.EFFECTIVE_DTM, "\
#                         "CPS.PRODUCT_STATUS, CPS.STATUS_REASON_TXT, AC.LAST_BILL_DTM , PRODUCT_LABEL "\
#                         "FROM  CUSTPRODUCTSTATUS@DBLINK_GENEVA CPS, CUSTHASPRODUCT@DBLINK_GENEVA CHP, "\
#                         "CUSTPRODUCTDETAILS@DBLINK_GENEVA CPD, PRODUCT@DBLINK_GENEVA PR, ACCOUNT@DBLINK_GENEVA AC "\
#                         "WHERE CPS.CUSTOMER_REF = CPD.CUSTOMER_REF "\
#                         "AND CPS.PRODUCT_SEQ = CPD.PRODUCT_SEQ "\
#                         "AND CHP.CUSTOMER_REF = CPD.CUSTOMER_REF "\
#                         "AND CHP.PRODUCT_SEQ = CPD.PRODUCT_SEQ "\
#                         "AND AC.ACCOUNT_NUM = CPD.ACCOUNT_NUM "\
#                         "AND CHP.PRODUCT_ID  = PR.PRODUCT_ID "\
#                         "AND CHP.PRODUCT_ID = 1529 "\
#                         "AND CHP.PARENT_PRODUCT_SEQ IS NULL "\
#                         "AND CPS.EFFECTIVE_DTM = (SELECT MAX(EFFECTIVE_DTM) FROM CUSTPRODUCTSTATUS@DBLINK_GENEVA CPQ "\
#                                                   "WHERE CPS.CUSTOMER_REF = CPQ.CUSTOMER_REF "\
#                                                    " AND CPS.PRODUCT_SEQ = CPQ.PRODUCT_SEQ "\
#                                                    " AND EFFECTIVE_DTM < (TO_DATE('"+str(REC[1])+"', 'yyyy-mm-dd HH24:MI:SS')+60) ) "\
#                         " AND AC.ACCOUNT_NUM  = '"+str(REC[2])+"' "\
#                         "AND (PRODUCT_LABEL = '"+str(REC[3])+"' OR PRODUCT_LABEL = '"+str(REC[4])+"')  "\
#                         "ORDER BY EFFECTIVE_DTM DESC) "\
#                         "WHERE ROWNUM<2 ) WHERE SUPPLIER_ORDER_NUM = '"+str(REC[5])+"' "
#     print (str(REC[1]))
#     x.execute(sql)
#     x.execute("commit")
#     x.close();


# #ADD FIRST INVOICE TO SLAES COUNT TABLE
# sql = "ALTER TABLE SALES_"+TableName+" ADD INVOICENO VARCHAR(10)"
# c.execute(sql)

# #ADD CHARGE TO SLAES COUNT TABLE
# sql = "ALTER TABLE SALES_"+TableName+" ADD CHARGES VARCHAR(10)"
# c.execute(sql)


# #ADD PAYMENT TO SLAES COUNT TABLE
# sql = "ALTER TABLE SALES_"+TableName+" ADD TOTPAYMENT VARCHAR(10)"
# c.execute(sql)
