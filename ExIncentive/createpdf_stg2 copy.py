from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4 , inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.doctemplate import Indenter
from db import DbConnection
from pathlib import Path
import math

conn = DbConnection.dbconn(self="")
c = conn.cursor()
cx = conn.cursor()

styles = getSampleStyleSheet()
heading_style = styles['Heading2']
heading2_style = styles['Heading3']
normal_style = styles['Normal']
body_style = styles['BodyText']


sql = "SELECT TO_CHAR(ADD_MONTHS(TRUNC(SYSDATE,'mm'),-3),'YYYYMM') TBNAME FROM DUAL";  
c.execute(sql)
for TBNAME in c:
    TableName = str(TBNAME[0])

sql = "SELECT TO_CHAR(ADD_MONTHS(TRUNC(SYSDATE,'mm'),-3),'YYYY-MON') TBNAME FROM DUAL";  
c.execute(sql)
for TBNAME in c:
    InvDate = str(TBNAME[0])

#GET ACTIVE DELER TABLE
sql = "SELECT TABLE_NAME  FROM EX_SETTING WHERE DISCRIPTION = 'DEALER' AND END_DATE IS NULL";  
c.execute(sql)
for TABLE_NAME in c:
    DealerTableName = str(TABLE_NAME[0]) 


Path(TableName+"/STG2/PDF").mkdir(parents=True, exist_ok=True)

#sub dealer pdf creation

sql = "SELECT A.DEALER_NAME , SUB_DEALER FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE DEALER_TYPE  ('M','X')d AND A.DEALER_NAME = B.DEALER_NAME AND PAYMRNT_STG1 IS NOT NULL"
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    SubDealer = str(DEALER_NAME[1])
    dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Commission")]]
   
    sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END   XX , NVL(COM_STG2,0) , COUNT(EVENT_SOURCE) "\
"FROM SALES_"+TableName+"  WHERE SALES_PERSON11 = '"+SubDealer+"' AND BSSSTATUS = 'OK' "\
"GROUP BY MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  ,NVL(COM_STG2,0) ORDER BY MEDIUM , "\
"COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  "
    
    #print(sqlx)
    cx.execute(sqlx)
    totpay =0
    for ROW in cx:
        totcom = float(ROW[3])*float(ROW[2])
        dataArray.append([ROW[0],Paragraph(ROW[1],body_style),ROW[3],"{:.2f}".format(float(ROW[2])) ,"{:.2f}".format(float(totcom))])
        totpay = totpay+totcom

    dataArray.append(["",Paragraph("Total Commission",body_style),"","","{:.2f}".format(float(totpay)) ])
  
    sql = "SELECT *  FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = '"+SubDealer+"'"
    cx.execute(sql)
    for ROW in cx:
        summaryTable = [
        [],
        ["Stage II Sales Count", ROW[11],  ],
        ["(-)Tereminated Sales Count ", ROW[2] - ROW[11],],
        ["Stage I Sales Count ", ROW[2],],
        ["Stage II Commission ","{:.2f}".format(float(ROW[18])),],
        ["(-)Stage I Paid Commission ", "{:.2f}".format(float(ROW[10])) ,],
        ["Payable Commission ", "{:.2f}".format(float(ROW[19])) ,],
        []
        ]

    doc_style = styles["Heading1"]
    doc_style.alignment = 0
    title = Paragraph("Dealer Commission System", doc_style)

    doc_style = styles["Heading2"]
    doc_style.alignment = 0
    subtitle = Paragraph("Sales Summery - Stage II", doc_style)



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

    style2 = TableStyle([          
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (1,0), (1 ,-1), 'RIGHT'),
            
        
        ])

    # creates a table object using the Table() to pass the table data and the style object
    table1 = Table(heddertable , colWidths=[1*inch,2.5*inch,2.2*inch,0.5*inch, 1*inch])
    table = Table(dataArray, style=style ,  colWidths=[1*inch,2.5*inch,1*inch,1*inch, 1*inch])
    table2 = Table(summaryTable,  style=style2 , colWidths=[3*inch,3*inch,2*inch])

    # finally, we have to build the actual pdf merging all objects together Indenter(left=1*inch),
    docu = SimpleDocTemplate(TableName+"/STG2/PDF/"+SubDealer.replace(".", " ")+"_"+TableName+"_STG1.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
                            topMargin=1*inch,bottomMargin=15)

    docu.build([title, subtitle,table1, table,table2, Indenter(right=1.5*inch)] )


sql = "SELECT A.DEALER_NAME , SUB_DEALER FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE DEALER_TYPE in ('M','X')  AND A.DEALER_NAME = B.DEALER_NAME AND PAYMRNT_STG1 IS NOT NULL"
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    SubDealer = str(DEALER_NAME[1])
    dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Commission")]]
   
    sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END   XX , NVL(COM_STG2,0) , COUNT(EVENT_SOURCE) "\
"FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 = '"+SubDealer+"' AND BSSSTATUS = 'OK' "\
"GROUP BY MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  ,NVL(COM_STG2,0) ORDER BY MEDIUM , "\
"COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  "
    
    #print(sqlx)
    cx.execute(sqlx)
    totpay =0
    for ROW in cx:
        totcom = float(ROW[3])*float(ROW[2])
        dataArray.append([ROW[0],Paragraph(ROW[1],body_style),ROW[3],"{:.2f}".format(float(ROW[2])) ,"{:.2f}".format(float(totcom))])
        totpay = totpay+totcom

    dataArray.append(["",Paragraph("Total Commission",body_style),"","","{:.2f}".format(float(totpay)) ])
  
    sql = "SELECT *  FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = '"+SubDealer+"'"
    cx.execute(sql)
    for ROW in cx:
        summaryTable = [
        [],
        ["Stage II Sales Count", ROW[11],  ],
        ["(-)Tereminated Sales Count ", ROW[2] - ROW[11],],
        ["Stage I Sales Count ", ROW[2],],
        ["Stage II Commission ","{:.2f}".format(float(ROW[18])),],
        ["(-)Stage I Paid Commission ", "{:.2f}".format(float(ROW[10])) ,],
        ["Payable Commission ", "{:.2f}".format(float(ROW[19])) ,],
        []
        ]

    doc_style = styles["Heading1"]
    doc_style.alignment = 0
    title = Paragraph("Dealer Commission System", doc_style)

    doc_style = styles["Heading2"]
    doc_style.alignment = 0
    subtitle = Paragraph("Sales Summery - Stage II", doc_style)



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

    style2 = TableStyle([          
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (1,0), (1 ,-1), 'RIGHT'),
            
        
        ])

    # creates a table object using the Table() to pass the table data and the style object
    table1 = Table(heddertable , colWidths=[1*inch,2.5*inch,2.2*inch,0.5*inch, 1*inch])
    table = Table(dataArray, style=style ,  colWidths=[1*inch,2.5*inch,1*inch,1*inch, 1*inch])
    table2 = Table(summaryTable,  style=style2 , colWidths=[3*inch,3*inch,2*inch])

    # finally, we have to build the actual pdf merging all objects together Indenter(left=1*inch),
    docu = SimpleDocTemplate(TableName+"/STG2/PDF/"+SubDealer.replace(".", " ")+"_"+TableName+"_STG1.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
                            topMargin=1*inch,bottomMargin=15)

    docu.build([title, subtitle,table1, table,table2, Indenter(right=1.5*inch)] )

