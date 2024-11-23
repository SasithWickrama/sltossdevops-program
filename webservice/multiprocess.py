import multiprocessing
import time
import db

# Process class
# class Process(multiprocessing.Process):
#     def __init__(self, id):
#         super(Process, self).__init__()
#         self.id = id
#
#     def run(self):
#         time.sleep(1)
#
#         conn = db.DbConnection.dbconn(self="")
#         c = conn.cursor()
#         sql = 'select LEA_CODE,RTOM_CODE from SLT_AREA WHERE MOD(DBMS_ROWID.ROWID_ROW_NUMBER(SLT_AREA.ROWID), 4) = ' + str(
#             self.id)
#         c.execute(sql)
#         # row = c.fetchall()
#
#         for row in c:
#
#             lea,rtom = row
#             sql = "insert into AA_PY(TNAME,ID) values(:tname,:pid)"
#             try:
#                     # create a cursor
#                     with conn.cursor() as cursor:
#                         cursor.execute(sql, [lea, self.id])
#                         # cursor.execute(sql)
#                         conn.commit()
#             except conn.Error as error:
#                 print('Error occurred:' + str(error))
#
#
#             print("Process ID : " + str(self.id))
#             print("I'm the process with id: {}".format(lea))
#             print("===============\n")
#
#
# if __name__ == '__main__':
#     starttime = time.time()
#     p = Process(0)
#
#     # Create a new process and invoke the
#     # Process.run() method
#     p.start()
#
#     # Process.join() to wait for task completion.
#     p.join()
#     p = Process(1)
#     p.start()
#     p.join()
#
#     p = Process(2)
#     p.start()
#     p.join()
#
#     p = Process(3)
#     p.start()
#     p.join()
#
#
#     print('P1111 That took {} seconds'.format(time.time() - starttime))


def multiprocessing_func(x):
        conn = db.DbConnection.dbconn(self="")
        c = conn.cursor()
        sql = 'select LEA_CODE,RTOM_CODE from SLT_AREA WHERE MOD(DBMS_ROWID.ROWID_ROW_NUMBER(SLT_AREA.ROWID), 10) = ' + str(
            x)
        c.execute(sql)
        # row = c.fetchall()

        for row in c:

            lea,rtom = row
            sql = "insert into AA_PY(TNAME,ID) values(:tname,:pid)"
            try:
                    # create a cursor
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [lea, x])
                        # cursor.execute(sql)
                        conn.commit()
            except conn.Error as error:
                print('Error occurred:' + str(error))


            print("Process ID : " + str(x))
            print("I'm the process with id: {}".format(lea))
            print("===============\n")

if __name__ == '__main__':
    starttime = time.time()
    processes = []
    for i in range(0,10):
        p = multiprocessing.Process(target=multiprocessing_func, args=(i,))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print('That took {} seconds'.format(time.time() - starttime))
