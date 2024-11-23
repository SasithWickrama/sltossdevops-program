import multiprocessing
import random
import sys
import time
import db
import subprocess
from log import getLogger
from zte import ZteGetSn, Ztecreate
from nms import Zte,Huawei,Nokia,Ims


def specific_string(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    # define the condition for random string
    return ''.join((random.choice(sample_string)) for x in range(length))


def ogbps_getsn(x, pe):
    logger = getLogger(pe + '_sn', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + pe)

    try:
        conn = db.DbConnection.dbconnOssRpt(self="")
        c = conn.cursor()
        sql = "select REGID ,REC_ID from ONEG_OLDCCT_DETAILS where  PE_NO = :PE_NO " \
              "and ONT_SN is not null and REGID is not null   " \
              "AND MOD(DBMS_ROWID.ROWID_ROW_NUMBER(ONEG_OLDCCT_DETAILS.ROWID), 10) = " + str(x)

        c.execute(sql, [pe])

        for row in c:
            REGID, REC_ID = row
            print(REGID, x)
            refid = specific_string(10)
            ref = refid + '_' + REGID

            data = {}
            data['ZTE_NMS_REGID'] = '94' + str(REGID)[1:10]
            data['REF_ID'] = str(ref)
            data['PENO'] = str(pe)

            resultsn = ZteGetSn.zteGetSn('FTTH_ZTEGET_SN.xml', data)
            logger.info(ref + "  " + str(resultsn['SN']))

            try:
                conn = db.DbConnection.dbconnOssRpt(self="")
                sql = "insert into  ONEG_NMS_SN values (:REC_ID,:NMS_SN,sysdate,:PE_NO )"
                with conn.cursor() as cursor:
                    cursor.execute(sql, [REC_ID, resultsn['SN'], pe])
                    conn.commit()
            except conn.Error as error:
                # print('DB Error:' + str(error))
                logger.error(ref + "  DB Error: " + str(error))

    except conn.Error as error:
        logger.error(ref + "  DB Error: " + str(error))


def ogbps_transfer(x, pe):
    logger = getLogger(pe + '_prov', 'F:\\xampp\\htdocs\\IMS\\dbFunction\\ONEGBPS\\logs\\' + pe)
    #logger = getLogger(pe + '_prov', 'logs/' + pe)
    refid = specific_string(10)

    try:
        conn = db.DbConnection.dbconnOssRpt(self="")
        c = conn.cursor()
        sql = "select MSAN_TYPE,DNAME,ONT_SN,ZTE_PORT,HUAWEI_PORT,NOKIA_PORT,V_PORT,REGID,BB_CIRCUIT,IPTV_COUNT,SPEED," \
              "ZTE_PROFILE,REC_ID from ONEG_OLDCCT_DETAILS where  PE_NO = :PE_NO and CCT_STATUS=:CCT_STATUS" \
              " and ONT_SN is not null and REGID is not null   " \
              "AND MOD(DBMS_ROWID.ROWID_ROW_NUMBER(ONEG_OLDCCT_DETAILS.ROWID), 10) = " + str(x)
        c.execute(sql, [pe, '0'])

        for row in c:
            time.sleep(2)
            MSAN_TYPE, DNAME, ONT_SN, ZTE_PORT, HUAWEI_PORT, NOKIA_PORT, V_PORT, REGID, BB_CIRCUIT, IPTV_COUNT, SPEED, ZTE_PROFILE, REC_ID = row
            print(MSAN_TYPE, ONT_SN, ZTE_PORT, IPTV_COUNT)

            sql = "select distinct ZTE_PORT,HUAWEI_PORT,NOKIA_PORT,V_PORT,REGID,DNAME,SPEED,ZTE_PROFILE,VOICE_NO" \
                  ",VOICE_NO2,VTYPE1,VTYPE2,REC_ID from ONEG_NEWCCT_DETAILS " \
                  "where PE_NO= :PE_NO  and ONT_SN= :ONT_SN and REGID= :REGID and CCT_STATUS=:CCT_STATUS"
            with conn.cursor() as cursor:
                cursor.execute(sql, [pe, ONT_SN, REGID,'0'])
                #cursor.execute(sql, [pe, 'ZTEGCB182EC1', REGID, '0'])
                credata = cursor.fetchone()

            ref = refid + '_' + REGID
            datadel = {}
            data = {}
            if BB_CIRCUIT is None:
                BB_CIRCUIT=''

            datadel['ADSL_ZTE_DNAME'] = DNAME
            datadel['FTTH_ONT_SN'] = ONT_SN
            datadel['FTTH_ZTE_PID'] = ZTE_PORT
            datadel['REF_ID'] = str(ref)
            datadel['PENO'] = str(pe)
            datadel['REC_ID'] = str(REC_ID)
            datadel['TPNO'] = str(REGID)[1:10]
            datadel['SOURCE'] = str(REGID)[1:2]
            datadel['FTTH_HUW_VP'] = str(V_PORT)

            data['ADSL_ZTE_DNAME'] = str(credata[5])
            data['FTTH_ZTE_PID'] = credata[0]
            data['FTTH_ONT_SN'] = ONT_SN
            #data['FTTH_ONT_SN'] = 'ZTEGCB182EC1'
            data['FTTH_HUW_VP'] = str(credata[3])
            data['ZTE_NMS_REGID'] = '94'+str(credata[4])[1:10]
            data['FTTH_ZTE_PROFILE'] = str(credata[7])
            data['REF_ID'] = str(ref)
            data['PENO'] = str(pe)
            data['ADSL_ZTE_USERNAME'] = BB_CIRCUIT
            data['REC_ID'] = str(credata[12])
            data['TPNO'] = str(credata[4])[1:10]
            data['SOURCE'] = str(credata[4])[1:3]
            data['ONTPORT'] = str(credata[10])

            print(data)

            if MSAN_TYPE == 'ZTE':
                data['ZTE_ONUTYPE'] = 'ZTE-F660'
                data['FTTH_INTERNET_PKG'] = '100M'

                #GET VLAN
                resultvlan = Ztecreate.zteVlan('lst_vlan.xml', data, 'VOBB', '')
                logger.info(ref+"  " + "command xml : lst_vlan.xml - VOICE")
                logger.info(ref+"  " + str(resultvlan))
                data.update(resultvlan)

                if BB_CIRCUIT != '':
                    resultvlanbb = Ztecreate.zteVlan('lst_vlan.xml', data, 'Entree', 'SVLAN')
                    logger.info(ref+"  " + "command xml : lst_vlan.xml - BB")
                    logger.info(ref+"  " + str(resultvlanbb))
                    data.update(resultvlanbb)

                if IPTV_COUNT != '0':
                    resultvlanpeo = Ztecreate.zteVlan('lst_vlan.xml', data, 'IPTV_SVLAN', 'IPTV')
                    logger.info(ref+"  " + "command xml : lst_vlan.xml - IPTV")
                    logger.info(ref+"  " + str(resultvlanpeo))
                    data.update(resultvlanpeo)


                #DELETE IMS UDR
                resultdeleteIms= Ims.deleteImsAts(datadel)
                logger.info(ref+"  " + "command xml : DELETE IMS")
                logger.info(ref+"  " + str(resultdeleteIms))

                if resultdeleteIms == 0:
                    resultdeleteHss= Ims.deleteUdrHss(datadel)
                    logger.info(ref+"  " + "command xml : DELETE HSS")
                    logger.info(ref+"  " + str(resultdeleteHss))

                    if resultdeleteHss == 0:
                        resultdeleteEns= Ims.deleteUdrEns(datadel)
                        logger.info(ref+"  " + "command xml : DELETE ENS")
                        logger.info(ref+"  " + str(resultdeleteEns))

                        if resultdeleteEns == 0:
                            resultdeleteMsan= Ims.deleteMsan(datadel)
                            logger.info(ref+"  " + "command xml : DELETE MSAN")
                            logger.info(ref+"  " + str(resultdeleteMsan))

                #DELETE
                resultdelete= Zte.deleteUser(datadel)
                logger.info(ref+"  " + "command xml : DELETE NMS")
                logger.info(ref+"  " + str(resultdelete))

                if resultdelete == 0:
                    #FAB CREATE
                    resultfab= Zte.createFab(data)
                    logger.info(ref+"  " + "command xml : FAB CREATE")
                    logger.info(ref+"  " + str(resultfab))

                    if resultfab == 0:
                        time.sleep(2)
                        #PROFILE CREATE
                        if credata[7] == 'DOUBLEPLAY_VOICE_IPTV':
                            command = 'FTTH_ZTEX_BIDPIPTV.xml'
                        elif credata[7] == 'TRIPLEPLAY_MULTYIIPTV':
                            command = 'FTTH_ZTEX_MIPTV.xml'
                        else:
                            command = 'FTTH_ZTEX_BIDP.xml'

                        resultprof = Zte.createProfile(data,command )
                        logger.info(ref+"  " + "command xml : PROFILE CREATE")
                        logger.info(ref+"  " + str(resultprof))

                        if resultprof == 0:
                            time.sleep(2)
                            #VOICE CREATE
                            resultvoice= Zte.createVoice(data)
                            logger.info(ref+"  " + "command xml : VOICE CREATE")
                            logger.info(ref+"  " + str(resultvoice))

                            if resultvoice == 0:
                                time.sleep(2)
                                if BB_CIRCUIT != '':
                                    #BROADBAND CREATE
                                    resultbb= Zte.createBroadband(data)
                                    logger.info(ref+"  " + "command xml : BB CREATE")
                                    logger.info(ref+"  " + str(resultbb))

                                    if resultbb == 0:
                                        time.sleep(2)
                                        #BROADBAND USER CREATE
                                        resultbbuser= Zte.createBroadbandUser(data)
                                        logger.info(ref+"  " + "command xml : BB USER CREATE")
                                        logger.info(ref+"  " + str(resultbbuser))

                                if IPTV_COUNT != '0':
                                    #IPTV PORT CREATE
                                    resultiptv= Zte.createIptv(data)
                                    logger.info(ref+"  " + "command xml : IPTV PORT CREATE")
                                    logger.info(ref+"  " + str(resultiptv))

                                    if resultiptv == 0:
                                        time.sleep(2)
                                        resultiptvA= Zte.createIptvSerA(data)
                                        logger.info(ref+"  " + "command xml : IPTV A CREATE")
                                        logger.info(ref+"  " + str(resultiptvA))

                                        if resultiptvA == 0:
                                            resultiptvB= Zte.createIptvSerB(data)
                                            logger.info(ref+"  " + "command xml : IPTV B CREATE")
                                            logger.info(ref+"  " + str(resultiptvB))

                                            if resultiptvB == 0:
                                                resultiptvC= Zte.createIptvSerC(data)
                                                logger.info(ref+"  " + "command xml : IPTV C CREATE")
                                                logger.info(ref+"  " + str(resultiptvC))

                                                if resultiptvC == 0:
                                                    resultiptvD= Zte.createIptvSerD(data)
                                                    logger.info(ref+"  " + "command xml : IPTV D CREATE")
                                                    logger.info(ref+"  " + str(resultiptvD))

                                                    if resultiptvD == 0:
                                                        if IPTV_COUNT == 2:
                                                            resultiptv2= Zte.createIptv2(data)
                                                            logger.info(ref+"  " + "command xml : IPTV 2 CREATE")
                                                            logger.info(ref+"  " + str(resultiptv2))

                                                        if IPTV_COUNT == 3:
                                                            resultiptv2= Zte.createIptv2(data)
                                                            logger.info(ref+"  " + "command xml : IPTV 2 CREATE")
                                                            logger.info(ref+"  " + str(resultiptv2))

                                                            resultiptv3= Zte.createIptv3(data)
                                                            logger.info(ref+"  " + "command xml : IPTV 3 CREATE")
                                                            logger.info(ref+"  " + str(resultiptv3))

                                #CREATE IMS UDR
                                resultcreateUdrHss= Ims.createUdrHss(data)
                                logger.info(ref + "  " + "command xml : CREATE HSS")
                                logger.info(ref+"  " + str(resultcreateUdrHss))
                                if resultcreateUdrHss == 0:
                                    resultcreateUdrEns= Ims.createUdrEns(data)
                                    logger.info(ref + "  " + "command xml : CREATE ENS")
                                    logger.info(ref + "  " + str(resultcreateUdrEns))
                                    if resultcreateUdrEns == 0:
                                        resultcreateImsAts= Ims.createImsAts(data)
                                        logger.info(ref + "  " + "command xml : CREATE ATS")
                                        logger.info(ref + "  " + str(resultcreateImsAts))


        try:
            conn = db.DbConnection.dbconnOssRpt(self="")
            sql = "update ONEG_PE_DETAILS set PE_STATUS= :PE_STATUS where   PE_NO= :PE_NO"
            with conn.cursor() as cursor:
                cursor.execute(sql, ['8', pe])
                conn.commit()
        except conn.Error as error:
            #print('DB Error:' + str(error))
            logger.error(ref+"  DB Error: " + str(error))


    except conn.Error as error:
        logger.error(" " + str(error))


if __name__ == '__main__':
    pe = sys.argv[1]

    processes = []
    for i in range(0, 10):
        if sys.argv[2] == 'OGBPS_TRANF':
            p = multiprocessing.Process(target=ogbps_transfer, args=(i, pe))
        if sys.argv[2] == 'OGBPS_GETSN':
            p = multiprocessing.Process(target=ogbps_getsn, args=(i, pe))
        processes.append(p)
        p.start()
    # multiprocessing_func(i)
    for process in processes:
        process.join()
