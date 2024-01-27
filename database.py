#Program to manage databases for small enterprises
print('''
            ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
            NOTE: In order to access full capabilities of this program, please install the fpdf library by following these steps:
            Steps:
            1) Ensure that you are connected to the internet.
            1) Click on search area on taskbar and type : command prompt
            2) Type the following command:
                pip install fpdf
''')

imp=open('log.txt','a+') #Making a text file to store login credentials for MySQL
imp.close()

import mysql.connector as msql #importing mysql connector
import datetime  

def startup(): #Defining a startup function which is called at the bottom of the code
    f=open('log.txt','r+')#Opening log file to check login credentials
    credi=f.read()

    if credi=='': #No previously saved credentials i.e. fresh login
        print('WELCOME\nPlease enter your credentials to log into MySQL:\n')
        global user_na
        global pas
        user_na=input('Enter username\n>')
        pas=input('Enter password\n>')
        cred=user_na+' '+pas
        f.write(cred)
        f.close()
        emp()

    else: #Credentials detected, auto-login option
        res=input('We are glad to have you back\nWould you like to continue as: '+credi.split()[0]+' ? (Y/N)\n>')

        if res=='Y' or res=='y':
            f.close()
            f=open('log.txt','r')
            k=f.read().split()
            user_na=k[0]
            pas=k[1]
            emp()

        else: #Erases previous credentials and initiates a fresh login
            f.close()
            f=open('log.txt','w')
            f.write('')
            f.close()
            startup()
        
def emp():  #The main program which is called inside startup()
    mcon=msql.connect(host='localhost',user=user_na,passwd=pas)

    if mcon.is_connected:
        print('MySQL connected successfully')#establishing the connection

    curs=mcon.cursor()#creating the cursor

    def fieldlist(liss):# Pre-defining a general program to make a list of fields of a table 
        curs.execute('desc '+liss)
        fliss=[]
        for x in curs:
            fliss.append(x[0]+' ')
        return fliss

    k=input('Which Database do you wish to continue with:\n1)Existing Databases\n2)Create a new database\n>')

    if k=='1':
        curs.execute('SHOW DATABASES')
        k1=curs.fetchall()
        ii=1
        print('Existing Databases are:\n')

        for x in k1:
            print(ii,' ',x[0])
            ii+=1

        kk=input('Type the name of the database that you want to use:\n>')
        curs.execute('use '+kk)
        print('Using database ',kk,' now')

    elif k=='2':
        kk=input('Enter name of database to be created:\n>')
        k2=curs.execute('CREATE DATABASE '+kk)
        print('Database successfully created')
        curs.execute('use '+kk)
        print('Using database ',kk,' now')

    else:
        print('Enter a valid choice!')
        emp()

    m=input('Which table do you wish to continue with:\n1)Existing Tables\n2)Create a new table\n>')
    global kkk

    if m=='1':
        curs.execute('SHOW TABLES')
        k2=curs.fetchall()
        iii=1
        print('Existing tables are:\n')

        for x in k2:
            print(iii,' ',x[0])
            iii+=1
        kkk=input('Enter the name of table that you wish to use:\n>')

    else:
        kkk=input('Enter the name of table to be created:\n>')
        rws=int(input('Enter the number of columns for the table:\n>'))
        qerr=[]
        j=0
        hui='CREATE TABLE '+kkk+'('
        print('''
NOTE: You will be asked for a column to be named as a Primary Key. In MySQL, a Primary Key is a unique key used to identify a record.
It cannot remain empty and each table must have one Primary Key. Choose wisely :)  

''')
        for i in range(rws):
            a=input('Name of Column '+str(i+1)+' followed by column data type.. example Name varchar(20) : ')

            if j==0:
                pki=input('Can '+a+' be used as a primary key ? (Y/N) : ')

                if pki=='Y' or pki=='y':
                    j+=1

                    if i!=rws-1:
                        hui+=a+' Primary Key,'

                    else:
                        hui+=a+' Primary Key'

                else:

                    if i!=rws-1:
                        hui+=a+','

                    else:
                        hui+=a

            else:

                if i!=rws-1:
                    hui+=a+','

                else:
                    hui+=a
        hui+=')'
        curs.execute(hui)
        print('Table created successfully')
        histfile=open(kkk+'.txt','w+')
        histfile.close()
        histfilec=open(kkk+'.txt','a')
        histfilec.writelines(fieldlist(kkk))
        histfilec.write('\n')
        histfilec.close()
    
    global pky #Global Primary key after table has been selected
    curs.execute('desc '+kkk)

    for x in curs:

        if x[3]=='PRI':
            pky=x[0]

    def insert():
        ta=fieldlist(kkk)
        histlist=[]
        huii=' values('

        for x in ta:
            yui=input('Enter the '+x+' : ')
            histlist.append(yui+' ')

            if x==ta[-1]:
                huii+='\''+yui+'\''

            else:
                huii+='\''+yui+'\''+','

        t_date=datetime.datetime.now()
        histlist.append(str(t_date))    
        toy=open(kkk+'.txt','a')
        toy.writelines(histlist)
        toy.write('\n')
        toy.close()
        query='insert into '+kkk+huii+')'
        curs.execute(query)
        mcon.commit()
        print(curs.rowcount,"record inserted")
        
    def selectall():
        curs.execute("select * from "+kkk)
        res2=curs.fetchall()
        print(str(fieldlist(kkk)))

        for x in res2:
            print(x)

    def delete():
        a=input('enter the '+pky+'for the record which has to be deleted: ')
        dlt='delete from '+kkk+' where '+pky+' = %s'
        val=(a, )
        curs.execute(dlt,val)
        mcon.commit()
        print(curs.rowcount, "record(s) deleted")

    def select():
        a1=input('enter the '+pky+': ')
        slct='select * from '+kkk+' where '+pky+' = %s'
        val=(a1, )
        curs.execute(slct,val)
        res1=curs.fetchall()
        print(str(fieldlist(kkk)))

        for y in res1:
            print(y)

    def update():
        ka=fieldlist(kkk)
        histlist1=[]
        print('What would you like to update? \n')
        oi=0

        for x in ka:
            print(oi,' ',x)
            oi+=1
        haha=int(input('>'))
        upd=ka[haha]
        ec1=input('enter the current '+pky+': ')
        na=input('enter the new '+upd+': ')
        updt='update '+kkk+' set '+upd+' = %s where '+pky+' = %s'
        val=(na,ec1, )
        curs.execute(updt,val)
        mcon.commit()
        
        slct='select * from '+kkk+' where '+pky+' = %s'
        val=(na, )
        curs.execute(slct,val)
        print(curs.rowcount, 'record(s) affected')
        res9=curs.fetchall()

        for y in res9:
            histlist1.append(y)
            
        t_date1=datetime.datetime.now()
        histlist1.append(str(t_date1))    
        toy1=open(kkk+'.txt','a')
        toy1.writelines(histlist1)
        toy1.write('\n')
        toy1.close()
        

    def order():
        ma=fieldlist(kkk)
        print('What would you like to order by? \n')
        ooi=0

        for x in ma:
            print(ooi,' ',x)
            ooi+=1
        hahah=int(input('>'))
        ordd=ma[hahah]
        ch2=input('Ascending or descending? (a/d): ')

        if ch2=='a' or ch2=='A':
                q='select * from '+kkk+' order by '+ordd
                curs.execute(q)
        else:
            q='select * from '+kkk+' order by '+ordd+' desc'
            curs.execute(q)
        resu=curs.fetchall()

        for i in resu:
            print(i)
            
    def accesshistory():
        i=0

        with open(kkk+'.txt','r') as y:
            key=input('Enter the date (yyyy-mm-dd) :') 

            for pid in y.readlines():

                if key in pid:#limit the beg
                    print('Following data belongs to record with date = ', key, ':\n',str(fieldlist(kkk))+'\tDate and Time of edit\n',pid)
                    i+=1

                else:
                    continue

            if i==0:
                print('No such record found')               

    def printablepdf():
        ui=open('Printable '+kkk+'.txt','w+')
        ui.close()
        ui=open('Printable '+kkk+'.txt','a')
        ui.writelines(fieldlist(kkk))
        ui.write('\n')
        curs.execute("select * from "+kkk)
        res3=curs.fetchall()

        for x in res3:

            for i in range(len(x)):
                str1=str(x[i])+' '
                ui.write(str1)
            ui.write('\n')
        ui.close()
        ui=open('Printable '+kkk+'.txt','r')

        from fpdf import FPDF
        pdf=FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 15)

        for x in ui:
            pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
        pdf.output('Printable '+kkk+'.pdf')
        
        print('\nPDF has been generated. Please check the folder in which this program is stored\n')    
        
        #program execution begins here             
                    
                    
    while True:
        print('***WELCOME TO DATABASE ',kk,' and you are using table ',kkk,'***')
        print('''
        1.Insert a new record
        2.Display table ''',kkk,'''
        3.Display table for selective ''',pky,'''
        4.Delete a record
        5.Update a record
        6.Display a record after ordering by a given parameter
        7.Create a printable PDF
        8.Load a previous version
        9.Go to another table/database
        10.Exit''')
        q=int(input('Enter choice: '))

        if q==1:
            insert()
            print('''
------------------------------------- Operation Successful ----------------------------------------------------------
''')
        if q==2:
            selectall()
            print('''
------------------------------------- Operation Successful ----------------------------------------------------------
''')
        if q==3:
            select()
            print('''
------------------------------------- Operation Successful ----------------------------------------------------------
''')
        if q==4:
            delete()
            print('''
------------------------------------- Operation Successful ----------------------------------------------------------
''')
        if q==5:
            update()
            print('''
------------------------------------- Operation Successful ----------------------------------------------------------
''')
        if q==6:
            order()
            print('''
------------------------------------- Operation Successful ----------------------------------------------------------
''')
        if q==10:
            print('''
------------------------------------- Exiting, Thank You ----------------------------------------------------------
''')
            break
        if q==8:
            accesshistory()
            print('''
------------------------------------- Operation Successful ----------------------------------------------------------
''')
        if q==7:
            printablepdf()
            print('''
------------------------------------- Operation Successful ----------------------------------------------------------
''')
        if q==9:
            emp()
            print('''
------------------------------------- Operation Successful ----------------------------------------------------------
''')
              
startup()                

quit()
                
