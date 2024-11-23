import logging
import sys

import smpplib.gsm
import smpplib.client
import smpplib.consts

# if you want to know what's happening
from smpplib.command import SubmitSMResp, SubmitSM

logging.basicConfig(level='DEBUG')

# Two parts, GSM default / UCS2, SMS with UDH
parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(u'Hello World €$£')

client = smpplib.client.Client('10.68.198.100', 5019)

# Print when obtain message_id
client.set_message_sent_handler(
    lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))

# Handle delivery receipts (and any MO SMS)
def handle_deliver_sm(pdu):
    sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id))
    return 0 # cmd status for deliver_sm_resp

client.set_message_received_handler(lambda pdu: handle_deliver_sm(pdu))

client.connect()
client.bind_transceiver(system_id='oss', password='MabL@z8/')


for part in parts:
    pdu = client.send_message(
        source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
        source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
        # Make sure it is a byte string, not unicode:
        source_addr='SLTMOBITEL',

        dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
        dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        # Make sure these two params are byte strings, not unicode:
        destination_addr='0710959907',
        short_message=part,

        data_coding=encoding_flag,
        esm_class=msg_type_flag,
        registered_delivery=True,
    )
    print(pdu.sequence)
    print(pdu.status)
    print(pdu.sm_length)


# Enters a loop, waiting for incoming PDUs
client.listen()
client.disconnect()

#=================================================================

# import smpplib.client, smpplib.consts, smpplib.gsm
# # SMSC Connection Details
# SMSC_IP = "xxx.xxx.xxx.xxx"
# SMSC_PORT = xxxx
# SYSTEM_ID = "username"
# SYSTEM_PASS = "password"
# SENDER_ID = "InstaCodeBlog"
# RECEIVER_NO = xxxxxxxxxx
# MESSAGE = "Test Message from InstaCodeBlog"
# # Converting message into parts
# parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(MESSAGE)
# # Connect to the remote SMSC gateway
# client = smpplib.client.Client(SMSC_IP, SMSC_PORT)
# client.connect()
# # Bind to the SMSC with the credentail
# client.bind_transceiver(system_id=SYSTEM_ID, password=SYSTEM_PASS)
# # Getting the message from parts and sending it
# for part in parts:
#     client.send_message(
#         source_addr_ton=smpplib.consts.SMPP_TON_INTL,
#         source_addr = SENDER_ID,
#         dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
#         destination_addr = RECEIVER_NO,
#         short_message = part,
#
#         data_coding = encoding_flag,
#         esm_class = msg_type_flag,
#         registered_delivery = True,
#     )
# client.unbind()
# client.disconnect()

# import smpplib
# import settings
#
# client = None
# try:
#     client = smpplib.client.Client(settings.SMS_SYSTEM_HOSTNAME, settings.SMS_SYSTEM_PORT)
#     client.connect()
#     try:
#         client.bind_transmitter(system_id=settings.SMS_SYSTEM_ID, password=settings.SMS_SYSTEM_PASSWORD)
#
#         client.send_message(source_addr_ton=smpplib.consts.SMPP_TON_INTL,
#                             source_addr='9535134654',
#                             dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
#                             destination_addr='9535134654',
#                             short_message='test Message`')
#     finally:
#         #print "==client.state====", client.state
#         if client.state in [smpplib.consts.SMPP_CLIENT_STATE_BOUND_TX]:
#             #if bound to transmitter
#             try:
#                 client.unbind()
#             except smpplib.exceptions.UnknownCommandError as ex:
#                 #https://github.com/podshumok/python-smpplib/issues/2
#                 try:
#                     client.unbind()
#                 except smpplib.exceptions.PDUError as ex:
#                     pass
# finally:
#     if client:
#         #print "==client.state====", client.state
#         client.disconnect()
#         #print "==client.state====", client.state



#====================================================
# import logging
# import sys
# import datetime
#
# import smpplib.gsm
# import smpplib.client
# import smpplib.consts
#
#
# # if you want to know what's happening
#
# logging.basicConfig(filename='sms_smpp.log', filemode='w', level='DEBUG')
#
# # Two parts, UCS2, SMS with UDH
# parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts('testing..........')
# client = smpplib.client.Client('10.68.198.100', 5019)
#
# # Print when obtain message_id
# client.set_message_sent_handler(
#     lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
# client.set_message_received_handler(
#     lambda pdu: sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id)))
#
# client.connect()
# client.bind_transceiver(system_id='oss', password='MabL@z8/')
#
#
# for part in parts:
#     pdu = client.send_message(
#         source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
#         source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
#         # Make sure it is a byte string, not unicode:
#         source_addr='SLTMOBITEL',
#
#         dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
#         dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
#         # Make sure these two params are byte strings, not unicode:
#         destination_addr='0710959907',
#         short_message=part,
#
#         data_coding=encoding_flag,
#         esm_class=msg_type_flag,
#         registered_delivery=True,
#     )
#     print(pdu.sequence)
#
# client.unbind()
# print('Unbind Done')
# client.disconnect()
# print('Disconnected')
# print('Sms sent on: ' + str(datetime.datetime.now()))

#=============================================================
