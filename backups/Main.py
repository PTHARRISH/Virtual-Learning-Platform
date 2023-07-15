import os
import re
import MySQLdb.cursors
import playsound
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mysqldb import MySQL
from playsound import playsound
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/Test_audios/'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "users"
app.secret_key = 'the random string'
app.config['secret_key'] = "dhfebfhuiu34h3u7rh387fh8723h7hr83h27h8"

mysql = MySQL(app)


@app.route('/')
def log():
    return render_template('log.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    # playsound("C:/Users/jeyav/OneDrive/Desktop/project/Flasspro/static/audio/loginform.mp3")
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
            return redirect(url_for('index'))
        else:
            msg = 'Incorrect emailaddress / password !'
            playsound("audio/incorrect.mp3")
            return render_template('log.html', msg=msg)


@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html', msg=session["emailaddress"])


@app.route('/register', methods=['POST', 'GET'])
def register():
    msg = ''
    print(request)
    if request.method == 'POST' and 'password' in request.form and 'emailāaddress' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        emailaddress = request.form['emailaddress']
        phoneno = request.form['phoneno']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register WHERE emailaddress = % s AND password = % s', (emailaddress, password))
        registers = cursor.fetchone()
        if registers:
            msg = 'Account already exists !'
            playsound("audio/accountexists.mp3")
            return render_template('register.html', msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailaddress):
            msg = 'Invalid email address !'
            playsound("audio/invalidemail.mp3")
            return render_template('register.html', msg=msg)
        else:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO register (firstname,lastname,emailaddress,phoneno,password) VALUES (%s,%s,%s,%s,%s)",
                (firstname, lastname, emailaddress, phoneno, password))
            mysql.connection.commit()
            cur.close()
            ms3 = 'You have successfully registered !'
            flash(ms3)
            playsound("audio/regsuccess.mp3")
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route('/termin')
def test():
    return render_template("Test.html", msg=session["emailaddress"])


@app.route("/lesson/<subjectName>", methods=['POST', 'GET'])
def lesson_subject(subjectName):
    if (subjectName == "null"):
        return render_template('lesson.html')
    else:
        session['lesson_subject'] = subjectName
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        print(subjectName)
        cursor.execute('SELECT * FROM upload1 WHERE subject = %s ', (subjectName,))
        upload1 = cursor.fetchall()
        print(upload1)
        return render_template("lessons.html", msg=list(upload1), ms=session["emailaddress"])


@app.route("/lesson/")
@app.route('/lesson')
def lesson():
    return render_template('lesson.html', msg=session["emailaddress"])


@app.route('/forgot/', methods=['POST', 'GET'])
def forgot():
    msg = ''
    print(request)
    if request.method == 'POST' and 'password' in request.form and 'emailaddress' in request.form:
        emailaddress = request.form['emailaddress']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register WHERE emailaddress = % s AND password = % s', (emailaddress, password))
        registers = cursor.fetchone()
        if registers:
            ms3 = 'Emailaddress and password are correct .'
            flash(ms3)
            playsound("audio/accountexistsforgot.mp3")
            return redirect(url_for('login'))
        else:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE register SET password=%s WHERE emailaddress=%s ", (password, emailaddress))
            mysql.connection.commit()
            cur.close()
            ms5 = 'Password Changed Successfully'
            flash(ms5)
            playsound("audio/paswordchanged.mp3")
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'email id not exists'
    return render_template('forgot.html', msg=msg)


@app.route("/result_subject/<subjectName>")
def result_subject(subjectName):
    subjectname = subjectName
    name = session['emailaddress']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT results FROM responses WHERE subject = % s AND emailaddress = % s limit 1',
                   (subjectname, name))
    resp = cursor.fetchone()
    if resp is None:
        msg = "yet to be announced"
    else:
        msg = resp["results"]
    return render_template("results.html", msg=msg, ms=session["emailaddress"])


@app.route('/results')
def results():
    return render_template('result.html', msg=session["emailaddress"])


@app.route('/resultup', methods=['POST', 'GET'])
def result_upload():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM  responses')
    res = cursor.fetchall()
    if request.method == 'POST' and 'id' in request.form and 'result' in request.form:
        id = request.form['id']
        result = request.form['result']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE responses SET results=%s WHERE id=%s ", (result, id))
        mysql.connection.commit()
        cursor.close()
        ms1 = 'Result Updated Successfully'
        flash(ms1)
        return redirect('/resultup')
    elif request.method == 'POST':
        ms1 = 'email id not exists'
        flash(ms1)
    return render_template('resultupload.html', msg=session["emailaddress"], res=res)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('loggedin', None)
    session.pop('emailaddress', None)
    if request.method == "POST":
        return render_template("login.html")
    return redirect(url_for('log'))


@app.route('/admin/')
def admin():
    return render_template('adminlog.html')


@app.route('/admin/', methods=['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST':
        emailaddress = request.form['emailaddress']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM adregister WHERE emailaddress = % s AND password = % s', (emailaddress, password))
        adregister = cursor.fetchone()
        print(adregister)
        if adregister:
            session['loggedin'] = True
            session['emailaddress'] = adregister["emailaddress"]
            return redirect('/adindex')
        else:
            msg = 'Incorrect emailaddress / password !'
            return render_template('adminlog.html', msg=msg)


@app.route('/adindex', methods=['POST', 'GET'])
def adindex():
    return render_template('adindex.html', msg=session["emailaddress"])


@app.route('/adregister', methods=['POST', 'GET'])
def adregister():
    msg = ''
    print(request)
    if request.method == 'POST' and 'password' in request.form and 'emailaddress' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        emailaddress = request.form['emailaddress']
        phoneno = request.form['phoneno']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM adregister WHERE emailaddress = % s AND password = % s', (emailaddress, password))
        adregisters = cursor.fetchone()
        if adregisters:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailaddress):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', emailaddress):
            msg = 'Username must contain only characters and numbers !'
        elif not emailaddress or not password:
            msg = 'Please fill out the form !'
        else:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO adregister (firstname,lastname,emailaddress,phoneno,password) VALUES (%s,%s,%s,%s,%s)",
                (firstname, lastname, emailaddress, phoneno, password))
            mysql.connection.commit()
            cur.close()
            msd = 'You have successfully registered !'
            flash(msd)
            return redirect('/admin/')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('adregister.html', msg=msg)


ALLOWED_EXTENSIONS =set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp3','wav'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        if file and allowed_file(file.filename):
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO upload (test_name,audio,question_no,subject) VALUES (%s,%s,%s,%s)",
                        (request.form["testtname"], file.filename, request.form["question"], request.form["subject"]))
            mysql.connection.commit()
            cur.close()
            ms = 'File Upload Successfully'
            flash((ms) + file.filename + ' to the database!')
            return redirect('/upload')
        else:
            ms = 'Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif'
            flash(ms)
    return render_template("upload1.html", msg=session["emailaddress"])


@app.route("/test/<subjectName>", methods=['POST', 'GET'])
def test_subject(subjectName):
    if (subjectName == "null"):
        return render_template('Test.html')
    else:
        session['test_subject'] = subjectName
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        print(subjectName)
        cursor.execute('SELECT * FROM upload WHERE subject = %s ', (subjectName,))
        upload = cursor.fetchall()
        print(upload)
        return render_template("testpage.html", msg=list(upload), ms=session["emailaddress"])


@app.route("/display/<filename>")
def display_image(filename):
    h = 'Test_audios/' + filename
    flash(h)
    return redirect(url_for('static', filename=h), code=301)


@app.route("/classroom/", methods=['GET', 'POST'])
def class_room():
    print(request.method)
    if request.method == 'POST':
        if request.form.get('lessons') == 'lessons':
            return render_template("lesson.html")
        elif request.form.get('tests') == 'tests':
            return render_template("test.html")
        else:
            return render_template("index.html")
    elif request.method == 'GET':
        return render_template("lesson.html")


@app.route('/uploads', methods=['POST', 'GET'])
def uploads():
    if request.method == "POST":
        file = request.files["file"]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        if file and allowed_file(file.filename):
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO upload1 (lesson_name,audio,question_no,subject) VALUES (%s,%s,%s,%s)",
                        (request.form["testtname"], file.filename, request.form["question"], request.form["subject"]))
            mysql.connection.commit()
            cur.close()
            ms = 'File successfully uploaded '
            flash((ms) + file.filename + ' to the database!')
            return redirect('/uploads')
        else:
            ms = 'Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif'
            flash(ms)
    return render_template("upload.html", msg=session["emailaddress"])


@app.route('/ResponseFromUser/', methods=['GET', 'POST'])
@app.route('/ResponseFromUser', methods=['GET', 'POST'])
def thisRoute():
    answers = ""
    for i in request.json:
        answers = answers + str(request.json[str(i)]) + ","
        print(request.json[i])
    print(answers)
    subjectname = session['test_subject']
    name = session['emailaddress']
    cur = mysql.connection.cursor()

    cur.execute("INSERT INTO responses (subject,emailaddress,answers) VALUES (%s,%s,%s)", (subjectname, name, answers))
    mysql.connection.commit()
    cur.close()

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
