from flask import Flask, render_template, request, redirect, url_for, flash, make_response,Response
from flask_mysqldb import MySQL
from array import *
import MySQLdb
from datetime import date
from datetime import datetime
import io
import xlwt
from tkinter import messagebox

today = date.today()
current_date = today.isoformat()


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
conn = MySQLdb.connect(host="localhost", user="root", password="", db="parking")
mysql = MySQL(app)



@app.route('/', methods=['POST', 'GET'])
def MainPage():
    return render_template("login.html", title="Login")



@app.route('/EmployeePage/<string:id>/<string:isAdmin>', methods=['POST', 'GET'])
def EmployeePage(id, isAdmin):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emp_details WHERE Emp_Id ='" + id + "'")
    user = cursor.fetchone()
    if(user[3]=='Female'):
        ch=['1']
    else:
        ch=[]
    if user[5] == "Y":
        return redirect(url_for('MyDetailsAdmin', id=id))

    cursor.execute("SELECT * FROM vehical_details WHERE Emp_Id ='" + id + "'")
    vehical_details = cursor.fetchall()

    cursor.execute("select Message from bulletin_board where Start_Time_Date < NOW() AND End_Time_Sate > NOW();")
    data1 = cursor.fetchall()

    if request.method == 'POST':
        vehno3=request.form['vehno3']
        vehno4=request.form['vehno4']
        vehno3=vehno3.upper()
        PSID = request.form['PSID']
        Name = request.form['Name']
        VehicleNO = request.form['vehno1'] + request.form['vehno2'] +vehno3 +vehno4
        CompanyName = request.form['CompanyName']
        Model = request.form['Model']
        Typev = request.form['Typev']
        UpdateTime = datetime.datetime.now()
        UpdatedBy = request.form['Name']
        cursor.execute("select * from vehical_details where Veh_No='"+VehicleNO+"'")
        x= cursor.fetchall()
        if not x:
            
            cursor.execute("INSERT INTO vehical_details (Emp_Id, Emp_Name, Veh_No, Veh_Company_Name, Veh_Model, Veh_Type, Updated_date, Updated_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(PSID, Name, VehicleNO, CompanyName, Model, Typev, UpdateTime, UpdatedBy))
            cursor.execute("INSERT INTO history_vehical_details (Emp_Id, Emp_Name, Veh_No, Veh_Company_Name, Veh_Model, Veh_Type, Updated_date, Updated_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(PSID, Name, VehicleNO, CompanyName, Model, Typev, UpdateTime, UpdatedBy))
            
        else:
            flash('Vehical Entered Already Exist!!!')
        conn.commit()
        cursor.close()

    return render_template('EmployeePage.html',ch=ch, id=id, name=user[1], vehical_details=vehical_details, bulletin_board=data1 )

    

@app.route('/MessageCenter',methods=['POST','GET'])
def MessageCenteremp():
    
    cursor = conn.cursor()
    cursor.execute("select Message from bulletin_board where Start_Time_Date < NOW() AND End_Time_Sate > NOW();")
    data = cursor.fetchall()
    cursor.close()

    return render_template('MessageCenter.html',bulletin_board=data)


@app.route("/loggedin", methods=["POST", 'GET'])
def login():
    username = str(request.form["user"])
    password = str(request.form["password"])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emp_details WHERE Emp_ID ='" + username + "'and Emp_Password='" + password + "'")
    user = cursor.fetchone()
    if user is None:
        return render_template("login.html", title="Wrong EmployeeID or Password !!")

    return redirect(url_for('EmployeePage', id=username, isAdmin=user[5]))



@app.route('/Dashboard/<string:id>',methods=['POST','GET'])
def Dashboard(id):
 
    cursor.execute("SELECT  City, Building, Veh_Type, Total_Allocated,Total_Available FROM total_slots  ")
    data = cursor.fetchall()
    conn.commit()

    cursor.close()
    return render_template('Dashboard.html' ,total_slots=data ,id=id)



@app.route('/MyDetailsAdmin/<string:id>', methods=['POST', 'GET'])
def MyDetailsAdmin(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehical_details WHERE Emp_Id ='" + id + "'")
    vehical_details = cursor.fetchall()
    cursor.execute("SELECT * FROM emp_details WHERE Emp_Id ='" + id + "'")
    user = cursor.fetchone()
    if(user[3]=='Female'):
        ch=['1']
    else:
        ch=[]
    
    if request.method == 'POST':
        Avehno3=request.form['Avehno3']
        Avehno4=request.form['Avehno4']
        Avehno3=Avehno3.upper()
        
        APSID = request.form['APSID']
        AName = request.form['AName']
        AVehicleNO = request.form['Avehno1'] + request.form['Avehno2'] + Avehno3 + Avehno4
        ACompanyName = request.form['ACompanyName']
        AModel = request.form['AModel']
        ATypev = request.form['ATypev']
        AUpdateTime = datetime.datetime.now()
        AUpdatedBy = request.form['AUpdatedBy']

        cursor.execute("select * from vehical_details where Veh_No='"+AVehicleNO+"'")
        x= cursor.fetchall()
        if not x:
            
            
            cursor.execute("INSERT INTO vehical_details (Emp_Id, Emp_Name, Veh_No, Veh_Company_Name, Veh_Model, Veh_Type, Updated_date, Updated_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(APSID, AName, AVehicleNO, ACompanyName, AModel, ATypev, AUpdateTime, AUpdatedBy))
            cursor.execute("INSERT INTO history_vehical_details (Emp_Id, Emp_Name, Veh_No, Veh_Company_Name, Veh_Model, Veh_Type, Updated_date, Updated_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(APSID, AName, AVehicleNO, ACompanyName, AModel, ATypev, AUpdateTime, AUpdatedBy))
            
           
        else:
            flash('Vehical Entered Already Exist!!!')

        conn.commit()
        cursor.close()

    return render_template('MyDetailsAdmin.html',ch=ch,id=id,name=user[1],vehical_details=vehical_details)


@app.route('/Report/<string:id>', methods=['POST', 'GET'])
def Report(id):
    cur = conn.cursor()
    cur.execute("SELECT NOW()")
    current = str(cur.fetchall())
    cur.execute("SELECT	* FROM emp_vehical_report WHERE Updated_date='" + current_date + "'")
    data = cur.fetchall()
    
    cur.execute("SELECT	City,Building FROM total_slots ")
    x=cur.fetchall()

    for i in x:
        cur.execute("SELECT	City,Building FROM location_details where City='"+i[0]+"' AND Building='"+i[1]+"'")
        chk=cur.fetchall()

        if not chk:
            cur.execute("INSERT into location_details (City,Building) VALUES (%s, %s)",(i[0], i[1],))
            conn.commit()
      
    cur.execute("SELECT	City,Building FROM location_details")
    building=cur.fetchall()   
    
    cur.close()
    return render_template('Report.html', j='#',id=id,list=data,building=building)


    #***************************Changed on 3/09/20******************

@app.route('/Download', methods=['POST', 'GET'])
def Download():
    if request.method == 'POST':
        option = request.form['attribute']
        
        
        S_days = int(request.form['days'])
        S_months = int(request.form['months'])
        S_year = int(request.form['year'])
        

        S_days1 = int(request.form['days1'])
        S_months1 = int(request.form['months1'])
        S_year1 = int(request.form['year1'])
        

        DateStart=date(S_year,S_months,S_days)
        DateEnd=date(S_year1,S_months1,S_days1)
        print(DateStart)
        print(DateEnd)

        locationlist=request.form.getlist('interest')
        l=[]
        for i in locationlist:
            l.append(str(i).split("#",1))
        
        if(locationlist[0]=='AL' and option=='All'):
            cursor = conn.cursor()
            sql = "SELECT * FROM emp_vehical_report where Updated_date >=%s AND Updated_date <=%s"
            cursor.execute(sql,(DateStart,DateEnd,))
            result=cursor.fetchall()
            output = io.BytesIO()
            workbook = xlwt.Workbook()
            sh = workbook.add_sheet('Employee Report')
            sh.write(0, 0, 'Employee Id')
            sh.write(0, 1, 'Employee Name')
            sh.write(0, 2, 'Vehical Number')
            sh.write(0, 3, 'In Time')
            sh.write(0, 4, 'Out Time')
            sh.write(0, 5, 'Vehical Type(F/T)')
            sh.write(0, 6, 'Updated Date')
            sh.write(0, 7, 'Building')
            sh.write(0, 8, 'City')
            sh.write(0, 9, 'Slot No')

            idx = 0
            for row in result:
                sh.write(idx+1, 0, str(row[0]))
                sh.write(idx+1, 1, str(row[1]))
                sh.write(idx+1, 2, str(row[2]))
                sh.write(idx+1, 3, str(row[3]))
                sh.write(idx+1, 4, str(row[4]))
                sh.write(idx+1, 5, str(row[5]))
                sh.write(idx+1, 6, str(row[6]))
                sh.write(idx+1, 7, str(row[7]))
                sh.write(idx+1, 8, str(row[8]))
                sh.write(idx+1, 9, str(row[9]))
                idx += 1

            workbook.save(output)
            output.seek(0)
            return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Vehical_report.xls"})

        elif(locationlist[0]=='AL'and option!='All'):
            search= request.form['search']
            cursor = conn.cursor()
            sql = "SELECT * FROM emp_vehical_report where {}=%s AND Updated_date >=%s AND Updated_date <=%s".format(option)
            cursor.execute(sql,(search,DateStart,DateEnd,))
            result=cursor.fetchall()
            output = io.BytesIO()
            workbook = xlwt.Workbook()
            sh = workbook.add_sheet('Employee Report')
            sh.write(0, 0, 'Employee Id')
            sh.write(0, 1, 'Employee Name')
            sh.write(0, 2, 'Vehical Number')
            sh.write(0, 3, 'In Time')
            sh.write(0, 4, 'Out Time')
            sh.write(0, 5, 'Vehical Type(F/T)')
            sh.write(0, 6, 'Updated Date')
            sh.write(0, 7, 'Building')
            sh.write(0, 8, 'City')
            sh.write(0, 9, 'Slot No')

            idx = 0
            for row in result:
                sh.write(idx+1, 0, str(row[0]))
                sh.write(idx+1, 1, str(row[1]))
                sh.write(idx+1, 2, str(row[2]))
                sh.write(idx+1, 3, str(row[3]))
                sh.write(idx+1, 4, str(row[4]))
                sh.write(idx+1, 5, str(row[5]))
                sh.write(idx+1, 6, str(row[6]))
                sh.write(idx+1, 7, str(row[7]))
                sh.write(idx+1, 8, str(row[8]))
                sh.write(idx+1, 9, str(row[9]))
                idx += 1

            workbook.save(output)
            output.seek(0)
            return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Vehical_report.xls"})
         
        elif(locationlist[0]!='AL'and option=='All'):
            cursor = conn.cursor()
            
            list1=[]
            
            for a in l:
        
                sql="SELECT * FROM emp_vehical_report WHERE Building=%s AND City=%s AND Updated_date >=%s AND Updated_date <=%s"
                cursor.execute(sql,(a[1],a[0],DateStart,DateEnd,))
                vehical_details=cursor.fetchall()
                list1.extend([list(i) for i in vehical_details])     
            list2=[tuple(i) for i in list1]
            output = io.BytesIO()
            workbook = xlwt.Workbook()
            sh = workbook.add_sheet('Employee Report')
            sh.write(0, 0, 'Employee Id')
            sh.write(0, 1, 'Employee Name')
            sh.write(0, 2, 'Vehical Number')
            sh.write(0, 3, 'In TimeDate')
            sh.write(0, 4, 'Out TimeDate')
            sh.write(0, 5, 'Vehical Type(F/T)')
            sh.write(0, 6, 'Updated Date')
            sh.write(0, 7, 'Building')
            sh.write(0, 8, 'City')
            sh.write(0, 9, 'Slot No')

            idx = 0
            for row in list2:
                sh.write(idx+1, 0, str(row[0]))
                sh.write(idx+1, 1, str(row[1]))
                sh.write(idx+1, 2, str(row[2]))
                sh.write(idx+1, 3, str(row[3]))
                sh.write(idx+1, 4, str(row[4]))
                sh.write(idx+1, 5, str(row[5]))
                sh.write(idx+1, 6, str(row[6]))
                sh.write(idx+1, 7, str(row[7]))
                sh.write(idx+1, 8, str(row[8]))
                sh.write(idx+1, 9, str(row[9]))
                idx += 1

            workbook.save(output)
            output.seek(0)
            return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Vehical_report.xls"})


        else:
            cursor = conn.cursor()
            search= request.form['search']
            list1=[]
            
            for a in l:
        
                sql="SELECT * FROM emp_vehical_report WHERE Building=%s AND City=%s AND {}=%s AND Updated_date >=%s AND Updated_date <=%s".format(option)
                cursor.execute(sql,(a[1],a[0],search,DateStart,DateEnd,))
                vehical_details=cursor.fetchall()
                list1.extend([list(i) for i in vehical_details])     
            list2=[tuple(i) for i in list1]
            output = io.BytesIO()
            workbook = xlwt.Workbook()
            sh = workbook.add_sheet('Employee Report')
            sh.write(0, 0, 'Employee Id')
            sh.write(0, 1, 'Employee Name')
            sh.write(0, 2, 'Vehical Number')
            sh.write(0, 3, 'In TimeDate')
            sh.write(0, 4, 'Out TimeDate')
            sh.write(0, 5, 'Vehical Type(F/T)')
            sh.write(0, 6, 'Updated Date')
            sh.write(0, 7, 'Building')
            sh.write(0, 8, 'City')
            sh.write(0, 9, 'Slot No')

            idx = 0
            for row in list2:
                sh.write(idx+1, 0, str(row[0]))
                sh.write(idx+1, 1, str(row[1]))
                sh.write(idx+1, 2, str(row[2]))
                sh.write(idx+1, 3, str(row[3]))
                sh.write(idx+1, 4, str(row[4]))
                sh.write(idx+1, 5, str(row[5]))
                sh.write(idx+1, 6, str(row[6]))
                sh.write(idx+1, 7, str(row[7]))
                sh.write(idx+1, 8, str(row[8]))
                sh.write(idx+1, 9, str(row[9]))
                idx += 1

            workbook.save(output)
            output.seek(0)
            return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Vehical_report.xls"})


    return render_template('Report.html')




#***************************Changed on 3/09/20******************

@app.route('/Yesterday', methods=['POST', 'GET'])
def Yesterday():
    if request.method == 'POST':
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emp_vehical_report WHERE DATE(Updated_date) = DATE(NOW() - INTERVAL 1 DAY)")
        result=cursor.fetchall()
        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Employee Report')
        sh.write(0, 0, 'Employee Id')
        sh.write(0, 1, 'Employee Name')
        sh.write(0, 2, 'Vehical Number')
        sh.write(0, 3, 'In TimeDate')
        sh.write(0, 4, 'Out TimeDate')
        sh.write(0, 5, 'Vehical Type(F/T)')
        sh.write(0, 6, 'Updated Date')
        sh.write(0, 7, 'Location')

        idx = 0
        for row in result:
            sh.write(idx+1, 0, str(row[0]))
            sh.write(idx+1, 1, str(row[1]))
            sh.write(idx+1, 2, str(row[2]))
            sh.write(idx+1, 3, str(row[3]))
            sh.write(idx+1, 4, str(row[4]))
            sh.write(idx+1, 5, str(row[5]))
            sh.write(idx+1, 6, str(row[6]))
            sh.write(idx+1, 7, str(row[7]))
            idx += 1

        workbook.save(output)
        output.seek(0)
        return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Vehical_report.xls"})

    return render_template('Report.html')


@app.route('/LastMonth', methods=['POST', 'GET'])
def LastMonth():
    if request.method == 'POST':
        
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM emp_vehical_report WHERE Updated_date>=(SELECT DATE_ADD(LAST_DAY(DATE_SUB(current_date, INTERVAL 2 MONTH)), INTERVAL 1 DAY)) AND Updated_date<=(SELECT LAST_DAY(DATE_SUB(current_date, INTERVAL 1 MONTH)))")
        result=cursor.fetchall()
        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Employee Report')
        sh.write(0, 0, 'Employee Id')
        sh.write(0, 1, 'Employee Name')
        sh.write(0, 2, 'Vehical Number')
        sh.write(0, 3, 'In TimeDate')
        sh.write(0, 4, 'Out TimeDate')
        sh.write(0, 5, 'Vehical Type(F/T)')
        sh.write(0, 6, 'Updated Date')
        sh.write(0, 7, 'Location')

        idx = 0
        for row in result:
            sh.write(idx+1, 0, str(row[0]))
            sh.write(idx+1, 1, str(row[1]))
            sh.write(idx+1, 2, str(row[2]))
            sh.write(idx+1, 3, str(row[3]))
            sh.write(idx+1, 4, str(row[4]))
            sh.write(idx+1, 5, str(row[5]))
            sh.write(idx+1, 6, str(row[6]))
            sh.write(idx+1, 7, str(row[7]))
            idx += 1

        workbook.save(output)
        output.seek(0)
        return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Vehical_report.xls"})

    return render_template('Report.html')


@app.route('/LastWeek', methods=['POST', 'GET'])
def LastWeek():
    if request.method == 'POST':
        
        cursor = conn.cursor()
        cursor.execute(
            "SELECT	* FROM emp_vehical_report WHERE Updated_date between date_sub(now(),INTERVAL 1 WEEK) and now()")
        result=cursor.fetchall()
        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Employee Report')
        sh.write(0, 0, 'Employee Id')
        sh.write(0, 1, 'Employee Name')
        sh.write(0, 2, 'Vehical Number')
        sh.write(0, 3, 'In TimeDate')
        sh.write(0, 4, 'Out TimeDate')
        sh.write(0, 5, 'Vehical Type(F/T)')
        sh.write(0, 6, 'Updated Date')
        sh.write(0, 7, 'Location')

        idx = 0
        for row in result:
            sh.write(idx+1, 0, str(row[0]))
            sh.write(idx+1, 1, str(row[1]))
            sh.write(idx+1, 2, str(row[2]))
            sh.write(idx+1, 3, str(row[3]))
            sh.write(idx+1, 4, str(row[4]))
            sh.write(idx+1, 5, str(row[5]))
            sh.write(idx+1, 6, str(row[6]))
            sh.write(idx+1, 7, str(row[7]))
            idx += 1

        workbook.save(output)
        output.seek(0)
        return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Vehical_report.xls"})

    return render_template('Report.html')


@app.route('/Last6Month', methods=['POST', 'GET'])
def Last6Month():
    if request.method == 'POST':
       
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM emp_vehical_report WHERE Updated_date < Now() and Updated_date > DATE_ADD(Now(), INTERVAL- 6 MONTH)")

        result=cursor.fetchall()
        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Employee Report')
        sh.write(0, 0, 'Employee Id')
        sh.write(0, 1, 'Employee Name')
        sh.write(0, 2, 'Vehical Number')
        sh.write(0, 3, 'In TimeDate')
        sh.write(0, 4, 'Out TimeDate')
        sh.write(0, 5, 'Vehical Type(F/T)')
        sh.write(0, 6, 'Updated Date')
        sh.write(0, 7, 'Location')

        idx = 0
        for row in result:
            sh.write(idx+1, 0, str(row[0]))
            sh.write(idx+1, 1, str(row[1]))
            sh.write(idx+1, 2, str(row[2]))
            sh.write(idx+1, 3, str(row[3]))
            sh.write(idx+1, 4, str(row[4]))
            sh.write(idx+1, 5, str(row[5]))
            sh.write(idx+1, 6, str(row[6]))
            sh.write(idx+1, 7, str(row[7]))
            idx += 1

        workbook.save(output)
        output.seek(0)
        return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Vehical_report.xls"})

    return render_template('Report.html')


@app.route('/ExceptionReport', methods=['POST', 'GET'])
def ExceptionReport():
    if request.method == 'POST':
        
        cursor = conn.cursor()
        cursor.execute("SELECT *,timestampdiff(second,In_Timedate, CURRENT_TIMESTAMP)/3600 from emp_vehical_report WHERE Out_Timedate='0000-00-00 00:00:00.00000' AND timestampdiff(second,In_Timedate, CURRENT_TIMESTAMP) / 3600>=12")
        result=cursor.fetchall()
        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Employee Report')
        sh.write(0, 0, 'Employee Id')
        sh.write(0, 1, 'Employee Name')
        sh.write(0, 2, 'Vehical Number')
        sh.write(0, 3, 'In TimeDate')
        sh.write(0, 4, 'Out TimeDate')
        sh.write(0, 5, 'Vehical Type(F/T)')
        sh.write(0, 6, 'Updated Date')
        sh.write(0, 7, 'Location')
        sh.write(0, 8, 'Hours Vehical is Parked')
        
        idx = 0
        for row in result:
            sh.write(idx+1, 0, str(row[0]))
            sh.write(idx+1, 1, str(row[1]))
            sh.write(idx+1, 2, str(row[2]))
            sh.write(idx+1, 3, str(row[3]))
            sh.write(idx+1, 4, str(row[4]))
            sh.write(idx+1, 5, str(row[5]))
            sh.write(idx+1, 6, str(row[6]))
            sh.write(idx+1, 7, str(row[7]))
            sh.write(idx+1, 8, str(row[8]))
            idx += 1

        workbook.save(output)
        output.seek(0)
        return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Vehical_report.xls"})

    return render_template('Report.html')


@app.route('/UpdateDetails/<string:id>',methods=['POST','GET'])
def UpdateDetails(id):
    cur = conn.cursor()
    cur.execute("SELECT Emp_Id, Emp_Name FROM emp_details WHERE isAdmin='Y'")
    data = cur.fetchall()

    if request.method == 'POST':
        
        PSID = request.form['PSID']
        fname = request.form['fname']
       
        cur.execute("UPDATE emp_details SET isAdmin='Y' WHERE Emp_Id=%s AND Emp_Name=%s",(PSID,fname,))
        conn.commit()
        cur.close()

    return render_template('UpdateDetails.html',id=id,emp_details=data)

@app.route('/UpdateDetails_Search/<string:id>',methods=['POST','GET'])
def UpdateDetails_Search(id):
    cur = conn.cursor()
    
    if request.method == 'POST':
        
        digit = request.form['no1']
        
        cur.execute("SELECT * FROM vehical_details where Substring(Veh_No,7,4)='"+digit+"'")
        data = cur.fetchall()
        if not data:
            flash("No entry of this vehicle number!!!")
        else:
            return render_template('UpdateDetails.html',id=id,vehical_details=data,title="Please Refresh before adding/removing Admin")
        cur.close()
        
    return render_template('UpdateDetails.html',id=id)





def search():
    cursor = conn.cursor()
    if request.method == 'POST':
        no1 = int(request.form['no1'])
        cursor.execute("SELECT RIGHT(Veh_No,4) FROM vehical_details")
        veh_no1 = int(cursor.fetchall())
        cursor.execute("SELECT * FROM vehical_details WHERE veh_no1 LIKE '%no1%'", (veh_no1, no1))
        vehical_details = cursor.fetchall()
        cursor.close()
    return render_template('UpdateDetails.html', vehical_details=vehical_details)


@app.route('/delete/<string:PSID>/<string:id>', methods = ['GET'])
def delete(PSID,id):
    
    cur = conn.cursor()
    cur.execute("UPDATE emp_details SET isAdmin='N' WHERE Emp_Id=%s",(PSID,))
    conn.commit()
    cur.close()
    return redirect(url_for('UpdateDetails',id=id))
    


@app.route('/MessageCenter/<string:id>',methods=['POST','GET'])
def MessageCenter(id):
    cursor = conn.cursor()
    cursor.execute("select Message from bulletin_board where Start_Time_Date < NOW() AND End_Time_Sate > NOW();")
    data = cursor.fetchall()
    cursor.execute("select * from bulletin_board ")
    alldata = cursor.fetchall()

     #************************************************Changed 3/09/20*******************


    if request.method == 'POST':      
        msges = request.form['msges']

        S_days = int(request.form['days'])
        S_months = int(request.form['months'])
        S_year = int(request.form['year'])
        S_hr = int(request.form['hr'])
        S_min = int(request.form['min'])

        S_days1 = request.form['days1']
        S_months1 = request.form['months1']
        S_year1 = request.form['year1']
        S_hr1 = request.form['hr1']
        S_min1 = request.form['min1']

        start=datetime(S_year,S_months,S_days,S_hr,S_min,00)
        end=datetime(S_year,S_months,S_days,S_hr,S_min,00)
        
        cursor.execute("INSERT INTO bulletin_board (Sno,Message, Start_Time_Date, End_Time_Sate) VALUES (%s,%s, %s, %s)", (msges+str(start)+str(end),msges, start, end ))

        conn.commit()

        cursor.close()
    

    return render_template('MessageCenter.html',bulletin_board=data,alldata=alldata,id=id)

        #************************************************Changed 3/09/20*******************

@app.route('/deleteMessageCenter/<string:id>',methods=['POST','GET'])
def deleteMessageCenter(id):
    if request.method=="POST":
        delete = request.form['delete']
        cursor = conn.cursor()    
        cursor.execute("delete from bulletin_board where Sno=%s",(delete,))
        conn.commit()
        cursor.close()

    return redirect(url_for('MessageCenter', id=id))

@app.route('/Message/<string:id>', methods=['POST', 'GET'])
def Message(id):
    return render_template('Message.html',id=id)


@app.route('/modify_location/<string:id>', methods=['POST', 'GET'])
def modify_location(id):
    cursor = conn.cursor()
    cursor.execute("SELECT City, Building, Veh_Type ,Total_Allocated FROM total_slots")
    data=cursor.fetchall()
    cursor.execute("select * from emp_details where Emp_Id='"+id+"'")
    user=cursor.fetchone()
    if request.method == 'POST':

        Location = request.form['Location']
        Building = request.form['Building']
        TypeVeh = request.form['TypeVeh']
        TotalAll = int(request.form['TotalAll'])

        cursor.execute("Select * from total_slots Where City=%s AND Building=%s AND Veh_Type=%s", (Location,Building, TypeVeh)) 
        check=cursor.fetchall()
        
        if check:
            if(TotalAll<check[0][3]):
                cursor.execute("Select count(PSID) from vehical_entry where PSID='NUll' AND City=%s AND Building=%s AND Veh_Type=%s",(Location,Building, TypeVeh))
                count=cursor.fetchall()
                if(TotalAll<check[0][3]-count[0][0]):
                    flash("You can Reduce slots to "+str(check[0][3]-count[0][0])+" only from "+str(check[0][3])+" !")
                else:
                    cursor.execute("SELECT slot_no from vehical_entry where PSID='NUll' AND City=%s AND Building=%s AND Veh_Type=%s ",(Location,Building, TypeVeh))
                    slot=cursor.fetchall()
                    i=len(slot)-1
                    c=0
                    while i>=0 and c<(check[0][3]-TotalAll):
                        cursor.execute("delete from vehical_entry where PSID='NUll' AND City=%s AND Building=%s AND Veh_Type=%s AND slot_no=%s",(Location,Building, TypeVeh,slot[i][0]))
                        conn.commit()
                        print(slot[i][0])
                        i=i-1
                        c=c+1

                    UpdateDate = datetime.datetime.now()
                    Updatedby = request.form['Updatedby']
                    cursor.execute("Update total_slots set Total_Allocated=%s, Updated_date=%s, Updated_by=%s Where City=%s AND Building=%s AND Veh_Type=%s", (TotalAll, UpdateDate, Updatedby,Location,Building, TypeVeh))
            
                        
                return render_template('modify_location.html',total_slots=data,id=id,name=user[1])
            slot_no = check[0][3]+1
            PSID="NULL"
            for i in range (TotalAll-check[0][3]):
                cursor.execute("INSERT INTO vehical_entry (City, Building, Veh_Type, slot_no,PSID) VALUES (%s, %s, %s, %s, %s)", (  Location, Building, TypeVeh, slot_no, PSID))
                slot_no += 1
        
        
            UpdateDate = datetime.datetime.now()
            Updatedby = request.form['Updatedby']
            cursor.execute("Update total_slots set Total_Allocated=%s, Updated_date=%s, Updated_by=%s Where City=%s AND Building=%s AND Veh_Type=%s", (TotalAll, UpdateDate, Updatedby,Location,Building, TypeVeh))
            
            conn.commit()
            return render_template('modify_location.html',total_slots=data,id=id,name=user[1])


        slot_no = 1
        PSID="NULL"
        for i in range (TotalAll):
            cursor.execute("INSERT INTO vehical_entry (City, Building, Veh_Type, slot_no,PSID) VALUES (%s, %s, %s, %s, %s)", (  Location, Building, TypeVeh, slot_no, PSID))
            slot_no += 1
        '''
        total=splabled2+splabled4+Twheeler+Fwheeler
        '''
        
        UpdateDate = datetime.datetime.now()
        Updatedby = request.form['Updatedby']
        cursor.execute("INSERT INTO total_slots (City,Building, Veh_Type, Total_Allocated, Updated_date, Updated_by) VALUES (%s, %s,%s,%s, %s, %s)", (Location,Building, TypeVeh, TotalAll, UpdateDate, Updatedby ))
        
        conn.commit()
    

    return render_template('modify_location.html',total_slots=data,id=id,name=user[1])



@app.route('/Update_slots/<string:id>',methods=['POST','GET'])
def Update_slots(id):
    if request.method == 'POST':
        City = request.form['City']
        Building= request.form['Building']
        Type = request.form['VehicleType']
        
        cur = conn.cursor()
        cur.execute("select *  from vehical_entry where City=%s AND Building=%s AND Veh_Type=%s",(City,Building,Type,))
        data = cur.fetchall()
        cur.close()
        
        return render_template('Update_slots.html',vehical_entry=data,id=id)
    return render_template('Update_slots.html',id=id)

@app.route('/Update_slots1/<string:id>/<string:City>/<string:Building>/<string:Type>/<string:slot_no>/<string:status>/<string:x>',methods=['POST','GET'])
def Update_slots1(id,City,Building,Type,slot_no,status,x):
    cur = conn.cursor()
    if request.method == 'POST':
        message = str(request.form[x])

        Type=Type.replace("%20", " ")
        print(message)
        if(status=="Disable"):
            Status="Enable"
        elif(status=="Enable"):
            Status="Disable"
    
        cur.execute("Update vehical_entry set Message='"+message+"',Status=%s where City='"+City+"' AND Building='"+Building+"' AND Veh_Type='"+Type+"' AND slot_no='"+slot_no+"'",(Status,))
        conn.commit()
        
        cur.execute("select * from vehical_entry where City=%s AND Building=%s AND Veh_Type=%s",(City,Building,Type,))
        data = cur.fetchall()
        
        return render_template('Update_slots.html',id=id,vehical_entry=data)
    return render_template('Update_slots.html',id=id)


@app.route('/ModifyVehical/<string:veh_no>/<string:id>', methods=['POST', 'GET'])
def ModifyVehical(veh_no,id):

    cursor = conn.cursor()
    cursor.execute("select * from emp_details where Emp_Id='"+id+"'")
    user=cursor.fetchone()
    if request.method == 'POST':
        delete = request.form['delete']
        Veh_No_u = request.form['Veh_No_u']
        Veh_Make_u = request.form['Veh_Make_u']
        Model_u = request.form['Model_u']
        Type_u= request.form['Type_u']
        AUpdateTime = datetime.datetime.now()
        AUpdatedBy = user[1]
        if delete=='n':
            cursor.execute("Update vehical_details set Veh_No=%s, Veh_Company_Name=%s,Veh_Model=%s,Veh_Type=%s,Updated_date=%s,Updated_by=%s where Veh_No='"+veh_no+"'",(Veh_No_u,Veh_Make_u,Model_u,Type_u,AUpdateTime,AUpdatedBy))
            cursor.execute("INSERT INTO history_vehical_details (Emp_Id, Emp_Name, Veh_No, Veh_Company_Name, Veh_Model, Veh_Type, Updated_date, Updated_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(id, user[1], Veh_No_u, Veh_Make_u, Model_u, Type_u, AUpdateTime, AUpdatedBy))
 
        elif delete=='delete':
            cursor.execute("delete from vehical_details where Veh_No='"+veh_no+"'")

        conn.commit()
        cursor.close()

    return redirect(url_for('UpdateDetails',id=id))


@app.route('/ModifyVehicalEmployee/<string:veh_no>/<string:id>', methods=['POST', 'GET'])
def ModifyVehicalEmployee(veh_no,id):

    cursor = conn.cursor()
    cursor.execute("select * from emp_details where Emp_Id='"+id+"'")
    user=cursor.fetchone()
    if request.method == 'POST':
        delete = request.form['delete']
        Veh_No_u = request.form['Veh_No_u']
        Veh_Make_u = request.form['Veh_Make_u']
        Model_u = request.form['Model_u']
        Type_u= request.form['Type_u']
        AUpdateTime = datetime.datetime.now()
        AUpdatedBy = user[1]
        if delete=='n':
            cursor.execute("Update vehical_details set Veh_No=%s, Veh_Company_Name=%s,Veh_Model=%s,Veh_Type=%s,Updated_date=%s,Updated_by=%s where Veh_No='"+veh_no+"'",(Veh_No_u,Veh_Make_u,Model_u,Type_u,AUpdateTime,AUpdatedBy))
            cursor.execute("INSERT INTO history_vehical_details (Emp_Id, Emp_Name, Veh_No, Veh_Company_Name, Veh_Model, Veh_Type, Updated_date, Updated_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(id, user[1], Veh_No_u, Veh_Make_u, Model_u, Type_u, AUpdateTime, AUpdatedBy))
 
        elif delete=='delete':
            cursor.execute("delete from vehical_details where Veh_No='"+veh_no+"'")

        conn.commit()
        cursor.close()

    return redirect(url_for('ModifyVehicalEmployee_Search',id=id))

@app.route('/ModifyVehicalEmployee_Search/<string:id>',methods=['POST','GET'])
def ModifyVehicalEmployee_Search(id):
    cur = conn.cursor()
    
    if request.method == 'POST':
        
        digit = request.form['no1']
        
        cur.execute("SELECT * FROM vehical_details where Substring(Veh_No,7,4)='"+digit+"'")
        data = cur.fetchall()
        cur.close()
        return render_template('ModifyVehicalEmployee.html',id=id,vehical_details=data)
    return render_template('ModifyVehicalEmployee.html',id=id)

@app.route('/displayP', methods=['POST','GET'])
def displayP():
    
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT(Building) FROM vehical_entry WHERE City LIKE '%Pune%'")
    build = cursor.fetchall()
    for i in build:
        
        cursor.execute("SELECT COUNT(Veh_Type) FROM vehical_entry WHERE Veh_Type='Four Wheeler' AND Building='"+i[0]+"' AND City LIKE '%Pune%' AND Status='Enable' AND PSID='NULL'")
        F = cursor.fetchall()
        cursor.execute("SELECT COUNT(Veh_Type) FROM vehical_entry WHERE Veh_Type='Two Wheeler' AND Building='"+i[0]+"' AND City LIKE '%Pune%' AND Status='Enable' AND PSID='NULL'")
        T = cursor.fetchall()
        cursor.execute("SELECT COUNT(Veh_Type) FROM vehical_entry WHERE Veh_Type LIKE '%Specially Abled Two Wheeler%' AND Building='"+i[0]+"' AND City LIKE '%Pune%' AND Status='Enable' AND PSID='NULL'")
        ST = cursor.fetchall()
        cursor.execute("SELECT COUNT(Veh_Type) FROM vehical_entry WHERE Veh_Type LIKE '%Specially Abled Four Wheeler%' AND Building='"+i[0]+"' AND City LIKE '%Pune%' AND Status='Enable' AND PSID='NULL'")
        SF = cursor.fetchall()
        cursor.execute("select * from real_time where Building='"+i[0]+"' AND City LIKE '%Pune%'")
        u = cursor.fetchall()
        
        if not u:
            cursor.execute("INSERT INTO real_time (Building,City,Specially_Abled_Two_Wheeler,Specially_Abled_Four_Wheeler,Two_Wheeler,Four_Wheeler) VALUES (%s,%s,%s,%s,%s,%s)", (i[0],"Pune",ST,SF,T,F))
        else:
            cursor.execute("Update real_time set Specially_Abled_Two_Wheeler='"+str(ST[0][0])+"' ,Specially_Abled_Four_Wheeler='"+str(SF[0][0])+"',Two_Wheeler='"+str(T[0][0])+"',Four_Wheeler='"+str(F[0][0])+"' WHERE Building='"+i[0]+"' AND City LIKE '%Pune%'")
    cursor.execute("SELECT Building,Specially_Abled_Two_Wheeler,Specially_Abled_Four_Wheeler,Two_Wheeler,Four_Wheeler from real_time where City LIKE '%Pune%' ")
    conn.commit()
    list2 = cursor.fetchall()
    
    return render_template('DisplayPagePune.html',total_slots=list2)


@app.route('/displayH', methods=['POST','GET'])
def displayH():
    
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT(Building) FROM vehical_entry WHERE City LIKE '%Hyderabad%'")
    build = cursor.fetchall()
    for i in build:
        
        cursor.execute("SELECT COUNT(Veh_Type) FROM vehical_entry WHERE Veh_Type='Four Wheeler' AND Building='"+i[0]+"' AND City LIKE '%Hyderabad%' AND Status='Enable' AND PSID='NULL'")
        F = cursor.fetchall()
        cursor.execute("SELECT COUNT(Veh_Type) FROM vehical_entry WHERE Veh_Type='Two Wheeler' AND Building='"+i[0]+"' AND City LIKE '%Hyderabad%' AND Status='Enable' AND PSID='NULL'")
        T = cursor.fetchall()
        cursor.execute("SELECT COUNT(Veh_Type) FROM vehical_entry WHERE Veh_Type LIKE '%Specially Abled Two Wheeler%' AND Building='"+i[0]+"' AND City LIKE '%Hyderabad%' AND Status='Enable' AND PSID='NULL'")
        ST = cursor.fetchall()
        cursor.execute("SELECT COUNT(Veh_Type) FROM vehical_entry WHERE Veh_Type LIKE '%Specially Abled Four Wheeler%' AND Building='"+i[0]+"' AND City LIKE '%Hyderabad%' AND Status='Enable' AND PSID='NULL'")
        SF = cursor.fetchall()
        cursor.execute("select * from real_time where Building='"+i[0]+"' AND City LIKE '%Hyderabad%'")
        u = cursor.fetchall()
        
        if not u:
            cursor.execute("INSERT INTO real_time (Building,City,Specially_Abled_Two_Wheeler,Specially_Abled_Four_Wheeler,Two_Wheeler,Four_Wheeler) VALUES (%s,%s,%s,%s,%s,%s)", (i[0],"Hyderabad",ST,SF,T,F))
        else:
            cursor.execute("Update real_time set Specially_Abled_Two_Wheeler='"+str(ST[0][0])+"' ,Specially_Abled_Four_Wheeler='"+str(SF[0][0])+"',Two_Wheeler='"+str(T[0][0])+"',Four_Wheeler='"+str(F[0][0])+"' WHERE Building='"+i[0]+"' AND City LIKE '%Hyderabad%'")
    cursor.execute("SELECT Building,Specially_Abled_Two_Wheeler,Specially_Abled_Four_Wheeler,Two_Wheeler,Four_Wheeler from real_time where City LIKE '%Hyderabad%' ")
    conn.commit()
    list2 = cursor.fetchall()
    
    return render_template('DisplayPageHyderabad.html',total_slots=list2)

@app.route('/card-swipe',methods=['POST','GET'])
def appinput():
    cursor = conn.cursor()
    '''  cursor.execute("select Message from bulletin_board where Start_Time_Date < NOW() AND End_Time_Sate > NOW();")
    data = cursor.fetchall()'''
    if request.method == 'POST':

        PSID = request.form['PSID']
        LocationIn = request.form['LocationIn']
        BuildingIn = request.form['BuildingIn']
        TypeVehIn = request.form['TypeVehIn']
        Veh_NOIn = request.form['Veh_NOIn']
        PSID = request.form['PSID']

        current_time=datetime.datetime.now()

        cursor.execute("SELECT * FROM emp_details WHERE Emp_Id ='" + PSID + "'")
        user = cursor.fetchone()
        
        cursor.execute("SELECT min(slot_no) FROM vehical_entry WHERE PSID='NULL' AND City=%s AND Building=%s AND Veh_Type=%s AND Status='Enable'",(LocationIn,BuildingIn,TypeVehIn,))
        data = cursor.fetchone()
        if str(data[0])=='None':
            flash('Parking is Full!!!')
        else:
            cursor.execute("UPDATE vehical_entry SET PSID=%s,Veh_No=%s WHERE City=%s AND Building=%s AND Veh_Type=%s AND slot_no=%s ", (PSID,Veh_NOIn, LocationIn, BuildingIn, TypeVehIn, data,))
            conn.commit()
            cursor.execute("INSERT INTO emp_vehical_report (Emp_Id,Emp_Name,Veh_No,In_Timedate,Veh_Type,Updated_date,Building,City,slot_no) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (str(PSID),str(user[1]),str(Veh_NOIn),current_time,str(TypeVehIn),current_date,str(BuildingIn),str(LocationIn),str(data[0])))
            conn.commit()
        
        cursor.close()

    return render_template('Inputpage.html')

@app.route('/remove',methods=['POST','GET'])
def remove():
    cursor = conn.cursor()
    if request.method == 'POST':
        
        current_time=datetime.datetime.now()
        
        PSID = request.form['PSID']
        
        
        cursor.execute("UPDATE vehical_entry SET PSID='NULL',Veh_No='NULL' WHERE PSID=%s ",(PSID,))
        conn.commit()
        cursor.execute("UPDATE emp_vehical_report SET Out_Timedate=current_time WHERE Emp_Id=%s AND Out_Timedate='0000-00-00 00:00:00.000000' ",(PSID,))
        conn.commit()
        cursor.close()

    return render_template('remove.html')



if __name__ == '__main__':
    app.run(debug=True)
