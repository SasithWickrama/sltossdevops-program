from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import re

import const
from log import Logger


logger = Logger.getLogger('email', 'logs/entmail')

def checkMail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return 0
    else:
        return 1


class SendMail:
        def sendMail(self, ref):
            to_addrs = self['mail']
            sub = self['subject']
            messagestr = self['msg']
            #messagestr = 'This is Test mail'

            try:
                message = MIMEMultipart('related')
                message['subject'] = sub
                message['from'] = const.from_addr
                message['to'] = to_addrs
                message.preamble = 'This is a multi-part message in MIME format.'

                msgAlternative = MIMEMultipart('alternative')
                message.attach(msgAlternative)

                msgText = MIMEText('This is the alternative plain text message.')
                msgAlternative.attach(msgText)

                # We reference the image in the IMG SRC attribute by the ID we give it below
                #msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
                msgText = MIMEText(messagestr, 'html')
                msgAlternative.attach(msgText)

                # This example assumes the image is in the current directory
                fp = open('mailsig.jpg', 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()

                # Define the image's ID as referenced above
                msgImage.add_header('Content-ID', '<image1>')
                message.attach(msgImage)

                server = smtplib.SMTP(const.smtp_ssl_host, const.smtp_ssl_port)

                if checkMail(to_addrs) == 0:
                    server.sendmail(const.from_addr, to_addrs, message.as_string())

                    logger.info(ref + str(self))
                    logger.info(ref + ' mail sent.....')

                    server.quit()

                    responsedata = {"result": "success", "msg": 'mail sent'}
                    return  responsedata


                else:
                    logger.info(ref + str(self))
                    logger.info(ref+' Invalid mail.....')

                    responsedata = {"result": "error", "msg": 'invalid mail'}
                    return  responsedata

            except Exception as e:
                logger.info(ref + str(e))

                responsedata = {"result": "error", "msg": str(e)}
                return  responsedata

