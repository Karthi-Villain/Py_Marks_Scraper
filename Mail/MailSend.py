import smtplib
from email.message import EmailMessage
import datetime
import os
import logging
#--Mailing--
def SendMails(PrintResults,StudName,StudMail,Roll):
    logging.info('Mailing Started to '+StudMail)
    try:
        with smtplib.SMTP(os.getenv('MServer',default='smtp.office365.com'),os.getenv('MPort',default='587')) as smtp:
            logging.info('Mail Signed in with '+os.getenv('Mail'))
            smtp.starttls()
            smtp.login(os.getenv('Mail'),os.getenv('MPass'))
            MainMsg=EmailMessage()
            MainMsg['Subject']=f'{StudName}({Roll}) Your Results Are Here'
            MainMsg['From']=os.getenv('Mail')
            MainMsg['To']=StudMail
            
            MarksHtml=f"""\
                        <!DOCTYPE html>
                        <html>
                        <body>
                        {PrintResults}
                        <p style="text-align:center"><strong><a href="https://svcet.onrender.com/">Generate Easy And Faster Results</a></strong></p>
                        </body>
                        </html>
                        """
            MainMsg.add_alternative(MarksHtml,subtype='html')
            smtp.send_message(MainMsg)
            logging.info('Mailed Results to '+StudMail)
    except Exception as e:
        logging.debug(Roll+"Mailing Error: Please Check if Your Mail Limit Reached\n")
        logging.debug(e)
    else:
        logging.debug(Roll+" Mail Sent To:"+StudMail+" - "+str(datetime.datetime.now()))
