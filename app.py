from flask import Flask,render_template,url_for,request,redirect,flash
from flask_mysqldb import MySQL

app = Flask(__name__)
#mysql connection
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="yoga@132005."
app.config["MYSQL_DB"]="flash"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

#home page
@app.route("/")
def home():
    con=mysql.connection.cursor()
    sql="SELECT *FROM USERS"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas=res)

#new user
@app.route("/add",methods=['GET','POST'])
def add():
    if request.method=='POST':
        name=request.form['name']
        age=request.form['age']
        city=request.form['city']
        con=mysql.connection.cursor()
        sql="insert into users(NAME,AGE,CITY) values (%s,%s,%s)"
        con.execute(sql,[name,age,city])
        mysql.connection.commit()
        con.close()
        flash('user details added succesfully')
        return redirect(url_for("home"))
    return render_template("add.html")

#update 
@app.route("/edit/<string:id>",methods=['GET','POST'])

def edituser(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        name=request.form['name']
        age=request.form['age']
        city=request.form['city']
        sql="update users set NAME=%s ,AGE=%s,CITY=%s where ID=%s"
        con.execute(sql,[name,age,city,id])
        mysql.connection.commit()
        con.close()
        flash('user details updated succesfully')
        return redirect(url_for("home"))
           
    sql="select * from users where ID=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("edit.html",datas=res) 

#delete user
@app.route("/<string:id>",methods=['GET','POST'])
def deleteuser(id):
    con=mysql.connection.cursor()
    sql="delete from users where ID=%s"
    con.execute(sql,[id])
    mysql.connection.commit()
    con.close()
    flash('user details deleted succesfully')
    return redirect(url_for("home"))

if(__name__=='__main__'):
    app.secret_key="abc123"
    app.run(debug=True)
