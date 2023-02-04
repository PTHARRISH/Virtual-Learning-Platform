from flask import Flask, render_template,request,Response
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="users"

mysql=MySQL(app)
@app.route('/',methods = ['POST', 'GET'])
def users():
    print(request)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO users (username,password) VALUES (%s,%s)",(username,password))
        mysql.connection.commit()
        cur.close()
        return Response("success")
    return render_template('users.html')


if __name__ == '__main__':
   app.run(debug = True)
