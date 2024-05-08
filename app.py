from flask import Flask, render_template,session,url_for,flash,request,redirect,send_file
import pandas as pd
import flask
import os, random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="onlinelibrary",
    charset='utf8'
)
mycursor = mydb.cursor()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'
app.config['uploadfolder'] = "static/"
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/registerback",methods=["POST","GET"])
def registerback():
    if request.method == "POST":
        Name = request.form['Name']
        Course = request.form['Course']
        Year = request.form['Year']
        Rollno = request.form['Rollno']
        Email = request.form['Email']
        password = request.form['password']
        Conformpassword = request.form['conformpassword']
        voters = pd.read_sql_query('SELECT * FROM register', mydb)
        all_emails = voters.Email.values

        if (Email in all_emails):
            flash('Already Registered', "warning")
        elif password == Conformpassword:
            sql = 'insert into register(Name,Course,Year,Rollno,Email,password)values(%s,%s,%s,%s,%s,%s)'
            cur = mydb.cursor()
            cur.execute(sql, (Name,Course,Year,Rollno,Email,password))
            mydb.commit()
            mycursor.close()
            msg = 'Your login details are : '
            t = 'Regards,'
            t1 = 'Online Book Services.'
            mail_content = 'Dear ' + Name + ',' + '\n' + msg +' Email: '+ Email+'Password: '+ password + '\n' + '\n' + t + '\n' + t1
            sender_address = 'marakalakshmi1234@gmail.com'
            sender_pass = 'sbqumhtghvfmrfxv'
            receiver_address = Email
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'Online Book System'
            message.attach(MIMEText(mail_content, 'plain'))
            ses = smtplib.SMTP('smtp.gmail.com', 587)
            ses.starttls()
            ses.login(sender_address, sender_pass)
            text = message.as_string()
            ses.sendmail(sender_address, receiver_address, text)
            ses.quit()
            flash("Account created successfully", "success")
            return render_template("register.html")
        else:
            flash("password & confirm password not match", "danger")
            return render_template('register.html')

    return render_template('register.html')


@app.route("/login")
def login():
    return render_template('login.html')
@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/forgetback', methods=['POST', 'GET'])
def forgetback():
    if request.method == "POST":
        email = request.form['email']
        sql = "select count(*),Name,password from register where Email='%s'" % (email)
        x = pd.read_sql_query(sql, mydb)
        count = x.values[0][0]
        pwd = x.values[0][2]
        name = x.values[0][1]
        if count == 0:
            flash("Email not valid try again", "info")
            return render_template('forgot.html')
        else:
            msg = 'This your password : '
            t = 'Regards,'
            t1 = 'Online Book Services.'
            mail_content = 'Dear ' + name + ',' + '\n' + msg + pwd + '\n' + '\n' + t + '\n' + t1
            sender_address = 'marakalakshmi1234@gmail.com'
            sender_pass = 'sbqumhtghvfmrfxv'
            receiver_address = email
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'Online Book Services'
            message.attach(MIMEText(mail_content, 'plain'))
            ses = smtplib.SMTP('smtp.gmail.com', 587)
            ses.starttls()
            ses.login(sender_address, sender_pass)
            text = message.as_string()
            ses.sendmail(sender_address, receiver_address, text)
            ses.quit()
            flash("Password sent to your mail ", "success")
            return render_template("student.html")

    return render_template('forgot.html')

@app.route('/studentback', methods=['POST', 'GET'])
def studentback():
    if request.method == 'POST':
        username = request.form['email']
        password1 = request.form['password']

        sql = "select * from register where Email='%s' and password='%s' " % (username, password1)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        print(type(results))
        if not results:
            flash("Invalid Email / Password", "danger")
            return render_template('student.html')
        else:
            # session['cid'] = username
            if len(results) > 0:
                session['name'] = results[0][1]
                session['email'] = results[0][5]
                # sql = "select * from register where Email='" + username + "'"
                # x = pd.read_sql_query(sql, mydb)
                # print(x)
                # x = x.drop(['id'], axis=1)
                # flash("Welcome ", "success")
                # print("==============")
                # image = results[0][-2]
                flash("Welcome ", "info")
                return render_template('studenthome.html', msg=results[0][1])
    return render_template('student.html')



@app.route("/admin",methods=["POST","GET"])
def admin():
    return render_template('admin.html')

@app.route("/adminlog",methods=["POST","GET"])
def adminlog():
    if request.method == "POST":
        username = request.form['email']
        password1 = request.form['pwd']
        if username == 'admin' and password1 == 'admin':
            return render_template('adminhome.html', msg="Login Success")
        else:
            return render_template('admin.html', msg="Login Failure!!!")
    return render_template('adminhome.html')
@app.route("/addbook")
def addbook():
    ss="select count(*) from newbook"
    x=pd.read_sql_query(ss,mydb)
    count=x.values[0][0]
    if count==0:
        bid="BID1"
        return render_template('addbook.html', b=bid)
    else:
        s="select bid from newbook ORDER BY bid DESC LIMIT 1"
        mycursor.execute(s)
        dc = mycursor.fetchall()[0]
        # dc = [j for i in dc for j in i]
        bid = str(dc[0])
        print(bid)
        bid = int(bid.split("BID")[1])
        bid=str(bid+1);
        bid="BID"+bid
        print(bid)
        # bid=list("BID089")
        return render_template('addbook.html',b=bid)

    return render_template('addbook.html')


@app.route('/addbookback', methods=['POST', 'GET'])
def addbookback():
    print("jhhhhhhhhhh")
    if request.method =="POST":
        print("jhhhhhhhhhh")
        Bookname = request.form['bname']
        Bookid = request.form['bid']
        Course = request.form['Course']
        Year = request.form['year']
        ref = request.form['ref']
        file = request.files['file']
        file_name = file.filename
        path = os.path.join(app.config['uploadfolder'], 'uploads/' + file_name)
        file.save(path)
        print(path)
        sql = "insert into newbook(bname,bid,course,year,ref,f1) values(%s,%s,%s,%s,%s,%s)"
        val = (Bookname,Bookid,Course,Year,ref,path)
        mycursor.execute(sql,val)
        mydb.commit()
        flash('Book details added successfully', "success")
        return redirect(url_for('addbook'))

@app.route("/managebook")
def managebook():
    sql="select * from newbook "
    mycursor.execute(sql, mydb)
    data = mycursor.fetchall()
    return render_template("managebook.html", data=data)

@app.route("/download/<s>")
def download(s=''):
    sql = "select f1 from newbook where id='%s'"%(s)
    mycursor.execute(sql,mydb)
    resume = mycursor.fetchall()[0][0]
    return send_file(filename_or_fp=resume,as_attachment=True)

@app.route('/cancel/<s>')
def cancel(s=0):
    sql = "delete from newbook where id='%s'" % (s)
    mycursor.execute(sql, mydb)
    mydb.commit()
    flash("Data deleted", "info")
    return redirect(url_for('managebook'))
@app.route('/cancel1/<s>')
def cancel1(s=0):
    sql = "delete from register where id='%s'" % (s)
    mycursor.execute(sql, mydb)
    mydb.commit()
    flash("Data deleted", "info")
    return redirect(url_for('viewstu'))
@app.route('/modify/<s>')
def modify(s=0):
    sql="select * from newbook where id='"+s+"'"
    x=pd.read_sql_query(sql,mydb)
    bname=x.values[0][1]
    bid=x.values[0][2]
    c=x.values[0][3]
    y=x.values[0][4]
    r=x.values[0][5]
    return render_template('modify.html',c=c,r=r,y=y,bid=bid,b=bname)

@app.route('/modifyback', methods=['POST', 'GET'])
def modifyback():
    print("jhhhhhhhhhh")
    if request.method =="POST":
        print("jhhhhhhhhhh")
        Bookname = request.form['bname']
        Bookid = request.form['bid']
        Course = request.form['c']
        Year = request.form['y']
        ref = request.form['ref']

        sql = "update newbook set bname='%s',course='%s',year='%s',ref='%s' where bid='%s'"%(Bookname,Course,Year,ref,Bookid)
        mycursor.execute(sql,mydb)
        mydb.commit()
        flash('Book details updated successfully', "success")
        return redirect(url_for('managebook'))

@app.route("/student")
def student():
    return render_template('student.html')

@app.route("/components")
def components():
    return render_template("components.html")

@app.route('/profile')
def profile():
    email=session.get('email')
    print(email)
    sql="select * from register where Email='"+email+"'"
    x=pd.read_sql_query(sql,mydb)
    id=x.values[0][0]
    name=x.values[0][1]
    c=x.values[0][2]
    y=x.values[0][3]
    r=x.values[0][4]
    p=x.values[0][6]
    return render_template('profile.html',id=id,name=name,c=c,r=r,y=y,p=p,e=email)


@app.route('/profileback', methods=['POST', 'GET'])
def profileback():
    print("jhhhhhhhhhh")
    if request.method =="POST":
        print("jhhhhhhhhhh")
        name = request.form['name']
        id = request.form['id']
        Course = request.form['c']
        Year = request.form['y']
        r = request.form['r']
        p = request.form['p']
        email=session.get('email')
        sql = "update register set name='%s',Course='%s',Year='%s',Rollno='%s',Email='%s',password='%s' where id='%s'"%(name,Course,Year,r,email,p,id)
        mycursor.execute(sql,mydb)
        mydb.commit()
        flash('Profile updated successfully', "success")
        return redirect(url_for('profile'))


@app.route("/view_books")
def view_books():
    sql="select * from newbook "
    mycursor.execute(sql, mydb)
    data = mycursor.fetchall()
    return render_template("view_books.html", data=data)
@app.route('/addstu')
def addstu():
    return render_template('register.html')

@app.route("/viewstu")
def viewstu():
    sql="select * from register "
    mycursor.execute(sql, mydb)
    data = mycursor.fetchall()
    return render_template("viewstu.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)