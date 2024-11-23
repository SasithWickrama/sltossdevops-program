from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from db import DbConnection
from pathlib import Path
import math


conn = DbConnection.dbconn(self="")
c = conn.cursor()
cx = conn.cursor()

sql = "SELECT TO_CHAR(ADD_MONTHS(TRUNC(SYSDATE,'mm'),-1),'YYYYMM') TBNAME FROM DUAL";  
c.execute(sql)
for TBNAME in c:
    TableName = str(TBNAME[0])

#GET ACTIVE DELER TABLE
sql = "SELECT TABLE_NAME  FROM EX_SETTING WHERE DISCRIPTION = 'DEALER' AND END_DATE IS NULL";  
c.execute(sql)
for TABLE_NAME in c:
    DealerTableName = str(TABLE_NAME[0]) 


Path(TableName+"/PDF").mkdir(parents=True, exist_ok=True)

sql = "SELECT DEALER_NAME FROM "+DealerTableName+" WHERE DEALER_TYPE ='S'";  
c.execute(sql)
for DEALER_NAME in c:
    Dealer = str(DEALER_NAME[0])
    sqlx = "SELECT MEDIUM , COM_TYPE ||'-'||SERO_ORDT_TYPE XX , COM_STG1 , COUNT(EVENT_SOURCE) FROM SALES_"+TableName+"  WHERE ( SALES_CHANNEL1 = '"+Dealer+"' OR SALES_PERSON11 =  '"+Dealer+"') AND STATUS = 0 GROUP BY MEDIUM , COM_TYPE ||'-'||SERO_ORDT_TYPE,COM_STG1 ORDER BY MEDIUM , COM_TYPE ||'-'||SERO_ORDT_TYPE,COM_STG1"
    cx.execute(sqlx)

    canvas = canvas.Canvas(TableName+"/PDF/"+Dealer.replace(".", " ")+"_"+TableName+"_STG1.pdf", pagesize=letter)
    canvas.setLineWidth(.3)

    canvas.setFont('Helvetica', 14)
    canvas.drawString(30,700,'Dealer Commission System')

    canvas.setFont('Helvetica', 12)
    canvas.drawString(30,675,'Sales Summery - Stage 1')

    canvas.setFont('Helvetica', 10)
    canvas.drawString(30,640,'Sales Channel :')
    canvas.drawString(110,640,Dealer)
    canvas.drawString(30,610,'Sales Person :')
    canvas.drawString(470,640,'Month :')
    canvas.drawString(510,640,TableName)

    canvas.line(30,590,580,590)

    canvas.drawString(35,575,'Access Bearer')
    canvas.drawString(130,575,'Medium')
    canvas.drawString(200,575,'Total Count')
    canvas.drawString(280,575,'Commission Rate')
    canvas.drawString(380,575,'Total Commission')
    canvas.drawString(480,575,'Paybale Commssion')

    canvas.line(30,565,580,565)

    i =1
    x = 575
    for ROW in cx:
        canvas.drawString(35,x-(i*25),ROW[0])
        canvas.drawString(130,x-(i*25),ROW[1])
        canvas.drawString(200,x-(i*25),ROW[3])
        canvas.drawString(280,x-(i*25),ROW[2])
        canvas.drawString(380,x-(i*25),ROW[3]*ROW[2])
        canvas.drawString(480,x-(i*25),ROW[3]*ROW[2]/2)

        if math.fmod(i.encode('utf-8'), 20).encode('utf-8') == 0:
            canvas.showPage()
            canvas.setFont('Helvetica', 10)
            canvas.line(30,700,580,700)

            canvas.drawString(35,690,'Access Bearer')
            canvas.drawString(130,690,'Medium')
            canvas.drawString(200,690,'Total Count')
            canvas.drawString(280,690,'Commission Rate')
            canvas.drawString(380,690,'Total Commission')
            canvas.drawString(480,690,'Paybale Commssion')

            canvas.line(30,680,580,680)
            i = 0
            x=670

        i = i+1

    canvas.save()