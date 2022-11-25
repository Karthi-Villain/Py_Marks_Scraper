
'''
https://github.com/Karthi-Villain
Telegram - @I_AmKarthi
Don't Miss USe This Code
'''
#@title <b><center>SVCET Marks Scrapper</center></b>
import requests
from bs4 import BeautifulSoup
Url='https://svceta.org/BeesERP/Login.aspx?ReturnUrl=/BeesERP/'
#Enter You Roll Number, PassWord And Sem Below
Roll=""#@param {type:"string"}
Passwd=""#@param {type:"string"}
Sem=2#@param {type:"integer"} 
#Ex:- 1,2,3...8 int
Roll=Roll.upper()
fourm={
    "__LASTFOCUS":"",
    "__EVENTTARGET":"",
    "__EVENTARGUMENT":"",
    "__VIEWSTATE":"/wEPDwUKLTk1NzEzMjEyNWQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFDEltZ1VzZXJQaG90b6Y0cgLFn3Bx0z1CYV2nK6HA95DJ0iJRCNXNMDmBgHg5",
    "__VIEWSTATEGENERATOR": "9331F466",
    "__EVENTVALIDATION": "/wEdAAVjVyBLqiX1cxjkBW0I57t2lSfEvot8s98xACen5j++l9L5WsiImyZWZthxHYT/WpZjemWCTRgEB59HPczIGVNwgWOkgugWB5Cq9dYD7toQNOvpRVNtIoB52WCSDT2a3G5fv9JeSWAnZlfxpyP/oCEU",
    "txtUserName": Roll,
    "btnNext": "Next"
}
ErrorMessage=''
try:
    s=requests.Session()
    res=s.post(Url,data=fourm)
    b=BeautifulSoup(res.text,'html.parser')
    #print(b.find('span',id="lblWarning").text) 
    if(b.find('span',id="lblWarning").text!='User Name is Incorrect'):
        LoginKeys={}
        for raw in b.find('form').find_all('input'):
            try:
                LoginKeys[raw['id']]=raw['value']
            except:
                pass
        LoginKeys['txtPassword']=Passwd
    else:
        ErrorMessage='User Name is Incorrect'
    if(ErrorMessage==''):
        res2=s.post(Url,data=LoginKeys)
        b2=BeautifulSoup(res2.text,"html.parser")

        #Scraping All The Post Request Hedders
        if(b2.head.title.text!='Bees Erp Login'):
            namestr=b2.find('span',class_="studentname mb-5").text.split('       ')
            name1=namestr[1].split('(')
            StudName=name1[0].strip()
        else:
            ErrorMessage='Given Password Is Worng'
        if(ErrorMessage==''):
            Keys1={}
            for raw in b2.find('form').find_all('input'):
                try:
                    Keys1[raw['id']]=raw['value']
                except:
                    pass
            Keys1['__EVENTTARGET']='ctl00$cpHeader$ucStud$lnkOverallMarksSemwise'

            res2=s.post('https://svceta.org/BeesERP/StudentLogin/MainStud.aspx',Keys1)
            b3=BeautifulSoup(res2.text,"html.parser")
            Keys2={}
            #print(b3)
            #Scraping All The Post Request Hedders
            for raw in b3.find('form').find_all('input'):
                if('ctl00_cpStud_btn' not in raw['id']):
                    try:
                        Keys2[raw['id']]=raw['value']
                    except:
                        pass
            #print(Keys2)
            #Scraping Available Semisters And Mid Results
            Btns={}
            Sems=1
            for btns in b3.find_all('input',class_="btn btn-success btn-sm"):
                Btns[Sems]={btns['name']:btns['value']}
                Sems=Sems+1
            #print(Btns)
            if(Sem not in Btns.keys()):
                ErrorMessage=f'Semister {Sem} Results are not Released Yet.\nNote: Fee Due Also a Cause for Not Showing your Results'
            FKeys={}
            FKeys.update(Keys2)
            FKeys.update(Btns[Sem])

            res3=s.post('https://svceta.org/BeesERP/StudentLogin/Student/OverallMarksSemwise.aspx',data=FKeys)
            bres3=BeautifulSoup(res3.text,"html.parser")

            Department=bres3.find('span',id="ctl00_cpHeader_ucStudCorner_lblStudentStatus").text

            ResultsTable = bres3.find('table',id="ctl00_cpStud_grdSemwise")

            SemDetails=bres3.find('span',id="ctl00_cpStud_lblSemDetails").text

            #print('Student Name: '+StudName+'\tRollNo: '+Roll+'\n'+SemDetails)

            #Scraping all The Table Headings
            for Heads in ResultsTable.find_all('tr',align="center"):
                C=0
                Marks_Headings=''
                for Head in Heads.find_all('th'):
                    if(C==2):
                        #print(Head.font.text.center(48,' '),end='  ')
                        Marks_Headings=Marks_Headings+Head.font.text.center(48,' ')+'  '
                    else:
                        #print(Head.font.text,end='  ')
                        Marks_Headings=Marks_Headings+Head.font.text+'  '
                    C=C+1
                #print('\n'+'='*110)
            #Scraping all The Marks
            Marks_SubWise=''
            for Rows in ResultsTable.find_all('tr',align="left"):
                C=0
                for Columns in Rows.find_all('td'):
                    if(C==0):
                        #print(Columns.font.text.center(5," "),end='')
                        Marks_SubWise=Marks_SubWise+Columns.font.text.center(5," ")
                    elif (C==1):
                        #print(Columns.font.text.center(11," "),end='')
                        Marks_SubWise=Marks_SubWise+Columns.font.text.center(11," ")
                    elif (C==2):
                        #print(Columns.font.text.center(50," "),end='')
                        Marks_SubWise=Marks_SubWise+Columns.font.text.center(50," ")
                    elif (C==3):
                        #print(Columns.font.text.center(14," "),end='')
                        Marks_SubWise=Marks_SubWise+Columns.font.text.center(14," ")
                    elif (C==4):
                        #print(Columns.font.text.center(12," "),end='')
                        Marks_SubWise=Marks_SubWise+Columns.font.text.center(12," ")
                    elif (C==5):
                        #print(Columns.font.text.center(9," "),end='')
                        Marks_SubWise=Marks_SubWise+Columns.font.text.center(9," ")
                    else:
                        #print(Columns.font.text.center(8," "))
                        Marks_SubWise=Marks_SubWise+Columns.font.text.center(8," ")+'\n'
                    C=C+1

            SemSGPA=bres3.find('span',id="ctl00_cpStud_lblSemSGPA").text
            SemCGPA=bres3.find('span',id="ctl00_cpStud_lblSemCGPA").text
            #print('='*110+'\n'+SemSGPA+' '*86+SemCGPA)

            #Logout
            LOKeys={}
            LOKeys['__EVENTTARGET']='ctl00$cpHeader$ucStudCorner$lnkLogOut'
            LOKeys.update(Keys2)
            LogOut=s.post('https://svceta.org/BeesERP/StudentLogin/Student/OverallMarksSemwise.aspx',data=LOKeys)
            #Marks f-String
            Marks=f'''Student Name: {StudName}\tRollNo: {Roll}\n{SemDetails.strip()}\n{Marks_Headings}\n{'='*110}\n{Marks_SubWise}\n{'='*110}\n{' '*84+SemSGPA+' '*4+SemCGPA}\n{' '*60+'-Team Villain4U https://github.com/Karthi-Villain'}'''
            print(Marks)
except Exception as Ex:
    print(Ex)
    print(ErrorMessage)
else:
    print(ErrorMessage)
