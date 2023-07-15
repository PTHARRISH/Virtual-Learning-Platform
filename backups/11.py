from flask import Flask,render_template,request,Response,session,flash,redirect,url_for,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import playsound 
from flask import jsonify
import re,os
from werkzeug.utils import secure_filename
from playsound import playsound
app=Flask(__name__)
app.config['UPLOAD_FOLDER']='static/Test_audios/'
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="users"
app.secret_key = 'the random string'
app.config['secret_key']="dhfebfhuiu34h3u7rh387fh8723h7hr83h27h8"

mysql=MySQL(app)

@app.route('/')
def log():
     return render_template('log.html') 

@app.route('/', methods =['GET', 'POST']) 
def login():
    msg = '' 
    if request.method == 'POST': 
        emailaddress = request.form['emailaddress'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM register WHERE emailaddress = % s AND password = % s', (emailaddress, password)) 
        register = cursor.fetchone() 
        print(register)
        if register: 
            session['loggedin'] = True
            session['emailaddress'] = register["emailaddress"] 
            playsound("audio/class.mp3")
            return render_template('index.html',name=register["emailaddress"])
        else: 
            msg = 'Incorrect emailaddress / password !'
            playsound("audio/incorrect.mp3")
            return render_template('log.html',msg = msg)
            
@app.route('/register',methods = ['POST', 'GET'])
def register():
    msg = ''
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
        return redirect(url_for('log'))
    return render_template('register.html')

@app.route('/testPage/', methods=['POST','GET'])
def test():
    return render_template('Test.html')

@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('emailaddress', None)  
    return redirect(url_for('log')) 

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp3','wav'])
def allowed_file(filename):
     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload', methods=['POST','GET'])
def upload():
    if request.method =="POST":
         file=request.files["file"]
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
         if file and allowed_file(file.filename):
           cur=mysql.connection.cursor()
           cur.execute("INSERT INTO upload (test_name,audio,question_no,subject) VALUES (%s,%s,%s,%s)",(request.form["testtname"],file.filename,request.form["question"],request.form["subject"]))
           mysql.connection.commit()
           cur.close()
           flash('File successfully uploaded ' + file.filename + ' to the database!')
           return redirect('/')
         else:
          flash('Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif') 
    return render_template("upload1.html")
@app.route("/test/<subjectName>")       
def test_subject(subjectName):
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
     print(subjectName)
     cursor.execute('SELECT * FROM upload WHERE subject = %s ', (subjectName,) )
     upload = cursor.fetchall()
     print(upload)
     return render_template("testpage.html",msg=list(upload))
@app.route("/display/<filename>")       
def display_image(filename):
    h='Test_audios/'+filename
    flash(h)
    return redirect(url_for('static',filename=h),code=301)
@app.route("/lesson/")       
def lesson_subject():
    return render_template("lesson.html")

@app.route('/ResponseFromUser', methods=['GET', 'POST'])
def thisRoute():
    print(request.data)
    information = request.json['data']
    return "1"    
if __name__ == '__main__':
    app.run(debug=True)