import requests
from bs4 import BeautifulSoup
import datetime
Url='https://svceta.org/BeesERP/Login.aspx?ReturnUrl=/BeesERP/'
Roll=""
Passwd=''
Sem=1
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

s=requests.Session()
res=s.post(Url,data=fourm)
b=BeautifulSoup(res.text,'html.parser')

LoginKeys={}
for raw in b.find('form').find_all('input'):
    try:
        LoginKeys[raw['id']]=raw['value']
    except:
        pass
LoginKeys['txtPassword']=Passwd
res2=s.post(Url,data=LoginKeys)
b2=BeautifulSoup(res2.text,"html.parser")
namestr=b2.find('span',class_="studentname mb-5").text.split('       ')
name1=namestr[1].split('(')
StudName=name1[0].strip()

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
for raw in b3.find('form').find_all('input'):
    if('ctl00_cpStud_btn' not in raw['id']):
        try:
            Keys2[raw['id']]=raw['value']
        except:
            pass
#print(Keys2)
Btns={}
Sems=1
for btns in b3.find_all('input',class_="btn btn-success btn-sm"):
    try:
        Btns[Sems]={btns['name']:btns['value']}
        Sems=Sems+1
    except:
        pass
#print(Btns)
FKeys={}
FKeys.update(Keys2)
FKeys.update(Btns[Sem])

res3=s.post('https://svceta.org/BeesERP/StudentLogin/Student/OverallMarksSemwise.aspx',data=FKeys)
bres3=BeautifulSoup(res3.text,"html.parser")

Department=bres3.find('span',id="ctl00_cpHeader_ucStudCorner_lblStudentStatus").text

ResultsTable = bres3.find('table',id="ctl00_cpStud_grdSemwise")

SemDetails=bres3.find('span',id="ctl00_cpStud_lblSemDetails").text

print('Student Name: '+StudName+'\tRollNo: '+Roll+'\n'+SemDetails)
for Heads in ResultsTable.find_all('tr',align="center"):
    C=0
    
    for Head in Heads.find_all('th'):
        if(C==2):
            print(Head.font.text.center(48,' '),end='  ')
        else:
            print(Head.font.text,end='  ')
        C=C+1
    print('\n'+'='*110)
for Rows in ResultsTable.find_all('tr',align="left"):
    C=0
    
    for Columns in Rows.find_all('td'):
        if(C==0):
            print(Columns.font.text.center(5," "),end='')
        elif (C==1):
            print(Columns.font.text.center(11," "),end='')
        elif (C==2):
            print(Columns.font.text.center(50," "),end='')
        elif (C==3):
            print(Columns.font.text.center(14," "),end='')
        elif (C==4):
            print(Columns.font.text.center(12," "),end='')
        elif (C==5):
            print(Columns.font.text.center(9," "),end='')
        else:
            print(Columns.font.text.center(8," "))
        C=C+1

SemSGPA=bres3.find('span',id="ctl00_cpStud_lblSemSGPA").text
SemCGPA=bres3.find('span',id="ctl00_cpStud_lblSemCGPA").text
print('='*110+'\n'+SemSGPA+' '*86+SemCGPA)
