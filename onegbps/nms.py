import subprocess

import db
from zte import Ztedelete, Ztecreate
from log import getLogger


class Ims:

    def deleteImsAts(self):
        loggerIms = getLogger(self['PENO'] + '_IMS', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        imsresult = subprocess.run(['java', '-jar', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\SLTIMSgui.jar', 'DELATS', '2','tpno#'+self['TPNO'],'source#'+self['SOURCE']], capture_output=True)
        #imsresult = '0#SUCCESS'
        loggerIms.info(self["REF_ID"]+"  " + "command xml : IMS DELATS ")
        loggerIms.info(self["REF_ID"]+"  " + imsresult.stdout.decode())

        if imsresult.stdout.decode().split('#')[0] == '0':
        #if imsresult.split('#')[0] == '0':
            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=14, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                with conn.cursor() as cursor:
                    cursor.execute(sql,[imsresult.stdout.decode().split('#')[1],self['REC_ID'], self['PENO']])
                    conn.commit()
            except conn.Error as error:
                loggerIms.error(self["REF_ID"]+"  DB Error: " + str(error))
            return 0
        else:
            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "update ONEG_NEWCCT_DETAILS set  CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                with conn.cursor() as cursor:
                    cursor.execute(sql, [imsresult.stdout.decode().split('#')[1],self['REC_ID'], self['PENO']])
                    conn.commit()
            except conn.Error as error:
                #print('DB Error:' + str(error))
                loggerIms.error(self["REF_ID"]+"  DB Error: " + str(error))
            return 1

    def deleteUdrHss(self):
        loggerUdr = getLogger(self['PENO'] + '_IMS', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        udrhssresult = subprocess.run(['java', '-jar', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\SLTUdrGui.jar', 'UDR_DEL_HSS', '1','tpno#'+self['TPNO']], capture_output=True)
        #udrhssresult  = '0#SUCCESS'
        loggerUdr.info(self["REF_ID"]+"  " + "command xml : UDR DELHSS ")
        loggerUdr.info(self["REF_ID"]+"  " + udrhssresult.stdout.decode())

        if udrhssresult.stdout.decode().split('#')[0] == '0':
        #if udrhssresult.split('#')[0] == '0':
            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=15, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                with conn.cursor() as cursor:
                    cursor.execute(sql,[udrhssresult.stdout.decode().split('#')[1],self['REC_ID'], self['PENO']])
                    conn.commit()
            except conn.Error as error:
                loggerUdr.error(self["REF_ID"]+"  DB Error: " + str(error))
            return 0
        else:
            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "update ONEG_NEWCCT_DETAILS set  CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                with conn.cursor() as cursor:
                    cursor.execute(sql, [udrhssresult.stdout.decode().split('#')[1],self['REC_ID'], self['PENO']])
                    conn.commit()
            except conn.Error as error:
                #print('DB Error:' + str(error))
                loggerUdr.error(self["REF_ID"]+"  DB Error: " + str(error))
            return 1

    def deleteUdrEns(self):
        loggerUdr = getLogger(self['PENO'] + '_IMS', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        udrensresult = subprocess.run(['java', '-jar', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\SLTUdrGui.jar', 'DELENS', '1','tpno#'+self['TPNO']], capture_output=True)
        #udrensresult = '0#SUCCESS'
        loggerUdr.info(self["REF_ID"]+"  " + "command xml : UDR DELENS ")
        loggerUdr.info(self["REF_ID"]+"  " + udrensresult.stdout.decode())

        if udrensresult.stdout.decode().split('#')[0] == '0':
        #if udrensresult.split('#')[0] == '0':
            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=16, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                with conn.cursor() as cursor:
                    cursor.execute(sql,[udrensresult.stdout.decode().split('#')[1],self['REC_ID'], self['PENO']])
                    conn.commit()
            except conn.Error as error:
                loggerUdr.error(self["REF_ID"]+"  DB Error: " + str(error))
            return 0
        else:
            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "update ONEG_NEWCCT_DETAILS set  CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                with conn.cursor() as cursor:
                    cursor.execute(sql, [udrensresult.stdout.decode().split('#')[1],self['REC_ID'], self['PENO']])
                    conn.commit()
            except conn.Error as error:
                #print('DB Error:' + str(error))
                loggerUdr.error(self["REF_ID"]+"  DB Error: " + str(error))
            return 1

    def deleteMsan(self):
        loggerUdr = getLogger(self['PENO'] + '_IMS', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        msandelresult = subprocess.run(['java', '-jar', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\SLTUdrGui.jar', 'MSAN_SCR_DEL', '5','MSAN_TYPE#ZTE','ONT_PORT#1','FTTH_ZTE_PID#'+self['FTTH_ZTE_PID'],'FTTH_HUW_VP#'+self['FTTH_HUW_VP'],'ADSL_ZTE_DNAME#'+self['ADSL_ZTE_DNAME']], capture_output=True)
        #msandelresult = '0#SUCCESS'
        loggerUdr.info(self["REF_ID"]+"  " + "command xml : MSAN DELETE ")
        loggerUdr.info(self["REF_ID"]+"  " + msandelresult.stdout.decode())

        if msandelresult.stdout.decode().split('#')[0] == '0':
        #if msandelresult.split('#')[0] == '0':
            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=25, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                with conn.cursor() as cursor:
                    cursor.execute(sql,[msandelresult.stdout.decode().split('#')[1],self['REC_ID'], self['PENO']])
                    conn.commit()
            except conn.Error as error:
                loggerUdr.error(self["REF_ID"]+"  DB Error: " + str(error))
            return 0
        else:
            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "update ONEG_NEWCCT_DETAILS set  CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                with conn.cursor() as cursor:
                    cursor.execute(sql, [msandelresult.stdout.decode().split('#')[1],self['REC_ID'], self['PENO']])
                    conn.commit()
            except conn.Error as error:
                #print('DB Error:' + str(error))
                loggerUdr.error(self["REF_ID"]+"  DB Error: " + str(error))
            return 1

    def createUdrHss(self):
        loggerUdr = getLogger(self['PENO'] + '_IMS', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        resultudrhss = subprocess.run(['java', '-jar', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\SLTUdrGui.jar', 'UDR_ADDFTTH_HSS', '6','tpno#'+self['TPNO'],'MSAN_TYPE#ZTE','ONT_PORT#'+self['ONTPORT'],'FTTH_ZTE_PID#'+self['FTTH_ZTE_PID'],'FTTH_HUW_VP#'+self['FTTH_HUW_VP'],'ADSL_ZTE_DNAME#'+self['ADSL_ZTE_DNAME']], capture_output=True)
        #resultudrhss = '0#SUCCESS'
        loggerUdr.info(self["REF_ID"]+"  " + "command xml : UDR ADDHSS ")
        loggerUdr.info(self["REF_ID"]+"  " + resultudrhss.stdout.decode())

        if resultudrhss.stdout.decode().split('#')[0] == '0':
        #if resultudrhss.split('#')[0] == '0':
            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=17, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                with conn.cursor() as cursor:
                    cursor.execute(sql,[resultudrhss.stdout.decode().split('#')[1],self['REC_ID'], self['PENO']])
                    conn.commit()
            except conn.Error as error:
                loggerUdr.error(self["REF_ID"]+"  DB Error: " + str(error))
            return 0
        else:
            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "update ONEG_NEWCCT_DETAILS set  CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                with conn.cursor() as cursor:
                    cursor.execute(sql, [resultudrhss.stdout.decode().split('#')[1],self['REC_ID'], self['PENO']])
                    conn.commit()
            except conn.Error as error:
                #print('DB Error:' + str(error))
                loggerUdr.error(self["REF_ID"]+"  DB Error: " + str(error))
            return 1

    def createUdrEns(self):
        loggerUdr = getLogger(self['PENO'] + '_IMS', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        resultudrens = subprocess.run(['java', '-jar', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\SLTUdrGui.jar', 'ADDENS', '1','tpno#'+self['TPNO']], capture_output=True)
        #resultudrens = '0#SUCCESS'
        loggerUdr.info(self["REF_ID"]+"  " + "command xml : UDR ADDENS ")
        loggerUdr.info(self["REF_ID"]+"  " + resultudrens.stdout.decode())

        if resultudrens.stdout.decode().split('#')[0] == '0':
        #if resultudrens.split('#')[0] == '0':
            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=18, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                with conn.cursor() as cursor:
                    cursor.execute(sql,[resultudrens.stdout.decode().split('#')[1],self['REC_ID'], self['PENO']])
                    conn.commit()
            except conn.Error as error:
                loggerUdr.error(self["REF_ID"]+"  DB Error: " + str(error))
            return 0
        else:
            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "update ONEG_NEWCCT_DETAILS set  CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                with conn.cursor() as cursor:
                    cursor.execute(sql, [resultudrens.stdout.decode().split('#')[1],self['REC_ID'], self['PENO']])
                    conn.commit()
            except conn.Error as error:
                #print('DB Error:' + str(error))
                loggerUdr.error(self["REF_ID"]+"  DB Error: " + str(error))
            return 1

    def createImsAts(self):
        loggerUdr = getLogger(self['PENO'] + '_IMS', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        resultimsats = subprocess.run(['java', '-jar', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\SLTIMSgui.jar', 'ADDATS', '2','tpno#'+self['TPNO'],'source#'+self['SOURCE']], capture_output=True)
        #resultimsats = '0#SUCCESS'
        loggerUdr.info(self["REF_ID"]+"  " + "command xml : IMS ADDATS ")
        loggerUdr.info(self["REF_ID"]+"  " + resultimsats.stdout.decode())

        if resultimsats.stdout.decode().split('#')[0] == '0':
        #if resultimsats.split('#')[0] == '0':
            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=19, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                with conn.cursor() as cursor:
                    cursor.execute(sql,[resultimsats.stdout.decode().split('#')[1],self['REC_ID'], self['PENO']])
                    conn.commit()
            except conn.Error as error:
                loggerUdr.error(self["REF_ID"]+"  DB Error: " + str(error))
            return 0
        else:
            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "update ONEG_NEWCCT_DETAILS set  CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                with conn.cursor() as cursor:
                    cursor.execute(sql, [resultimsats.stdout.decode().split('#')[1],self['REC_ID'], self['PENO']])
                    conn.commit()
            except conn.Error as error:
                #print('DB Error:' + str(error))
                loggerUdr.error(self["REF_ID"]+"  DB Error: " + str(error))
            return 1


class Zte:
    def deleteUser(self):
        logger = getLogger(self['PENO'] + '_prov', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        try:
            result = Ztedelete.zteDelete(self)
            #result = '0#SUCCESS'

            if result.split('#')[0] == '0':
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=1, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()

                    sql2 = "update ONEG_OLDCCT_DETAILS set CCT_STATUS=1, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor2:
                        cursor2.execute(sql2, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 0
            else:
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql2 = "update ONEG_OLDCCT_DETAILS set CCT_STATUS=1, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor2:
                        cursor2.execute(sql2, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 1

        except Exception as e:
            logger.error(self["REF_ID"]+"  DB Error: " + str(e))
            return 1

    def createFab(self):
        logger = getLogger(self['PENO'] + '_prov', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        try:
            result = Ztecreate.zteCreate('FTTH_ZTEADD_ONU.xml', self)
            #result = '0#SUCCESS'
            if result.split('#')[0] == '0':
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=2, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 0
            else:
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 1

        except Exception as e:
            logger.error(self["REF_ID"]+"  DB Error: " + str(e))
            return 1

    def createProfile(self,cmd ):
        logger = getLogger(self['PENO'] + '_prov', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        try:
            result = Ztecreate.zteCreate(cmd, self)
            #result = '0#SUCCESS'

            if result.split('#')[0] == '0':
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=3, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 0
            else:
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set  CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 1

        except Exception as e:
            logger.error(self["REF_ID"]+"  DB Error: " + str(e))
            return 1

    def createVoice(self):
        logger = getLogger(self['PENO'] + '_prov', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        try:
            result = Ztecreate.zteCreate('FTTH_VSER_PORT.xml', self)
            #result = '0#SUCCESS'

            if result.split('#')[0] == '0':
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=4, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 0
            else:
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 1

        except Exception as e:
            logger.error(self["REF_ID"]+"  DB Error: " + str(e))
            return 1

    def createBroadband(self):
        logger = getLogger(self['PENO'] + '_prov', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        try:
            result = Ztecreate.zteCreate('FTH_ISER_POT.xml', self)
            #result = '0#SUCCESS'

            if result.split('#')[0] == '0':
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=5, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 0
            else:
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 1

        except Exception as e:
            logger.error(self["REF_ID"]+"  DB Error: " + str(e))
            return 1

    def createBroadbandUser(self):
        logger = getLogger(self['PENO'] + '_prov', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        try:
            result = Ztecreate.zteCreate('FTTH_INT_USRADD.xml', self)
            #result = '0#SUCCESS'

            if result.split('#')[0] == '0':
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=6, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 0
            else:
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 1

        except Exception as e:
            logger.error(self["REF_ID"]+"  DB Error: " + str(e))
            return 1

    def createIptv(self):
        logger = getLogger(self['PENO'] + '_prov', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        try:
            result = Ztecreate.zteCreate('FTTH_PSER_PORT.xml', self)
            #result = '0#SUCCESS'

            if result.split('#')[0] == '0':
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=7, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 0
            else:
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 1

        except Exception as e:
            logger.error(self["REF_ID"]+"  DB Error: " + str(e))
            return 1

    def createIptvSerA(self):
        logger = getLogger(self['PENO'] + '_prov', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        try:
            result = Ztecreate.zteCreate('FTTH_ZTE_IPTVSERA.xml', self)
            #result = '0#SUCCESS'

            if result.split('#')[0] == '0':
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=8, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 0
            else:
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 1

        except Exception as e:
            logger.error(self["REF_ID"]+"  DB Error: " + str(e))
            return 1

    def createIptvSerB(self):
        logger = getLogger(self['PENO'] + '_prov', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        try:
            result = Ztecreate.zteCreate('FTTH_ZTE_IPTVSERB.xml', self)
            #result = '0#SUCCESS'

            if result.split('#')[0] == '0':
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=9, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 0
            else:
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 1

        except Exception as e:
            logger.error(self["REF_ID"]+"  DB Error: " + str(e))
            return 1

    def createIptvSerC(self):
        logger = getLogger(self['PENO'] + '_prov', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        try:
            result = Ztecreate.zteCreate('FTTH_ZTE_IPTVSERC.xml', self)
            #result = '0#SUCCESS'

            if result.split('#')[0] == '0':
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=10, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 0
            else:
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 1

        except Exception as e:
            logger.error(self["REF_ID"]+"  DB Error: " + str(e))
            return 1

    def createIptvSerD(self):
        logger = getLogger(self['PENO'] + '_prov', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        try:
            result = Ztecreate.zteCreate('FTTH_ZTE_IPTVSERD.xml', self)
            #result = '0#SUCCESS'

            if result.split('#')[0] == '0':
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=11, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 0
            else:
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 1

        except Exception as e:
            logger.error(self["REF_ID"]+"  DB Error: " + str(e))
            return 1

    def createIptv2(self):
        logger = getLogger(self['PENO'] + '_prov', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        try:
            result = Ztecreate.zteCreate('FTTH_ZTE_IPTV2.xml', self)
            #result = '0#SUCCESS'

            if result.split('#')[0] == '0':
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=12, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 0
            else:
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 1

        except Exception as e:
            logger.error(self["REF_ID"]+"  DB Error: " + str(e))
            return 1

    def createIptv3(self):
        logger = getLogger(self['PENO'] + '_prov', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + self['PENO'])

        try:
            result = Ztecreate.zteCreate('FTTH_ZTE_IPTV3.xml', self)
            #result = '0#SUCCESS'

            if result.split('#')[0] == '0':
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_STATUS=12, CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 0
            else:
                try:
                    conn = db.DbConnection.dbconnOssRpt(self="")
                    sql = "update ONEG_NEWCCT_DETAILS set CCT_MESSAGE= :CCT_MESSAGE where  REC_ID= :REC_ID and PE_NO= :PE_NO"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, [result.split('#')[1],self['REC_ID'], self['PENO']])
                        conn.commit()
                except conn.Error as error:
                    logger.error(self["REF_ID"]+"  DB Error: " + str(error))
                return 1

        except Exception as e:
            logger.error(self["REF_ID"]+"  DB Error: " + str(e))
            return 1

class Huawei:
    def deleteUser(self):
        return 0


class Nokia:
    def deleteUser(self):
        return 0

