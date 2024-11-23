import db

conn = db.DbConnection.dbconnHadwh("")


class Initiate:
    def initiateTask(self):
        totTime = 0
        endTime = 0

        try:
            sql = "select distinct PROS_SVTYPE,PROS_TYPE,PROS_STATUS  from  PROJECTS where PROS_ID=:PROS_ID"
            c = conn.cursor()
            c.execute(sql, [self])

            for row in c:
                PROS_SVTYPE, PROS_TYPE, PROS_STATUS = row
                print(PROS_SVTYPE, PROS_TYPE, PROS_STATUS)

            sqltask = "select distinct *  from  TASK_LIST where TASKSVTYPE=:TASKSVTYPE and " \
                      "TASKPROJECTTYPE=:TASKPROJECTTYPE order by TASKORDER"
            c2 = conn.cursor()
            c2.execute(sqltask, [PROS_SVTYPE, PROS_TYPE])

            for rowtask in c2:
                endTime += int(rowtask[13])

                sqltaskinsert = "INSERT INTO LUNOX.PROJECT_TASKS  VALUES ( :PID, 100, :TASKNAME,sysdate, sysdate + interval '" + str(
                    totTime) + "' minute,sysdate + interval '" + str(
                    endTime) + "' minute,:STAT,sysdate,:UPFATEUSER,:TASKID,:WG,:DISPLAYORDER,:TASKTYPE)"
                with conn.cursor() as cursor:
                    cursor.execute(sqltaskinsert,
                                   [self, rowtask[1], 'ASSIGNED', 'SYS', rowtask[0], rowtask[9], rowtask[6],
                                    rowtask[2]])
                conn.commit()
                print(cursor.rowcount)
                totTime += int(rowtask[13])

            sqlatt = "select distinct *  from  ATTRIBUTE_LIST where ATTSVTYPE=:ATTSVTYPE and " \
                     "ATTPROJECTTYPE=:ATTPROJECTTYPE order by ATTDISPLAYORDER"
            c3 = conn.cursor()
            c3.execute(sqlatt, [PROS_SVTYPE, PROS_TYPE])

            for rowatt in c3:
                sqlattinsert = "INSERT INTO LUNOX.PROJECT_ATTRIBUTES VALUES ( :PID, 100, :ATTNAME,:DEFAULTVALUE,:OLDVALUE ,sysdate,:UPDATEBY,:ATTID,:DISPLAYORDER)"
                with conn.cursor() as cursor:
                    cursor.execute(sqlattinsert, [self, rowatt[1], '', '', 'SYS', rowatt[0], rowatt[5]])
                conn.commit()
                print(cursor.rowcount)

            return 'success'

        except Exception as e:
            return str(e)
