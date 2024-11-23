from db import DbConnection
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4 , inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.doctemplate import Indenter
from db import DbConnection
from pathlib import Path

conn = DbConnection.dbconn(self="")
c = conn.cursor()
engine = DbConnection.dbengin()
styles = getSampleStyleSheet()
heading_style = styles['Heading2']
heading2_style = styles['Heading3']
normal_style = styles['Normal']
body_style = styles['BodyText']

sql = "SELECT TO_CHAR(ADD_MONTHS(TRUNC(SYSDATE,'mm'),-1),'YYYYMM') TBNAME FROM DUAL";  
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





sql = "SELECT TO_CHAR(ADD_MONTHS(TRUNC(SYSDATE,'mm'),-1),'YYYY-MON') TBNAME FROM DUAL";  
c.execute(sql)
for TBNAME in c:
    InvDate = str(TBNAME[0])




#exporting data to excel
# sql = "SELECT DEALER_NAME FROM "+DealerTableName+" WHERE DEALER_TYPE ='X'";  
# c.execute(sql)
# for DEALER_NAME in c:
#     Dealer = str(DEALER_NAME[0])
#     data = pd.read_sql("SELECT RTOM , EVENT_SOURCE,MEDIUM,SERO_ORDT_TYPE,TARIFF_NAME,BSSDSP ACTIVE_DATE ,SALES_CHANNEL1 ,SALES_PERSON11,COM_STG1 STAGE1_COMMISSION FROM SALES_"+TableName+" WHERE SALES_CHANNEL1 = '"+Dealer+"'", engine)
#     data.to_excel(TableName+"/STG1/"+Dealer.replace(".", " ")+"_"+TableName+"_STG1.xlsx")


sql = "SELECT SUB_DEALER FROM SALES_COUNT_"+TableName;  
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    data = pd.read_sql("SELECT RTOM , EVENT_SOURCE,MEDIUM,SERO_ORDT_TYPE,TARIFF_NAME,BSSDSP ACTIVE_DATE ,SALES_CHANNEL1 ,SALES_PERSON11 ,COM_STG1 STAGE1_COMMISSION FROM SALES_"+TableName+" WHERE ( SALES_CHANNEL1 = '"+Dealer+"' OR SALES_PERSON11 =  '"+Dealer+"')", engine)
    data.to_excel(TableName+"/STG1/"+Dealer.replace(".", " ")+"_"+TableName+"_STG1.xlsx")




#sub dealer pdf creation

sql = "SELECT A.DEALER_NAME , SUB_DEALER FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE DEALER_TYPE IN ('X','S') AND A.DEALER_NAME = B.DEALER_NAME AND PAYMRNT_STG1 IS NOT NULL"
#print(sql)
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    SubDealer = str(DEALER_NAME[1])
    dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Total Commission"),Paragraph("Paybale Commssion")]]
   
    sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END   XX , NVL(COM_STG1,0) , COUNT(EVENT_SOURCE) "\
"FROM SALES_"+TableName+"  WHERE SALES_PERSON11 = '"+SubDealer+"' AND STATUS_STG1 = 0  "\
"GROUP BY MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  ,NVL(COM_STG1,0) ORDER BY MEDIUM , "\
"COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  "
    
  #  "SELECT MEDIUM , COM_TYPE ||'-'||BB_PACKAGE_NAME XX , COM_STG1 , COUNT(EVENT_SOURCE) FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 = '"+Dealer+"'  AND STATUS_STG1 = 0  AND COM_STG1 IS NOT NULL GROUP BY MEDIUM , COM_TYPE ||'-'||BB_PACKAGE_NAME,COM_STG1 ORDER BY MEDIUM , COM_TYPE ||'-'||BB_PACKAGE_NAME,COM_STG1"
    c.execute(sqlx)
    totpay =0
    for ROW in c:
        totcom = float(ROW[3])*float(ROW[2])
        pay = float(ROW[3])*float(ROW[2])/2
        dataArray.append([ROW[0],Paragraph(ROW[1],body_style),ROW[3],"{:.2f}".format(float(ROW[2])),"{:.2f}".format(float(totcom)) , "{:.2f}".format(float(pay))])
        totpay = totpay+pay

    dataArray.append(["",Paragraph("Total Paybale",body_style),"","","","{:.2f}".format(float(totpay)) ])
    docu = SimpleDocTemplate(TableName+"/STG1/PDF/"+SubDealer.replace(".", " ")+"_"+TableName+"_STG1.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
                            topMargin=1*inch,bottomMargin=15)



    doc_style = styles["Heading1"]
    doc_style.alignment = 0
    title = Paragraph("Dealer Commission System", doc_style)

    doc_style = styles["Heading2"]
    doc_style.alignment = 0
    subtitle = Paragraph("Sales Summery - Stage 1", doc_style)



    heddertable = [
        [],
        ["Sales Channel :", Dealer, "","Month :", InvDate ],
        ["Sales Person :",SubDealer,"","","",],
        []
        ]

    style = TableStyle([          
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("GRID", (0, 0), (-1,-1), 1, colors.black),
            ("BACKGROUND", (0, 0), (5, 0), colors.skyblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ('FONTSIZE', (0, 0), (-1, -1), 10),

            ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
            ('RIGHTPADDING', (3, 1), (3, -1), 20),

            ('ALIGNMENT', (4, 1), (4, -1), 'DECIMAL'),
            ('RIGHTPADDING', (4, 1), (-1, -1), 20),

            ('ALIGNMENT', (5, 1), (5, -1), 'DECIMAL'),
            ('RIGHTPADDING', (5, 1), (-1, -1), 20),           
        ])

    # creates a table object using the Table() to pass the table data and the style object
    table1 = Table(heddertable , colWidths=[1*inch,2.5*inch,2.2*inch,0.5*inch, 1*inch])
    table = Table(dataArray, style=style ,  colWidths=[1*inch,2.5*inch,1*inch,1*inch, 1*inch])

    # finally, we have to build the actual pdf merging all objects together Indenter(left=1*inch),

    docu.build([title, subtitle,table1, table, Indenter(right=1.5*inch)] )


sql = "SELECT A.DEALER_NAME , SUB_DEALER FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE DEALER_TYPE in ('M','X') AND A.DEALER_NAME = B.DEALER_NAME AND PAYMRNT_STG1 IS NOT NULL"
print(sql)
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    SubDealer = str(DEALER_NAME[1])
    print(SubDealer)
    dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Total Commission"),Paragraph("Paybale Commssion")]]
   
    sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END   XX , NVL(COM_STG1,0) , COUNT(EVENT_SOURCE) "\
"FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 = '"+SubDealer+"' AND STATUS_STG1 = 0  "\
"GROUP BY MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  ,NVL(COM_STG1,0) ORDER BY MEDIUM , "\
"COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  "
    
  #  "SELECT MEDIUM , COM_TYPE ||'-'||BB_PACKAGE_NAME XX , COM_STG1 , COUNT(EVENT_SOURCE) FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 = '"+Dealer+"'  AND STATUS_STG1 = 0  AND COM_STG1 IS NOT NULL GROUP BY MEDIUM , COM_TYPE ||'-'||BB_PACKAGE_NAME,COM_STG1 ORDER BY MEDIUM , COM_TYPE ||'-'||BB_PACKAGE_NAME,COM_STG1"
    c.execute(sqlx)
    totpay =0
    for ROW in c:
        totcom = float(ROW[3])*float(ROW[2])
        pay = float(ROW[3])*float(ROW[2])/2
        dataArray.append([ROW[0],Paragraph(ROW[1],body_style),ROW[3],"{:.2f}".format(float(ROW[2])),"{:.2f}".format(float(totcom)) , "{:.2f}".format(float(pay))])
        totpay = totpay+pay

    dataArray.append(["",Paragraph("Total Paybale",body_style),"","","","{:.2f}".format(float(totpay)) ])
    docu = SimpleDocTemplate(TableName+"/STG1/PDF/"+SubDealer.replace(".", " ")+"_"+TableName+"_STG1.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
                            topMargin=1*inch,bottomMargin=15)



    doc_style = styles["Heading1"]
    doc_style.alignment = 0
    title = Paragraph("Dealer Commission System", doc_style)

    doc_style = styles["Heading2"]
    doc_style.alignment = 0
    subtitle = Paragraph("Sales Summery - Stage 1", doc_style)



    heddertable = [
        [],
        ["Sales Channel :", Dealer, "","Month :", InvDate ],
        ["Sales Person :",SubDealer,"","","",],
        []
        ]

    style = TableStyle([          
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("GRID", (0, 0), (-1,-1), 1, colors.black),
            ("BACKGROUND", (0, 0), (5, 0), colors.skyblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ('FONTSIZE', (0, 0), (-1, -1), 10),

            ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
            ('RIGHTPADDING', (3, 1), (3, -1), 20),

            ('ALIGNMENT', (4, 1), (4, -1), 'DECIMAL'),
            ('RIGHTPADDING', (4, 1), (-1, -1), 20),

            ('ALIGNMENT', (5, 1), (5, -1), 'DECIMAL'),
            ('RIGHTPADDING', (5, 1), (-1, -1), 20),           
        ])

    # creates a table object using the Table() to pass the table data and the style object
    table1 = Table(heddertable , colWidths=[1*inch,2.5*inch,2.2*inch,0.5*inch, 1*inch])
    table = Table(dataArray, style=style ,  colWidths=[1*inch,2.5*inch,1*inch,1*inch, 1*inch])

    # finally, we have to build the actual pdf merging all objects together Indenter(left=1*inch),

    docu.build([title, subtitle,table1, table, Indenter(right=1.5*inch)] )
 
c.close()
conn.close()