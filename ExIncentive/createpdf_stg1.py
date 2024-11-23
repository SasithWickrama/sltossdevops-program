from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4 , inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.doctemplate import Indenter
from db import DbConnection
from pathlib import Path

conn = DbConnection.dbconn(self="")
c = conn.cursor()
cx = conn.cursor()

styles = getSampleStyleSheet()
heading_style = styles['Heading2']
heading2_style = styles['Heading3']
normal_style = styles['Normal']
body_style = styles['BodyText']


sql = "SELECT TO_CHAR(ADD_MONTHS(TRUNC(SYSDATE,'mm'),-1),'YYYYMM') TBNAME FROM DUAL";  
c.execute(sql)
for TBNAME in c:
    TableName = str(TBNAME[0])

sql = "SELECT TO_CHAR(ADD_MONTHS(TRUNC(SYSDATE,'mm'),-1),'YYYY-MON') TBNAME FROM DUAL";  
c.execute(sql)
for TBNAME in c:
    InvDate = str(TBNAME[0])

#GET ACTIVE DELER TABLE
sql = "SELECT TABLE_NAME  FROM EX_SETTING WHERE DISCRIPTION = 'DEALER' AND END_DATE IS NULL";  
c.execute(sql)
for TABLE_NAME in c:
    DealerTableName = str(TABLE_NAME[0]) 


Path(TableName+"/STG1/PDF").mkdir(parents=True, exist_ok=True)
"""
sql = "SELECT A.DEALER_NAME FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE DEALER_TYPE ='M' AND A.DEALER_NAME = B.DEALER_NAME AND PAYMRNT_STG1 IS NOT NULL"
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Total Commission"),Paragraph("Paybale Commssion")]]
    sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||TARIFF_NAME XX , COM_STG1 , COUNT(EVENT_SOURCE) FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 = '"+Dealer+"'  AND STATUS_STG1 = 0  AND COM_STG1 IS NOT NULL GROUP BY MEDIUM , COM_TYPE ||'-'||TARIFF_NAME,COM_STG1 ORDER BY MEDIUM , COM_TYPE ||'-'||TARIFF_NAME,COM_STG1"
    cx.execute(sqlx)
    totpay =0
    for ROW in cx:
        totcom = float(ROW[3])*float(ROW[2])
        pay = float(ROW[3])*float(ROW[2])/2
        dataArray.append([ROW[0],Paragraph(ROW[1],body_style),ROW[3],ROW[2],totcom,pay])
        totpay = totpay+pay

    dataArray.append(["",Paragraph("Total Paybale",body_style),"","","",totpay])
    docu = SimpleDocTemplate(TableName+"/PDF/"+Dealer.replace(".", " ")+"_"+TableName+"_STG1.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
                            topMargin=1*inch,bottomMargin=15)



    doc_style = styles["Heading1"]
    doc_style.alignment = 0
    title = Paragraph("Dealer Commission System", doc_style)

    doc_style = styles["Heading2"]
    doc_style.alignment = 0
    subtitle = Paragraph("Sales Summery - Stage 1", doc_style)



    heddertable = [
        [],
        ["Sales Channel :", Dealer, "","Month :", TableName ],
        ["Sales Person :","","","","",],
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

"""
#sub dealer pdf creation - Freelancers

sql = "SELECT A.DEALER_NAME , b.SUB_DEALER FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE A.DEALER_NAME = 'Freelancers' AND A.DEALER_NAME = B.DEALER_NAME AND PAYMRNT_STG1 IS NOT NULL"
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
    
  #  "SELECT MEDIUM , COM_TYPE ||'-'||TARIFF_NAME XX , COM_STG1 , COUNT(EVENT_SOURCE) FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 = '"+Dealer+"'  AND STATUS_STG1 = 0  AND COM_STG1 IS NOT NULL GROUP BY MEDIUM , COM_TYPE ||'-'||TARIFF_NAME,COM_STG1 ORDER BY MEDIUM , COM_TYPE ||'-'||TARIFF_NAME,COM_STG1"
    cx.execute(sqlx)
    totpay =0
    for ROW in cx:
        pay = 0
        totcom = float(ROW[3])*float(ROW[2])
        pay = float(ROW[3])*float(ROW[2])/2
        dataArray.append([ROW[0],Paragraph(ROW[1],body_style),ROW[3],"{:.2f}".format(float(ROW[2])),"{:.2f}".format(float(totcom)) , "{:.2f}".format(float(pay))])
        totpay = totpay+pay

    dataArray.append(["",Paragraph("Total Paybale",body_style),"","","","{:.2f}".format(float(totpay)) ])
    docu = SimpleDocTemplate(TableName+"/STG1/Freelancers/"+SubDealer.replace(".", " ")+"_"+TableName+"_STG1.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
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




#sub dealer pdf creation - Mobitel Dealers

sql = "SELECT A.DEALER_NAME , SUB_DEALER FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE A.DEALER_NAME = 'Mobitel Dealers' AND A.DEALER_NAME = B.DEALER_NAME AND PAYMRNT_STG1 IS NOT NULL"
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
    
  #  "SELECT MEDIUM , COM_TYPE ||'-'||TARIFF_NAME XX , COM_STG1 , COUNT(EVENT_SOURCE) FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 = '"+Dealer+"'  AND STATUS_STG1 = 0  AND COM_STG1 IS NOT NULL GROUP BY MEDIUM , COM_TYPE ||'-'||TARIFF_NAME,COM_STG1 ORDER BY MEDIUM , COM_TYPE ||'-'||TARIFF_NAME,COM_STG1"
    cx.execute(sqlx)
    totpay =0
    for ROW in cx:
        pay = 0
        totcom = float(ROW[3])*float(ROW[2])
        pay = float(ROW[3])*float(ROW[2])/2
        dataArray.append([ROW[0],Paragraph(ROW[1],body_style),ROW[3],"{:.2f}".format(float(ROW[2])),"{:.2f}".format(float(totcom)) , "{:.2f}".format(float(pay))])
        totpay = totpay+pay

    dataArray.append(["",Paragraph("Total Paybale",body_style),"","","","{:.2f}".format(float(totpay)) ])
    docu = SimpleDocTemplate(TableName+"/STG1/Mobitel Dealers/"+SubDealer.replace(".", " ")+"_"+TableName+"_STG1.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
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




#sub dealer pdf creation - Mobitel Staff

sql = "SELECT A.DEALER_NAME , SUB_DEALER FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE A.DEALER_NAME = 'Mobitel Staff' AND A.DEALER_NAME = B.DEALER_NAME AND PAYMRNT_STG1 IS NOT NULL"
#print(sql)
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    SubDealer = str(DEALER_NAME[1])
    dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Total Commission"),Paragraph("Paybale Commssion")]]
   
    sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END   XX , NVL(COM_STG1,0) , COUNT(PRODUCT_LABEL) "\
"FROM SALES_"+TableName+"  WHERE SALES_PERSON11 = '"+SubDealer+"' AND STATUS_STG1 = 0  "\
"GROUP BY MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  ,NVL(COM_STG1,0) ORDER BY MEDIUM , "\
"COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  "
    
  #  "SELECT MEDIUM , COM_TYPE ||'-'||TARIFF_NAME XX , COM_STG1 , COUNT(EVENT_SOURCE) FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 = '"+Dealer+"'  AND STATUS_STG1 = 0  AND COM_STG1 IS NOT NULL GROUP BY MEDIUM , COM_TYPE ||'-'||TARIFF_NAME,COM_STG1 ORDER BY MEDIUM , COM_TYPE ||'-'||TARIFF_NAME,COM_STG1"
    cx.execute(sqlx)
    totpay =0
    for ROW in cx:
        pay = 0
        totcom = float(ROW[3])*float(ROW[2])
        pay = float(ROW[3])*float(ROW[2])/2
        dataArray.append([ROW[0],Paragraph(ROW[1],body_style),ROW[3],"{:.2f}".format(float(ROW[2])),"{:.2f}".format(float(totcom)) , "{:.2f}".format(float(pay))])
        totpay = totpay+pay

    dataArray.append(["",Paragraph("Total Paybale",body_style),"","","","{:.2f}".format(float(totpay)) ])
    docu = SimpleDocTemplate(TableName+"/STG1/Mobitel Staff/"+SubDealer.replace(".", " ")+"_"+TableName+"_STG1.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
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




#sub dealer pdf creation - External Channel Dealers

sql = "SELECT A.DEALER_NAME , SUB_DEALER FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE A.DEALER_NAME = 'External Channel Dealers' AND A.DEALER_NAME = B.DEALER_NAME AND PAYMRNT_STG1 IS NOT NULL"
#print(sql)
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    SubDealer = str(DEALER_NAME[1])
    dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Total Commission"),Paragraph("Paybale Commssion")]]
   
    sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END   XX , NVL(COM_STG1,0) , COUNT(PRODUCT_LABEL) "\
"FROM SALES_"+TableName+"  WHERE SALES_PERSON11 = '"+SubDealer+"' AND STATUS_STG1 = 0  "\
"GROUP BY MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  ,NVL(COM_STG1,0) ORDER BY MEDIUM , "\
"COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  "
    
  #  "SELECT MEDIUM , COM_TYPE ||'-'||TARIFF_NAME XX , COM_STG1 , COUNT(EVENT_SOURCE) FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 = '"+Dealer+"'  AND STATUS_STG1 = 0  AND COM_STG1 IS NOT NULL GROUP BY MEDIUM , COM_TYPE ||'-'||TARIFF_NAME,COM_STG1 ORDER BY MEDIUM , COM_TYPE ||'-'||TARIFF_NAME,COM_STG1"
    cx.execute(sqlx)
    totpay =0
    for ROW in cx:
        pay = 0
        totcom = float(ROW[3])*float(ROW[2])
        pay = float(ROW[3])*float(ROW[2])/2
        dataArray.append([ROW[0],Paragraph(ROW[1],body_style),ROW[3],"{:.2f}".format(float(ROW[2])),"{:.2f}".format(float(totcom)) , "{:.2f}".format(float(pay))])
        totpay = totpay+pay

    dataArray.append(["",Paragraph("Total Paybale",body_style),"","","","{:.2f}".format(float(totpay)) ])
    docu = SimpleDocTemplate(TableName+"/STG1/"+SubDealer.replace(".", " ")+"_"+TableName+"_STG1.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
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



sql = "SELECT A.DEALER_NAME , SUB_DEALER FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE DEALER_TYPE = 'M' AND A.DEALER_NAME <> 'Mobitel Staff' AND A.DEALER_NAME = B.DEALER_NAME AND PAYMRNT_STG1 IS NOT NULL"
print(sql)
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    SubDealer = str(DEALER_NAME[1])
    print(SubDealer)
    dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Total Commission"),Paragraph("Paybale Commssion")]]
   
    sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END   XX , NVL(COM_STG1,0) , COUNT(*) "\
"FROM SALES_"+TableName+"  WHERE ( SALES_CHANNEL1 = '"+SubDealer+"' OR SALES_PERSON11 = '"+SubDealer+"' ) AND STATUS_STG1 = 0  "\
"GROUP BY MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  ,NVL(COM_STG1,0) ORDER BY MEDIUM , "\
"COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  "
    
  #  "SELECT MEDIUM , COM_TYPE ||'-'||TARIFF_NAME XX , COM_STG1 , COUNT(EVENT_SOURCE) FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 = '"+Dealer+"'  AND STATUS_STG1 = 0  AND COM_STG1 IS NOT NULL GROUP BY MEDIUM , COM_TYPE ||'-'||TARIFF_NAME,COM_STG1 ORDER BY MEDIUM , COM_TYPE ||'-'||TARIFF_NAME,COM_STG1"
    cx.execute(sqlx)
    totpay =0
    for ROW in cx:
        pay = 0
        totcom = float(ROW[3])*float(ROW[2])
        pay = float(ROW[3])*float(ROW[2])/2
        dataArray.append([ROW[0],Paragraph(ROW[1],body_style),ROW[3],"{:.2f}".format(float(ROW[2])),"{:.2f}".format(float(totcom)) , "{:.2f}".format(float(pay))])
        totpay = totpay+pay

    dataArray.append(["",Paragraph("Total Paybale",body_style),"","","","{:.2f}".format(float(totpay)) ])
    docu = SimpleDocTemplate(TableName+"/STG1/"+SubDealer.replace(".", " ")+"_"+TableName+"_STG1.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
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



#TALENFORT 

dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Total Commission"),Paragraph("Paybale Commssion")]]
   
sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END   XX , NVL(COM_STG1,0) , COUNT(*) "\
"FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 IN ('Talentfort-Dealer','Talentfort-Franchise','Talentfort') AND STATUS_STG1 = 0  "\
"GROUP BY MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  ,NVL(COM_STG1,0) ORDER BY MEDIUM , "\
"COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END  "
    
  #  "SELECT MEDIUM , COM_TYPE ||'-'||TARIFF_NAME XX , COM_STG1 , COUNT(EVENT_SOURCE) FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 = '"+Dealer+"'  AND STATUS_STG1 = 0  AND COM_STG1 IS NOT NULL GROUP BY MEDIUM , COM_TYPE ||'-'||TARIFF_NAME,COM_STG1 ORDER BY MEDIUM , COM_TYPE ||'-'||TARIFF_NAME,COM_STG1"
cx.execute(sqlx)
totpay =0
for ROW in cx:
    pay = 0
    totcom = float(ROW[3])*float(ROW[2])
    pay = float(ROW[3])*float(ROW[2])/2
    dataArray.append([ROW[0],Paragraph(ROW[1],body_style),ROW[3],"{:.2f}".format(float(ROW[2])),"{:.2f}".format(float(totcom)) , "{:.2f}".format(float(pay))])
    totpay = totpay+pay

dataArray.append(["",Paragraph("Total Paybale",body_style),"","","","{:.2f}".format(float(totpay)) ])
docu = SimpleDocTemplate(TableName+"/STG1/Talentfort_"+TableName+"_STG1.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
                            topMargin=1*inch,bottomMargin=15)



doc_style = styles["Heading1"]
doc_style.alignment = 0
title = Paragraph("Dealer Commission System", doc_style)
doc_style = styles["Heading2"]
doc_style.alignment = 0
subtitle = Paragraph("Sales Summery - Stage 1", doc_style)



heddertable = [
        [],
        ["Sales Channel : Talentfort", "","Month :", InvDate ],
        ["Sales Person :","","","","",],
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



