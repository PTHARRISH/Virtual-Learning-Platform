from flask import Flask, render_template,request,Response
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="users"

mysql=MySQL(app)
@app.route('/register',methods = ['POST', 'GET'])
def register():
    print(request)
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        emailaddress = request.form['emailaddress']
        phoneno = request.form['phoneno']
        password = request.form['password']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO register (firstname,lastname,emailaddress,phoneno,password) VALUES (%s,%s,%s,%s,%s)",(firstname,lastname,emailaddress,phoneno,password))
        mysql.connection.commit()
        cur.close()
        return render_template("login.html")
    return render_template('register.html')




if __name__ == '__main__':
   app.run(debug = True)
