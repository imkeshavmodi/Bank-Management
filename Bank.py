'''
Created on Jul 9, 2017

@author: keshav
'''
import cx_Oracle
import getpass
import time
import pickle
import os

"""**********************************************************
                            CLASSES
**********************************************************"""
class account(object):
    def __init__(s):
        s.fname=""
        s.lname=""
        s.deposit=0
        s.type=""
        s.add=""
        s.ph=""
        s.pincode=""
        s.city=""
        s.state=""
        s.pwd=""
        s.acno=0
        s.name=""
    def create_account(s):   # Function to get data from user
        fname=input("\n\nEnter Your First Name: ")
        s.fname=fname.capitalize()
        lname=input("\nEnter You Last Name: ")
        s.lname=lname.capitalize()
        s.name=s.fname + " " + s.lname
        ad=input("\nEnter Your Address: ")
        s.add=ad.capitalize()
        city=input("\nEnter Your City: ")
        s.city=city.capitalize()
        state=input("\nEnter Your State: ")
        s.state=state.capitalize()
        s.pincode=input("\nEnter Your Pincode: ")
        while len(s.pincode)!=6:
            print("\n**Pincode must be of 6 characters long")
            s.pincode=input("\nAgain Enter Pincode: ")
            
        s.ph=input("\nEnter Your Phone Number: ")
        while len(s.ph)!=10:
            print("\n**Mobile Number is not of 10 digits")
            s.ph=input("\n**Retype your Mobile Number: ")
            
        t=input("\nEnter type of the Account (C/S): ")
        s.type=t.upper()
        
        s.deposit=int(input("\nEnter INITIAL OPENING AMOUNT\n**For Savings no min.  For Current >=5000 : "))
        while s.type=='C' and s.deposit<5000:
                print ("\nOpening bank account balance for Current should be greater than 5000")
                s.deposit=int(input("\n**Renter the Amount for Current Account: "))
                
        s.pwd=input("\nEnter Your PASSWORD for ONLINE BANKING\n**Atleast 8characters long ; can be alphanumeric: ")
        while len(s.pwd)< 8:
            print ("\nPASSWORD must be 8 characters long")
            s.pwd=input("\n**Retype your PASSWORD: ")
            
        print("\n\n** Your ACCOUNT No. is : ",(s.acno))
        print("\n\n**** KINDLY REMEMBER IT AS THIS IS YOUR CUSTOMER ID FOR ONLINE BANKING ****")
        if s.type=='C':
            cur.execute("""insert into cb values(:1,:2,:3,:4,:5,:6,:7,:8)""",(s.acno,s.name,s.type,s.deposit,5000,s.pwd,'Y',0))
        else:
            cur.execute("""insert into cb values(:1,:2,:3,:4,:5,:6,:7,:8)""",(s.acno,s.name,s.type,s.deposit,0,s.pwd,'Y',0))
        
         
    def show_account(s):
        
        print("\nACCOUNT NUMBER: ",s.acno)
        print("\nACCOUNT HOLDER NAME: ",s.name )
        print("\nTYPE OF ACCOUNT: ",s.type)
        print("\nADDRESS: ",(s.add),",",(s.city),",",(s.state),"-",(s.pincode))
        print("\nOPENING BALANCE: ",s.deposit)
        print("\nPHONE NUMBER: ",s.ph)

"""********************************************************************
                    FUNCTION TO GENERATE ACCOUNT NUMBER
********************************************************************"""


def gen_acno():
    try:
        inFile=open("account.dat","rb")
        outFile=open("text.dat","w")
        n=inFile.read()
        n=int(n)
        while True:
            n+=1
            outFile.write(str(n))
            inFile.close()
            outFile.close()
            os.remove("account.dat")
            os.rename("text.dat","account.dat")
            yield n
            
    except IOError:
        print ("I/O error occured")
        
"""*******************************************************************
                    FUNCTIONS TO CREATE A NEW ACCOUNT
*******************************************************************"""

def write_account():
    
    try:
        print("\nTO OPEN AN ACCOUNT IN THIS BANK. FILL OUT THE DETAILS ")
        ac=account()
        ch=gen_acno()
        ac.acno=next(ch)
        ac.create_account()
        print("\n\n**CREATING NEW DATABASE ENTRY**")
        time.sleep(1)
        print("\n\n**WAIT FOR 5 SECONDS FOR ACCOUNT TO BE ACTIVATED**")
        time.sleep(5)
        print("\n\n*****ACCOUNT CREATED SUCCESSFULLY*****")
        print("\n\n\n*****SHOWING DETAILS OF YOUR NEWLY CREATED ACCOUNT*****")
        ac.show_account()
        pickle.dump(ac)
    except:
        pass

        
"""********************************************************************
                    FUNCTION FOR CUSTOMER SIGNING IN
********************************************************************"""

def sign_in(s):
    pswd=getpass.getpass("PASSWORD: ")
    cur.execute("select pwd from cb where acno= :param1 and active='Y'",{'param1':s})
    k=cur.fetchall()
    cur.execute("select trial from cb where acno= :param1 and active='Y'",{'param1':s})
    l=cur.fetchall()
    if k==None:
        print("\n**YOUR ACCOUNT HAS NOT BEEN OPENED UP YET!!**\n")
    elif k[0][0]==pswd and l[0][0]<=3:
      cur.execute("update cb set trial=0 where acno=:param1",{'param1':s})
      print("\n**CORRECT PASSWORD**")
      print("\n*****YOU HAVE SUCCESSFULLY LOGGED IN*****")
      print(3*"\n")
      print(60*"=")
      cur.execute("select sname from cb where acno=:param1",{'param1':s})
      i=cur.fetchone()
      print("\n \t\t\tWELCOME ",i[0])
      print("")
      while True:
        
        print(60*"=")
        print("\n\n \t\t\tCUSTOMER AREA")
        print("\n \t\tSELECT WHAT OPERATION YOU WANT TO DO")
        print(60*"=")
        print(""" \n\n\t\tMENU
        
        1. Address Change
        2. Money Deposit
        3. Money Withdrawal
        4. Print Statement
        5. Transfer Money
        6. Account Closure
        7. Customer Logout""")
        
        try: 
            ch=input("\nEnter Your Choice: ")
            if ch=='1':
                ad=input("\nEnter your New ADDRESS: ")
                time.sleep(1)
                #cur.execute("update cb set address=:param1 where acno=:param2",{'param1':ad,'param2':s})
                print("\n*****Address Changed SUCCESSFULLY*****")
                
            elif ch=='2':
                de=int(input("\nEnter the Amount to be Deposited: "))
                if de>0:
                    cur.execute("select bal from cb where acno=:param1",{'param1':s})
                    i=cur.fetchone()
                    j=i[0]+de
                    cur.execute("update cb set bal=:param1 where acno=:param2",{'param1':j,'param2':s})
                    print("\n*****AMOUNT SUCCESSFULLY DEPOSITED*****")
                    cur.execute("select bal from cb where acno=:param1",{'param1':s})
                    i=fetchone()
                    print("\n\n YOUR UPDATED BALANCE IS :",i[0])
                else:
                    print("\n**WARNING : DEPOSIT AMOUNT SHOULD BE GREATER THAN 0")
                    
            elif ch=='3':
                cur.execute("select toc from cb where acno=:param1",{'param1':s})
                i=cur.fetchone()
                toc=i[0][0]
                if toc=='C' or toc=='c':
                    cur.execute("select mbal from cb where acno=:param1",{'param1':s})
                    i=cur.fetchone()
                    wit=int(input("\nEnter the Amount to WITHDRAW :"))
                    cur.execute("select bal from cb where acno=:param1",{'param1':s})
                    j=cur.fetchone()
                    if i[0]>5000 and j[0]>wit:
                        cur.execute("update cb set bal=:param1 where acno=:param2",{'param1':wit,'param2':s})
                        print("\n*****AMOUNT SUCCESSFULLY WITHDRAWN*****")
                        cur.execute("select bal from cb where acno=:param1",{'param1':s})
                        i=fetchone()
                        print("\n\n YOUR UPDATED BALANCE IS :",i[0])
                    else:
                        print("\n**WARNING : MINIMUM BALANCE RULE VOILATED **")
                elif toc=='S' or toc=='s':
                    cur.execute("select bal from cb where acno=:param1",{'param1':s})
                    i=cur.fetchone()
                    wit=int(input("\nEnter the Amount to WITHDRAW :"))
                    if i[0]>=wit:
                        cur.execute("update cb set bal=:param1 where acno=:param2",{'param1':wit,'param2':s})
                        print("\n*****AMOUNT SUCCESSFULLY WITHDRAWN*****")
                        cur.execute("select bal from cb where acno=:param1",{'param1':s})
                        i=fetchone()
                        print("\n\n YOUR UPDATED BALANCE IS :",i[0])
                    else:
                        print("\n**WARNING : MINIMUM BALANCE RULE VOILATED **")
                        
            elif ch=='4':
                cur.execute("select sname,toc,bal from cb where acno=:param1",{'param1':s})
                print("\n PRINTING ACCOUNT STATEMENT ....\n\n")
                print("\n NAME   ACCOUNT TYPE  CURRENT BALANCE\n")
                i=cur.fetchone()
                print(i)
                time.sleep(3)
                print("\n\n")
                input("\n**Press any key to continue**\n")
                
            elif ch=='5':
                cur.execute("select toc from cb where acno=:param1",{'param1':s})
                i=cur.fetchone()
                toc=i[0][0]
                tr=int(input("\nEnter the AMOUNT to be TRANSFERRED: "))
                print("\nEnter the ACCOUNT NUMBER to which ",(tr),"is to be TRANSFERRED: ")
                ac=input("")
                cur.execute("select acno from cb where acno=:param1 and active='Y'",{'param1':ac})
                i=cur.fetchone()
                if i==None:
                    print("\n** NO SUCH ACCOUNT EXISTS **")
                else:
                  cur.execute("select bal from cb where acno=:param1",{'param1':ac})
                  j=cur.fetchone()
                  k=j[0]+tr # crediting in other's account
                  if toc=='C':
                    cur.execute("select bal from cb where acno=:param1",{'param1':s})
                    i=cur.fetchone()
                    m=i[0]-tr #updating self balance
                    if i[0]>5000:
                        cur.execute("update cb set bal=:param1 where acno=:param2",{'param1':k,'param2':ac})
                        cur.execute("update cb set bal=:param1 where acno=:param2",{'param2':s,'param1':m})
                        print("\n*****AMOUNT SUCCESSFULLY TRANSFERRED*****")
                        cur.execute("select bal from cb where acno=:param1",{'param1':s})
                        i=cur.fetchone()
                        print("\n\n YOUR UPDATED BALANCE IS :",i[0])
                        '''cur.execute("select bal from cb where acno=:param1",{'param1':ac})
                        i=cur.fetchone()
                        print("\n\n OTHER'S UPDATED BALANCE IS :",i[0])'''
                    else:
                        print("\n**YOU CAN'T TRANSFER THIS MUCH AMOUNT AS IT IS GREATER THAN YOUR ACCOUNT BALANCE**\n")
                        
                  elif toc=='S':
                    cur.execute("select bal from cb where acno=:param1",{'param1':s})
                    i=cur.fetchone()
                    m=i[0]-tr #updating self balance
                    if m<0:
                        print("\n**YOU CAN'T TRANSFER THIS MUCH AMOUNT AS IT IS GREATER THAN YOUR ACCOUNT BALANCE**\n")
                    else:
                        cur.execute("update cb set bal=:param1 where acno=:param2",{'param1':k,'param2':ac})
                        cur.execute("update cb set bal=:param1 where acno=:param2",{'param2':s,'param1':m})
                        print("\n*****AMOUNT SUCCESSFULLY TRANSFERRED*****")
                        cur.execute("select bal from cb where acno=:param1",{'param1':s})
                        i=cur.fetchone()
                        print("\n\n YOUR UPDATED BALANCE IS :",i[0])
                        '''cur.execute("select bal from cb where acno=:param1",{'param1':ac})
                        i=cur.fetchone()
                        print("\n\n OTHER'S UPDATED BALANCE IS :",i[0])'''
                  else:
                    print("\nYOUR ACCOUNT IS NOT RECOGNISED\n")
                    print("**TRY AGAIN**")
                
            elif ch=='6':
                print("\n***WARNING: YOU ARE ABOUT TO CLOSE YOUR ACCOUNT. ARE YOU SURE?")
                i=input("Enter 'Y' if YES or else 'N' : ")
                if i=='Y' or i=='y':
                    cur.execute("update cb set active='N' where acno=:param1",{'param1':s})
                    print("\n*****ACCOUNT SUCCESSFULLY CLOSED*****")
                    break
                elif i=='N' or i=='n':
                    print("\n**WE ARE GLAD YOU MAKE RIGHT DECISION AT RIGHT TIME")
                    print("\n** THANKS A LOT ***")
                else:
                    print("\nINCORRECT CHOICE")
                    
            elif ch=='7':
                print("\n**YOU HAVE SUCCESSFULLY LOGOUT **")
                break
            
            else:
                print("\nIncorrect Choice ")
                
        except NameError:
            print("\n INCORRECT CHOICE")
            
    elif l[0][0]>3:
        print("\n** YOU HAVE REACHED MAXIMUM LIMIT OF RETRIALS **")
        print("\n\n\n ** WE ARE EXTREMELY SORRY **")
        print("\n\n **YOUR ACCOUNT HAS BEEN LOCKED. CONTACT ADMIN**")
        cur.execute("update cb set active='N' where acno=:param1",{'param1':s})
        
    else:
        m=l[0][0]
        print("\nINCORRECT PASSWORD")
        print("\n**TRY AGAIN**")
        cur.execute("update cb set trial=:param2 where acno=:param1",{'param1':s,'param2':m+1})
        sign_in(s)

            
"""********************************************************************
                    FUNCTION FOR ADMIN
********************************************************************"""


def admin(s,pswd):
    cur.execute("select pwd from ad where id=:param1",{'param1':s})
    i=cur.fetchone()
    if i==None:
        print("\n**YOU ARE UNAUTHORISED**\n")
    elif i[0]==pswd:
      print("\n****YOU HAVE SUCCESSFULLY LOGGED IN****\n\n")
      print("\n \tWELCOME Keshav")
      while True:
        print(3*"\n")
        print(60*"=")
        print("\n \tADMIN AREA")
        print("\n \tSELECT WHAT OPERATION YOU WANT TO DO")
        print(""" \n\n\t\tMENU
        
        1. Print Closed Accounts History
        2. Display All Accounts
        3. Admin Logout""")       
        
        try:
            ch=input("\n Enter your choice: ")
            if ch=='1':
                cur.execute("select * from cb where active='N'")
                i=cur.fetchall()
                j=cur.rowcount
                if j==0:
                    print("\n**NO ACCOUNT(s) IS CLOSED YET**\n")
                else:
                    print("\n*****PRINTING ALL CLOSED ACCOUNTS HISTORY*****\n\n")
                    for k in range(0,j,1):
                        print(i[k])
                    
            elif ch=='2':
                cur.execute("select acno,sname,toc,bal,active,pwd from cb")
                i=cur.fetchall()
                j=cur.rowcount
                if j==0:
                    print("\n**EMPTY DATABASE YET**\n")
                else:
                    print("\n***** DISPLAYING ALL ACCOUNTS *****\n\n")
                    print("\n ACNo.\tNAME\t\tTOC  Bal  Active    PWD")
                    for k in range(0,j,1):
                        print(i[k])
                    
            elif ch=='3':
                print("\n**YOU HAVE SUCCESSFULLY LOGOUT **")
                break
            else:
                print("\nIncorrect Choice")
        except NameError:
            print("\nIncorrect choice")
    else:
        print("\n** INVALID ID OR PASSWORD **")
        print("\n** TRY TO LOGIN AGAIN **")
        admin(s)

            
"""*****************************************************************************
                                    MAIN FUNCTION
*****************************************************************************"""
            
            
def intro():
    print ("\n\n\tBANK")
    print ("\n\tMANAGEMENT")
    print ("\n\n\nMADE BY : Keshav Modi")
    print ("\nCOLLEGE : JECRC")
    
intro()     # calling the main function

time.sleep(1)
print("\n\n**CHECKING STATUS OF ORACLE DATABASE**")
time.sleep(2)
con=cx_Oracle.connect("SYSTEM/1@localhost/xe")
global cur          #to execute sql statements from anywhere in the program
cur=con.cursor()
cur.execute("select open_mode from v$database")
i=cur.fetchall()
a="READ WRITE"      #check whether database is ready or not
if i[0][0]==a:
        print("\n\n*****SUCCESSFULLY CONNECTED TO THE ORACLE DATABASE*****\n\n")
else:
        print("RESTART THE PROGRAM OR ORACLE SERVICE IS NOT RUNNING IN BACKGROUND")
'''cur.execute("drop table cb")
cur.execute("""create table cb
                    (acno int primary key,sname VARCHAR2(50),toc VARCHAR2(1),
                    bal int,mbal int,pwd VARCHAR2(50),active VARCHAR2(1),trial int)""")'''
cur.execute("drop table ad")
cur.execute("create table ad(id int primary key,pwd VARCHAR2(50))")
cur.execute("insert into ad values (101,'keshav')")

while True:
    print(3*"\n")
    print(60*"=")
    print("""\t\t MAIN MENU
    
    1. Sign UP (New Customer)
    2. Sign IN (Existing Customer)
    3. ADMIN Log IN
    4. QUIT """)
    
    try:
        ch=input("\nEnter Your Choice(1~4): ")
        if ch=='1':
            write_account()
        elif ch=='2':
            cid=input("\nEnter Your CUSTOMER ID: ")
            print("\n**WARNING: Password will not be ECHOED**\n")
            sign_in(cid)
        elif ch=='3':
            aid=input("\nEnter Your ADMIN ID: ")
            print("\n**WARNING: Password will not be ECHOED**\n")
            pwd=getpass.getpass("PASSWORD: ")
            admin(aid,pwd)
        elif ch=='4':
            break
        else:
            print("\nINCORRECT CHOICE")
    except NameError:
        print("\n Incorrect Choice")
con.commit()
con.close()
        
input("\n\n\n\t\t\tTHANK YOU\n\n\n\t\t*****Press any key to exit*****")
            
"""********************************************************************************
                                END OF PROJECT
********************************************************************************"""
        
