import smtplib
from email.message import EmailMessage
import datetime
import os
#--Mailing--
def SendMails(PrintResults,StudName,StudMail):
    try:
        with smtplib.SMTP(os.getenv('MServer',default='smtp.office365.com'),os.getenv('MPort',default='587')) as smtp:
            #print(datetime.datetime.now())
            smtp.starttls()
            smtp.login(os.getenv('Mail'),os.getenv('MPass'))
            MainMsg=EmailMessage()
            MainMsg['Subject']=f'{StudName} Your Results Are Here'
            MainMsg['From']=os.getenv('Mail')
            MainMsg['To']=StudMail
            
            MarksHtml=f"""\
                        <!DOCTYPE html>
                        <html>
                        <body>
                        {PrintResults}
                        &nbsp;</p>
                        <p style="text-align:center"><strong><a href="https://svcet.onrender.com/">Generate Easy And Faster Results</a></strong></p>
                        </body>
                        </html>
                        """
            MainMsg.add_alternative(MarksHtml,subtype='html')
            smtp.send_message(MainMsg)
    except Exception as e:
        print("Mailing Error: Please Check Your Mailor Limit Reached\n")
        print(e)
    else:
        print("Mail Sent To:"+StudMail+" - "+str(datetime.datetime.now()))
