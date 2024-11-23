from db import DbConnection
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

conn = DbConnection.dbconn(self="")
c = conn.cursor()
engine = DbConnection.dbengin()

sql = "SELECT TO_CHAR(ADD_MONTHS(TRUNC(SYSDATE,'mm'),-1),'YYYYMM') TBNAME FROM DUAL";  
c.execute(sql)
for TBNAME in c:
    TableName = str(TBNAME[0])

#REMOVE BLACKLIST PRICE PLANS
sql = "UPDATE SALES_"+TableName+" SET STATUS_STG1 = 100 WHERE TARIFF_NAME IN (SELECT PRICEPLAN FROM EX_PRICEPLAN_BL "\
" WHERE SERVICE_TYPE = COM_TYPE)"
c.execute(sql)
c.execute("commit")

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

#CREATE SLAES COUNT TABLE
sql = "CREATE TABLE SALES_COUNT_"+TableName+" AS SELECT DEALER_NAME ,DEALER_NAME SUB_DEALER , COUNT (*) SALES_COUNT FROM "+DealerTableName+" , SALES_"+TableName+" WHERE DEALER_NAME = SALES_CHANNEL1 AND COM_TYPE IN ('MEGALINE' , 'LTE' , 'FTTH') AND DEALER_TYPE = 'M' AND STATUS_STG1 = 0 GROUP BY DEALER_NAME , DEALER_NAME UNION SELECT DEALER_NAME,SALES_PERSON11 , COUNT (*) FROM "+DealerTableName+" , SALES_"+TableName+" WHERE DEALER_NAME = SALES_CHANNEL1 AND COM_TYPE IN ('MEGALINE' , 'LTE' , 'FTTH') AND DEALER_TYPE IN ('S','X') AND STATUS_STG1 = 0 GROUP BY DEALER_NAME,SALES_PERSON11"
c.execute(sql)
c.execute("commit")

#ADD SLAB
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD SLAB varchar(2)"
c.execute(sql)
c.execute("commit")

#UPDATE SLAB
sql = "UPDATE SALES_COUNT_"+TableName+" SET SLAB = (SELECT SLAB FROM  "+SlabTableName+" WHERE SALES_COUNT  BETWEEN MIN_SALES AND MAX_SALES)"
c.execute(sql)
c.execute("commit")

# #UPDATE SLAB FOR Freelancers SLAB IS B AND ALL AMMOUNT SHOULD BE 65% OF SLAB B VALUE
sql = "UPDATE SALES_COUNT_"+TableName+" SET SLAB = 'B' WHERE DEALER_NAME = 'Freelancers'"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1
sql = "ALTER TABLE SALES_"+TableName+" ADD COM_STG1 NUMBER"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION FROM "+BBTableName+" WHERE UPPER(PACKAGE) = UPPER(REPLACE(BB_PACKAGE_NAME,'LTE_','') ) AND SLAB = 'B' ) WHERE COM_TYPE = 'BB' AND STATUS_STG1 = 0"
c.execute(sql)
c.execute("commit")
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION FROM "+BBTableName+" WHERE UPPER(PACKAGE) = UPPER(BB_PACKAGE_NAME) AND SLAB = 'B' ) WHERE COM_TYPE = 'BB' AND STATUS_STG1 = 0 AND COM_STG1 IS NULL"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1 - FREELANCER 
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION * 0.65 FROM "+BBTableName+" WHERE UPPER(PACKAGE) = UPPER(REPLACE(BB_PACKAGE_NAME,'LTE_','') ) AND SLAB = 'B' ) WHERE COM_TYPE = 'BB' AND STATUS_STG1 = 0 AND SALES_CHANNEL1 = 'Freelancers' "
c.execute(sql)
c.execute("commit")
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION * 0.65 FROM "+BBTableName+" WHERE UPPER(PACKAGE) = UPPER(BB_PACKAGE_NAME ) AND SLAB = 'B' ) WHERE COM_TYPE = 'BB' AND STATUS_STG1 = 0 AND SALES_CHANNEL1 = 'Freelancers' AND COM_STG1 IS NULL"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION FROM "+IPTVTableName+" WHERE UPPER(PACKAGE) = UPPER(REPLACE(BB_PACKAGE_NAME,' Rental','')) AND SLAB = 'B' ) WHERE COM_TYPE = 'IPTV' AND STATUS_STG1 = 0"
c.execute(sql)
c.execute("commit")
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION FROM "+IPTVTableName+" WHERE UPPER(PACKAGE) = UPPER(BB_PACKAGE_NAME) AND SLAB = 'B' ) WHERE COM_TYPE = 'IPTV' AND STATUS_STG1 = 0 AND COM_STG1 IS NULL"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1 - FREELANCER 
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION * 0.65  FROM "+IPTVTableName+" WHERE UPPER(PACKAGE) = UPPER(REPLACE(BB_PACKAGE_NAME,' Rental','')) AND SLAB = 'B' ) WHERE COM_TYPE = 'IPTV' AND STATUS_STG1 = 0 AND SALES_CHANNEL1 = 'Freelancers'"
c.execute(sql)
c.execute("commit")
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION * 0.65  FROM "+IPTVTableName+" WHERE UPPER(PACKAGE) = UPPER(BB_PACKAGE_NAME) AND SLAB = 'B' ) WHERE COM_TYPE = 'IPTV' AND STATUS_STG1 = 0 AND SALES_CHANNEL1 = 'Freelancers' AND COM_STG1 IS NULL"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION FROM "+BearerTableName+" WHERE PRODUCT = 'FTTH New' AND SLAB = 'B' ) WHERE COM_TYPE = 'FTTH' AND SERO_ORDT_TYPE = 'CREATE' AND STATUS_STG1 = 0"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1 - FREELANCER 
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION * 0.65  FROM "+BearerTableName+" WHERE PRODUCT = 'FTTH New' AND SLAB = 'B' ) WHERE COM_TYPE = 'FTTH' AND SERO_ORDT_TYPE = 'CREATE' AND STATUS_STG1 = 0 AND SALES_CHANNEL1 = 'Freelancers'"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION FROM "+BearerTableName+" WHERE PRODUCT = 'FTTH Migration' AND SLAB = 'B' ) WHERE COM_TYPE = 'FTTH' AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' AND STATUS_STG1 = 0"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1 - FREELANCER 
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION * 0.65 FROM "+BearerTableName+" WHERE PRODUCT = 'FTTH Migration' AND SLAB = 'B' ) WHERE COM_TYPE = 'FTTH' AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' AND STATUS_STG1 = 0 AND SALES_CHANNEL1 = 'Freelancers'"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION FROM "+BearerTableName+" WHERE PRODUCT = 'Megaline' AND SLAB = 'B' ) WHERE COM_TYPE = 'MEGALINE' AND STATUS_STG1 = 0"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1 - FREELANCER 
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION * 0.65 FROM "+BearerTableName+" WHERE PRODUCT = 'Megaline' AND SLAB = 'B' ) WHERE COM_TYPE = 'MEGALINE' AND STATUS_STG1 = 0 AND SALES_CHANNEL1 = 'Freelancers'"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION FROM "+BearerTableName+" WHERE PRODUCT = 'LTE' AND SLAB = 'B' ) WHERE COM_TYPE = 'LTE' AND STATUS_STG1 = 0"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1 - FREELANCER
sql = "UPDATE SALES_"+TableName+" SET COM_STG1 = (SELECT DISTINCT COMMISSION * 0.65 FROM "+BearerTableName+" WHERE PRODUCT = 'LTE' AND SLAB = 'B' ) WHERE COM_TYPE = 'LTE' AND STATUS_STG1 = 0 AND SALES_CHANNEL1 = 'Freelancers'"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD FTTH_STG1 VARCHAR2(20)"
c.execute(sql)
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD FTTH_STG1_PAY VARCHAR2(20)"
c.execute(sql)

sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD BB_STG1 VARCHAR2(20)"
c.execute(sql)
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD BB_STG1_PAY VARCHAR2(20)"
c.execute(sql)

sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD MEGALINE_STG1 VARCHAR2(20)"
c.execute(sql)
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD MEGALINE_STG1_PAY VARCHAR2(20)"
c.execute(sql)

sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD LTE_STG1 VARCHAR2(20)"
c.execute(sql)
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD LTE_STG1_PAY VARCHAR2(20)"
c.execute(sql)

sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD IPTV_STG1 VARCHAR2(20)"
c.execute(sql)
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD IPTV_STG1_PAY VARCHAR2(20)"
c.execute(sql)

sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD TOT_STG1 VARCHAR2(20)"
c.execute(sql)
sql = "ALTER TABLE SALES_COUNT_"+TableName+" ADD PAYMRNT_STG1 VARCHAR2(20)"
c.execute(sql)
c.execute("commit")

#ADD COM_STG1
sql = "UPDATE SALES_COUNT_"+TableName+" SET  FTTH_STG1 = (SELECT  SUM(COM_STG1) FROM SALES_"+TableName+" WHERE COM_TYPE = 'FTTH' AND ((DEALER_NAME = SALES_CHANNEL1 AND SUB_DEALER =  SALES_PERSON11 )) )"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  LTE_STG1 = (SELECT  SUM(COM_STG1) FROM SALES_"+TableName+" WHERE COM_TYPE = 'LTE' AND ((DEALER_NAME = SALES_CHANNEL1 AND SUB_DEALER =  SALES_PERSON11 )) )"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  MEGALINE_STG1 = (SELECT  SUM(COM_STG1) FROM SALES_"+TableName+" WHERE COM_TYPE = 'MEGALINE' AND ((DEALER_NAME = SALES_CHANNEL1 AND SUB_DEALER =  SALES_PERSON11 )) )"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  BB_STG1 = (SELECT  SUM(COM_STG1) FROM SALES_"+TableName+" WHERE COM_TYPE = 'BB' AND ((DEALER_NAME = SALES_CHANNEL1 AND SUB_DEALER =  SALES_PERSON11 )) )"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  IPTV_STG1 = (SELECT  SUM(COM_STG1) FROM SALES_"+TableName+" WHERE COM_TYPE = 'IPTV' AND ((DEALER_NAME = SALES_CHANNEL1 AND SUB_DEALER =  SALES_PERSON11 )) )"
c.execute(sql)
c.execute("commit")
sql = "UPDATE SALES_COUNT_"+TableName+" SET  TOT_STG1 = (SELECT  SUM(COM_STG1) FROM SALES_"+TableName+" WHERE ((DEALER_NAME = SALES_CHANNEL1 AND SUB_DEALER =  SALES_PERSON11 )) )"
c.execute(sql)
c.execute("commit")


sql = "UPDATE SALES_COUNT_"+TableName+" SET  FTTH_STG1 = (SELECT  SUM(COM_STG1) FROM SALES_"+TableName+" WHERE COM_TYPE = 'FTTH' AND DEALER_NAME = SALES_CHANNEL1 ) WHERE  SUB_DEALER =  DEALER_NAME"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  LTE_STG1 = (SELECT  SUM(COM_STG1) FROM SALES_"+TableName+" WHERE COM_TYPE = 'LTE' AND DEALER_NAME = SALES_CHANNEL1 ) WHERE  SUB_DEALER =  DEALER_NAME"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  MEGALINE_STG1 = (SELECT  SUM(COM_STG1) FROM SALES_"+TableName+" WHERE COM_TYPE = 'MEGALINE' AND DEALER_NAME = SALES_CHANNEL1 ) WHERE  SUB_DEALER =  DEALER_NAME"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  BB_STG1 = (SELECT  SUM(COM_STG1) FROM SALES_"+TableName+" WHERE COM_TYPE = 'BB' AND DEALER_NAME = SALES_CHANNEL1 ) WHERE  SUB_DEALER =  DEALER_NAME"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  IPTV_STG1 = (SELECT  SUM(COM_STG1) FROM SALES_"+TableName+" WHERE COM_TYPE = 'IPTV' AND DEALER_NAME = SALES_CHANNEL1) WHERE  SUB_DEALER =  DEALER_NAME"
c.execute(sql)
c.execute("commit")
sql = "UPDATE SALES_COUNT_"+TableName+" SET  TOT_STG1 = (SELECT  SUM(COM_STG1) FROM SALES_"+TableName+" WHERE DEALER_NAME = SALES_CHANNEL1  ) WHERE  SUB_DEALER =  DEALER_NAME "
c.execute(sql)
c.execute("commit")


sql = "UPDATE SALES_COUNT_"+TableName+" SET  FTTH_STG1_PAY = ROUND(FTTH_STG1/2,2) WHERE SLAB <> 'A'"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  BB_STG1_PAY = ROUND(BB_STG1/2,2) WHERE SLAB <> 'A'"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  MEGALINE_STG1_PAY = ROUND(MEGALINE_STG1/2,2) WHERE SLAB <> 'A'"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  LTE_STG1_PAY = ROUND(LTE_STG1/2,2) WHERE SLAB <> 'A'"
c.execute(sql)
sql = "UPDATE SALES_COUNT_"+TableName+" SET  IPTV_STG1_PAY = ROUND(IPTV_STG1/2,2) WHERE SLAB <> 'A'"
c.execute(sql)

sql = "UPDATE SALES_COUNT_"+TableName+" SET  PAYMRNT_STG1 = ROUND(TOT_STG1/2,2) WHERE SLAB <> 'A'"
c.execute(sql)
c.execute("commit")


#create dir
Path(TableName).mkdir(parents=True, exist_ok=True)
Path(TableName+"/STG1").mkdir(parents=True, exist_ok=True)


#exporting data to excel

#Mobitel Dealers
Path(TableName+"/STG1/Mobitel Dealers").mkdir(parents=True, exist_ok=True)
#sql = "SELECT DEALER_NAME FROM "+DealerTableName+" WHERE DEALER_TYPE ='X'";  
#c.execute(sql)
#for DEALER_NAME in c:
Dealer = "Mobitel Dealers"
data = pd.read_sql("SELECT DISTINCT RTOM , PRODUCT_LABEL,ACCOUNT_NUM,MEDIUM,SERO_ORDT_TYPE,COM_TYPE,TARIFF_NAME,BSSDSP ACTIVE_DATE ,SALES_CHANNEL1 ,SALES_PERSON11 , ROUND(COM_STG1/2,2) COM_STG1 FROM SALES_"+TableName+" WHERE SALES_CHANNEL1 = '"+Dealer+"'", engine)
data.to_excel(TableName+"/STG1/Mobitel Dealers/"+Dealer.replace(".", " ")+"_"+TableName+"_STG1.xlsx")

#Freelancers
Path(TableName+"/STG1/Freelancers").mkdir(parents=True, exist_ok=True)
sql = "SELECT SUB_DEALER FROM SALES_COUNT_"+TableName+" WHERE DEALER_NAME = 'Freelancers' ";  
c.execute(sql)
for SUB_DEALER in c:
    Dealer = str(SUB_DEALER[0])
    data = pd.read_sql("SELECT DISTINCT RTOM , PRODUCT_LABEL,ACCOUNT_NUM,MEDIUM,SERO_ORDT_TYPE,COM_TYPE,TARIFF_NAME,BSSDSP ACTIVE_DATE ,SALES_CHANNEL1 ,SALES_PERSON11 , ROUND(COM_STG1/2,2) COM_STG1  FROM SALES_"+TableName+" WHERE SALES_CHANNEL1 = '"+Dealer+"'", engine)
    data.to_excel(TableName+"/STG1/Freelancers/"+Dealer.replace(".", " ")+"_"+TableName+"_STG1.xlsx")

#Mobitel Staff
Path(TableName+"/STG1/Mobitel Staff").mkdir(parents=True, exist_ok=True)
Dealer = "Mobitel Staff"
data = pd.read_sql("SELECT DISTINCT RTOM , PRODUCT_LABEL,ACCOUNT_NUM,MEDIUM,SERO_ORDT_TYPE,COM_TYPE,TARIFF_NAME,BSSDSP ACTIVE_DATE ,SALES_CHANNEL1 ,SALES_PERSON11 , ROUND(COM_STG1/2,2) COM_STG1  FROM SALES_"+TableName+" WHERE SALES_CHANNEL1 = '"+Dealer+"'", engine)
data.to_excel(TableName+"/STG1/Mobitel Staff/"+Dealer.replace(".", " ")+"_"+TableName+"_STG1.xlsx")

sql = "SELECT SUB_DEALER FROM SALES_COUNT_"+TableName+" WHERE DEALER_NAME = 'Mobitel Staff' ";  
c.execute(sql)
for SUB_DEALER in c:
    Dealer = str(SUB_DEALER[0])
    data = pd.read_sql("SELECT DISTINCT RTOM , PRODUCT_LABEL,ACCOUNT_NUM,MEDIUM,SERO_ORDT_TYPE,COM_TYPE,TARIFF_NAME,BSSDSP ACTIVE_DATE ,SALES_CHANNEL1 ,SALES_PERSON11 , ROUND(COM_STG1/2,2) COM_STG1  FROM SALES_"+TableName+" WHERE SALES_CHANNEL1 = '"+Dealer+"'", engine)
    data.to_excel(TableName+"/STG1/Mobitel Staff/"+Dealer.replace(".", " ")+"_"+TableName+"_STG1.xlsx")

#OTHER DEALERS
sql = "SELECT SUB_DEALER FROM SALES_COUNT_"+TableName+" WHERE DEALER_NAME NOT IN ('Mobitel Staff','Freelancers','Mobitel Dealers')";  
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    data = pd.read_sql("SELECT DISTINCT RTOM , PRODUCT_LABEL,ACCOUNT_NUM,MEDIUM,SERO_ORDT_TYPE,COM_TYPE,TARIFF_NAME,BSSDSP ACTIVE_DATE ,SALES_CHANNEL1 ,SALES_PERSON11, ROUND(COM_STG1/2,2) COM_STG1  FROM SALES_"+TableName+" WHERE ( SALES_CHANNEL1 = '"+Dealer+"' OR SALES_PERSON11 =  '"+Dealer+"')", engine)
    data.to_excel(TableName+"/STG1/"+Dealer.replace(".", " ")+"_"+TableName+"_STG1.xlsx")
    
c.close()
conn.close()