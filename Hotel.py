#import random
import datetime
import mysql.connector as m
db=m.connect(host='localhost',user='root', password='password',database='hotel')
my=db.cursor()


def createdatabase():
    try:
        my.execute('CREATE DATABASE HOTEL')
        my.execute('USE HOTEL')
        db.commit()
    except:
        my.execute('USE HOTEL')
        
def createtablecust():
    try :
        my.execute('create table cust(custid int primary key,Name varchar(20),phoneno int,Address varchar(30),Aadharno int)')
    except:
        pass
    
def createtablerooms():
    try :
        my.execute('create table rooms(roomno int primary key,roomtypeid tinyint,roomtype varchar(20),rent int,vacant tinyint,custid int, foreign key(custid) references cust(custid))')
    except:
        pass


def createtableoccup():
    try :
        my.execute('create table occup(slno int primary key,roomno int ,custid int,DoCI date ,ToCI time, DoCO date,ToCO time,foreign key(roomno) references rooms(roomno),foreign key(custid) references cust(custid))')
    except:
        pass

#######################################################################################################################

def login():
    ch=5
    while ch>0 :
        user=input('Enter Username :')
        passwd=input('Enter Password :')
        username='user'
        password='password'
        ch-=1
        if user==username and passwd==password:
            main()
        else:
            print("Wrong Username or password\nYou've ",ch," attemps remaining")
            
def main():
    print('''
~~~~~~~~~~~~~~~~~~~~~~TAJ HOTEL~~~~~~~~~~~~~~~~~~~~~
WELCOME TO TAJ HOTEL
''')
    ch = int(input('''
1-CUSTOMER
2-CHECK IN
3-CHECK OUT
4-INFO
Enter Choice :'''))
    if ch==1:
        cust()
    elif ch==2:
        checkin()
    elif ch==3:
        checkout()
    elif ch==4:
        info()
    else:
        main()
        
###############################################################################
#CUSTOMER
def cust():
    ch = int(input('''
1-ADD CUSTOMER
2-EDIT CUSTOMER
3-VIEW CUSTOMER DETAILS
9-MAIN MENU
Enter Choice :'''))
    if ch==1:
        addcust()
    elif ch==2:
        editcust()
    elif ch==3:
        viewcust()
    elif ch==9:
        main()
    

def addcust():
    print('\n#####  ADD CUSTOMER  #####\n')
    while True: 
        custid=int(input('Enter Customer Id :'))
        my.execute('Select exists(select * from cust where custid=%s)',(custid,))
        if my.fetchone()[0]==1:
            print('Customer ID Exists\n')
        else :
            break
    name= input('Enter Name :')
    phno= int(input('Enter Phone No :'))
    address= input('Enter Address :')
    aadhar = int(input('Enter Aadhaar No :'))
    my.execute('INSERT INTO cust(custid,Name,phoneno,Address,Aadharno) VALUES(%s,%s,%s,%s,%s)',(custid,name,phno,address,aadhar))
    db.commit()
    cust()
    

def editcust():
    print('#####  EDIT CUSTOMER  #####')
    while True: 
        custid=int(input('Enter Customer Id :'))
        my.execute('Select exists(select * from cust where custid=%s)',(custid,))
        if my.fetchone()[0]==0:
            print("Customer ID Doesn't Exists\n")
        else :
            break
    name= input('Enter Name :')
    phno= int(input('Enter Phone No :'))
    address= input('Enter Address :')
    aadhar = int(input('Enter Aadhaar No :'))
    my.execute("UPDATE cust set NAME=%s ,phoneno=%s ,Address=%s ,Aadharno=%s ",(name,phno,address,aadhar))
    db.commit()
    cust()


def viewcust():
    print('#####  VIEW CUSTOMER  #####')
    while True: 
        custid=int(input('Enter Customer Id :'))
        my.execute('Select exists(select * from cust where custid=%s)',(custid,))
        if my.fetchone()[0]==0:
            print("Customer ID Doesn't Exists\n")
        else :
            break
    my.execute("SELECT * from cust WHERE custid=%s ",(custid,))
    dat=my.fetchone()
    print('''
Customer ID :{}
Name        :{}
Phone No    :{}
ADDRESS     :{}
AADHAR NO   :{}
'''.format(dat[0],dat[1],dat[2],dat[3],dat[4]))
    cust()

##############################################################################
#CHECKIN

def checkin():
    while True:
        roomtype=int(input('''
####  CHECK IN  ####
1- AC 2 Bedroom
2- AC 1 Bedroom
3- Non-AC 2 Bedroom
4- Non-AC 1 Bedroom
Enter Choice :'''))
        if roomtype not in range(0,5):
            continue
        custid=int(input('Enter Customer ID :'))
        dt = datetime.datetime.now()
        roomdb = my.execute('SELECT ROOMNO FROM ROOMS WHERE ROOMTYPEID=%s AND vacant=1',(roomtype,))
        roomlst=my.fetchall()
        if len(roomlst)!= 0:
            my.execute('INSERT INTO occup(roomno,custid,DToCI) VALUES(%s,%s,%s)',(roomlst[0][0],custid,dt) )
            my.execute('UPDATE rooms SET vacant = 0,custid=%s where roomno=%s',(custid,roomlst[0][0]))
            db.commit()
            print("Room no :",roomlst[0][0])
            break
        else:
            print('Rooms Full')
    main()
    
#CHECKOUT

def checkout():
    print('#####  CHECK OUT  #####')
    while True:
        my.reset
        roomno=int(input('Enter ROOM NO :'))
        my.execute('select vacant from rooms where roomno=%s',(roomno,))
        rm=my.fetchone()
        if rm == None:
            print("Room No Dosen't exist\n")
        elif rm[0]!=0:
            print("Room Empty\nTRY AGAIN\n")
        else :
            break
    
    my.execute('UPDATE occup,rooms SET DToCO =%s,vacant=1,rooms.custid=NULL where occup.roomno=%s',(datetime.datetime.now(),roomno))
    my.execute('select rent,rooms.custid,DToCI from rooms,occup where rooms.roomno=%s',(roomno,))
    dat = my.fetchone()
    dt=datetime.datetime.now()-dat[2]            #Calculating Rent
    days=dt.days
    if days == 0:
        rent = dat[0]
    else:
        rent = dat[0]*days
    print("Rent = Rs.",rent)
    print('''
Thank You For your Stay in TAJ HOTEL
Do Visit Again
''')
    my.reset()
    db.commit()
    main()

########################################################################################### 
#INFO

def info():
    ch=int(input('''
1-Display Room Occupant
2-Display Vaccant Rooms
3-Display Occupied Rooms
'''))

    #SHOW ROOM OCCUPANT
    if ch == 1 :
        while True: 
            roomno=int(input('Enter Room NO :'))
            my.execute('select vacant from rooms where roomno=%s',(roomno,))
            rm=my.fetchone()
            if rm == None:
                print("Room No Dosen't exist\n")
                break
            elif rm[0]!=0:
                print("Room Empty\n")
                break
            else :
                my.execute('select cust.custid,Name,phoneno,address,Aadharno,DToCI from cust,rooms,occup where rooms.roomno=%s',(roomno,))
                dat=my.fetchone()
                date=datetime.datetime.date(dat[5])
                time=datetime.datetime.time(dat[5])

                print('''
Room No     :{}
Customer ID :{}
Name        :{}
Phone No    :{}
ADDRESS     :{}
AADHAR NO   :{}
Date Of Check in :{}
Time Of Check in :{}
'''.format(roomno,dat[0],dat[1],dat[2],dat[3],dat[4],date,time))
                break

    #SHOW VACANT ROOMS

    elif ch == 2:
        typ = int(input('''
1- AC 2 Bedroom
2- AC 1 Bedroom
3- Non-AC 2 Bedroom
4- Non-AC 1 Bedroom
Enter Choice :'''))
        if typ in range(1,5):
            my.execute('select roomno,rent from rooms where vacant=1 and roomtypeid=%s',(typ,))
            dat=my.fetchall()
            print('Vacant Rooms :',end='')
            for i in dat:
                print(i[0],end=',')
            print('\nRent :',dat[0][1])
        else:
            print('Incorrenct Input\n')
        info()     

    #SHOW OCCUPIED ROOMS

    elif ch == 3:
        typ = int(input('''
1- AC 2 Bedroom
2- AC 1 Bedroom
3- Non-AC 2 Bedroom
4- Non-AC 1 Bedroom
Enter Choice :'''))
        if typ in range(1,5):
            my.execute(' select roomno,rent,rooms.custid,cust.name from rooms,cust where vacant=0 and roomtypeid=%s and cust.custid=rooms.custid;',(typ,))
            dat=my.fetchall()
            print('''
        Occupied Rooms
 Room No |   Name    | Cust ID |''')
            for i in dat:
                print('''{0:<9d}| {1:<10s}| {2:<8d}| '''.format(i[0],i[3],i[1]))
                
        else:
            print('Incorrenct Input\n')
        info()
    main()
    


login()


#createdatabase()
#createtablecust()
#createtablerooms()
#createtableoccup()

