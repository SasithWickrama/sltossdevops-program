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


#sub dealer pdf creation - Freelancers

sql = "SELECT A.DEALER_NAME , b.SUB_DEALER FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE A.DEALER_NAME = 'Freelancers' AND A.DEALER_NAME = B.DEALER_NAME AND PAYMRNT_STG1 IS NOT NULL"
#print(sql)
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    SubDealer = str(DEALER_NAME[1])
    dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Commission")]]
   
    sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END   XX , NVL(COM_STG2,0) , COUNT(EVENT_SOURCE) "\
"FROM SALES_"+TableName+"  WHERE SALES_PERSON11 = '"+SubDealer+"' AND FINALSTATUS = 'OK' "\
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
  
    # sql = "SELECT *  FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = '"+SubDealer+"'"
    # cx.execute(sql)
    # for ROW in cx:
    #     summaryTable = [
    #     [],
    #     ["Stage II Sales Count", ROW[11],  ],
    #     ["(-)Tereminated Sales Count ", ROW[2] - ROW[11],],
    #     ["Stage I Sales Count ", ROW[2],],
    #     ["Stage II Commission ","{:.2f}".format(float(ROW[18])),],
    #     ["(-)Stage I Paid Commission ", "{:.2f}".format(float(ROW[10])) ,],
    #     ["Payable Commission ", "{:.2f}".format(float(ROW[19])) ,],
    #     []
    #     ]
    sql = "SELECT '', NVL(SUM(SALES_COUNT_STG2),'0'), NVL(SUM(SALES_COUNT),'0') , NVL(SUM(TOT_STG2),'0') , NVL(SUM(PAYMRNT_STG1),'0') ,NVL(SUM(PAYMRNT_STG2),'0')  FROM SALES_COUNT_"+TableName+" WHERE  SUB_DEALER = '"+SubDealer+"'"
    #print(sql)
    cx.execute(sql)
    for ROW in cx:
        summaryTable = [
        [],
        ["Stage II Sales Count", ROW[1],  ],
        ["(-)Tereminated Sales Count ", ROW[2] - ROW[1],],
        ["Stage I Sales Count ", ROW[2],],
        ["Stage II Commission ","{:.2f}".format(float(ROW[3])),],
        ["(-)Stage I Paid Commission ", "{:.2f}".format(float(ROW[4])) ,],
        ["Payable Commission ", "{:.2f}".format(float(ROW[5])) ,],
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
    docu = SimpleDocTemplate(TableName+"/STG2/Freelancers/"+SubDealer.replace(".", " ")+"_"+TableName+"_STG2.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
                            topMargin=1*inch,bottomMargin=15)

    docu.build([title, subtitle,table1, table,table2, Indenter(right=1.5*inch)] )




#sub dealer pdf creation - Mobitel Dealers

sql = "SELECT distinct A.DEALER_NAME FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE A.DEALER_NAME = 'Mobitel Dealers' AND A.DEALER_NAME = B.DEALER_NAME "
#print(sql)
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
   # SubDealer = str(DEALER_NAME[1])
    dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Commission")]]
   
    sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END   XX , NVL(COM_STG2,0) , COUNT(EVENT_SOURCE) "\
"FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 = '"+Dealer+"' AND FINALSTATUS = 'OK' "\
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
  
    sql = "SELECT DEALER_NAME , SUM(SALES_COUNT_STG2), SUM(SALES_COUNT) , SUM(TOT_STG2) , NVL(SUM(PAYMRNT_STG1),'0') ,SUM(PAYMRNT_STG2)  FROM SALES_COUNT_"+TableName+" WHERE DEALER_NAME = '"+Dealer+"' GROUP BY DEALER_NAME"
    #print(sql)
    cx.execute(sql)
    for ROW in cx:
        summaryTable = [
        [],
        ["Stage II Sales Count", ROW[1],  ],
        ["(-)Tereminated Sales Count ", ROW[2] - ROW[1],],
        ["Stage I Sales Count ", ROW[2],],
        ["Stage II Commission ","{:.2f}".format(float(ROW[3])),],
        ["(-)Stage I Paid Commission ", "{:.2f}".format(float(ROW[4])) ,],
        ["Payable Commission ", "{:.2f}".format(float(ROW[5])) ,],
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
    docu = SimpleDocTemplate(TableName+"/STG2/Mobitel Dealers/"+Dealer.replace(".", " ")+"_"+TableName+"_STG2.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
                            topMargin=1*inch,bottomMargin=15)

    docu.build([title, subtitle,table1, table,table2, Indenter(right=1.5*inch)] )





#sub dealer pdf creation - Mobitel Staff

sql = "SELECT distinct A.DEALER_NAME FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE A.DEALER_NAME = 'Mobitel Staff' AND A.DEALER_NAME = B.DEALER_NAME "
#print(sql)
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
   # SubDealer = str(DEALER_NAME[1])
    dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Commission")]]
   
    sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END   XX , NVL(COM_STG2,0) , COUNT(EVENT_SOURCE) "\
"FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 = '"+Dealer+"' AND FINALSTATUS = 'OK' "\
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
  
    sql = "SELECT DEALER_NAME , SUM(SALES_COUNT_STG2), SUM(SALES_COUNT) , SUM(TOT_STG2) , NVL(SUM(PAYMRNT_STG1),'0') ,SUM(PAYMRNT_STG2)  FROM SALES_COUNT_"+TableName+" WHERE DEALER_NAME = '"+Dealer+"' GROUP BY DEALER_NAME"
    #print(sql)
    cx.execute(sql)
    for ROW in cx:
        summaryTable = [
        [],
        ["Stage II Sales Count", ROW[1],  ],
        ["(-)Tereminated Sales Count ", ROW[2] - ROW[1],],
        ["Stage I Sales Count ", ROW[2],],
        ["Stage II Commission ","{:.2f}".format(float(ROW[3])),],
        ["(-)Stage I Paid Commission ", "{:.2f}".format(float(ROW[4])) ,],
        ["Payable Commission ", "{:.2f}".format(float(ROW[5])) ,],
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
    docu = SimpleDocTemplate(TableName+"/STG2/Mobitel Staff/"+Dealer.replace(".", " ")+"_"+TableName+"_STG2.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
                            topMargin=1*inch,bottomMargin=15)

    docu.build([title, subtitle,table1, table,table2, Indenter(right=1.5*inch)] )




#sub dealer pdf creation - External Channel Dealers

sql = "SELECT A.DEALER_NAME , SUB_DEALER FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE A.DEALER_NAME = 'External Channel Dealers' AND A.DEALER_NAME = B.DEALER_NAME "
#print(sql)
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    SubDealer = str(DEALER_NAME[1])
    dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Commission")]]
   
    sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END   XX , NVL(COM_STG2,0) , COUNT(EVENT_SOURCE) "\
"FROM SALES_"+TableName+"  WHERE SALES_PERSON11 = '"+SubDealer+"' AND FINALSTATUS = 'OK' "\
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
  
    sql = "SELECT  DEALER_NAME , NVL(SALES_COUNT_STG2,'0'), NVL(SALES_COUNT,'0') , NVL(TOT_STG2,'0') , NVL(PAYMRNT_STG1,'0') ,NVL(PAYMRNT_STG2,'0')  FROM SALES_COUNT_"+TableName+" WHERE SUB_DEALER = '"+SubDealer+"'"
    cx.execute(sql)
    for ROW in cx:
        summaryTable = [
        [],
        ["Stage II Sales Count", ROW[1],  ],
        ["(-)Tereminated Sales Count ", ROW[2] - ROW[1],],
        ["Stage I Sales Count ", ROW[2],],
        ["Stage II Commission ","{:.2f}".format(float(ROW[3])),],
        ["(-)Stage I Paid Commission ", "{:.2f}".format(float(ROW[4])) ,],
        ["Payable Commission ", "{:.2f}".format(float(ROW[5])) ,],
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
    docu = SimpleDocTemplate(TableName+"/STG2/"+SubDealer.replace(".", " ")+"_"+TableName+"_STG2.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
                            topMargin=1*inch,bottomMargin=15)

    docu.build([title, subtitle,table1, table,table2, Indenter(right=1.5*inch)] )



sql = "SELECT A.DEALER_NAME , SUB_DEALER FROM "+DealerTableName+" A , SALES_COUNT_"+TableName+" B WHERE DEALER_TYPE = 'M' AND A.DEALER_NAME <> 'Mobitel Staff' AND A.DEALER_NAME = B.DEALER_NAME "
#print(sql)
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
   # SubDealer = str(DEALER_NAME[1])
    dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Commission")]]
   
    sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END   XX , NVL(COM_STG2,0) , COUNT(EVENT_SOURCE) "\
"FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 = '"+Dealer+"' AND FINALSTATUS = 'OK' "\
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
  
    sql = "SELECT DEALER_NAME , SUM(SALES_COUNT_STG2), SUM(SALES_COUNT) , SUM(TOT_STG2) , NVL(SUM(PAYMRNT_STG1),'0') ,SUM(PAYMRNT_STG2)  FROM SALES_COUNT_"+TableName+" WHERE DEALER_NAME = '"+Dealer+"' GROUP BY DEALER_NAME"
    #print(sql)
    cx.execute(sql)
    for ROW in cx:
        summaryTable = [
        [],
        ["Stage II Sales Count", ROW[1],  ],
        ["(-)Tereminated Sales Count ", ROW[2] - ROW[1],],
        ["Stage I Sales Count ", ROW[2],],
        ["Stage II Commission ","{:.2f}".format(float(ROW[3])),],
        ["(-)Stage I Paid Commission ", "{:.2f}".format(float(ROW[4])) ,],
        ["Payable Commission ", "{:.2f}".format(float(ROW[5])) ,],
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
    docu = SimpleDocTemplate(TableName+"/STG2/"+Dealer.replace(".", " ")+"_"+TableName+"_STG2.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
                            topMargin=1*inch,bottomMargin=15)

    docu.build([title, subtitle,table1, table,table2, Indenter(right=1.5*inch)] )


#TALENT PORT ALL

dataArray = [ [Paragraph("Access Bearer"),"Medium",Paragraph("Total Count"),Paragraph("Commission Rate"),Paragraph("Commission")]]
   
sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||CASE WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE' THEN 'CREATE' "\
"WHEN BB_PACKAGE_NAME IS NULL AND SERO_ORDT_TYPE = 'CREATE-UPGRD SAME NO' THEN 'UPGRADE' "\
"ELSE REPLACE(BB_PACKAGE_NAME,'LTE_','') END   XX , NVL(COM_STG2,0) , COUNT(EVENT_SOURCE) "\
"FROM SALES_"+TableName+"  WHERE SALES_CHANNEL1 IN ('Talentfort-Dealer','Talentfort-Franchise','Talentfort') AND FINALSTATUS = 'OK' "\
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
  
sql = "SELECT  '0', SUM(SALES_COUNT_STG2), SUM(SALES_COUNT) , SUM(TOT_STG2) , NVL(SUM(PAYMRNT_STG1),'0') ,SUM(PAYMRNT_STG2)  FROM SALES_COUNT_"+TableName+" WHERE DEALER_NAME IN ('Talentfort-Dealer','Talentfort-Franchise','Talentfort') "
    #print(sql)
cx.execute(sql)
for ROW in cx:
    summaryTable = [
    [],
    ["Stage II Sales Count", ROW[1],  ],
    ["(-)Tereminated Sales Count ", ROW[2] - ROW[1],],
    ["Stage I Sales Count ", ROW[2],],
    ["Stage II Commission ","{:.2f}".format(float(ROW[3])),],
    ["(-)Stage I Paid Commission ", "{:.2f}".format(float(ROW[4])) ,],
    ["Payable Commission ", "{:.2f}".format(float(ROW[5])) ,],
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
        ["Sales Channel :", "Talentfort", "","Month :", InvDate ],
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
docu = SimpleDocTemplate(TableName+"/STG2/Talentfort_"+TableName+"_STG2.pdf", pagesize=A4 ,rightMargin=0.5*inch,leftMargin=0.5*inch,
                            topMargin=1*inch,bottomMargin=15)

docu.build([title, subtitle,table1, table,table2, Indenter(right=1.5*inch)] )


