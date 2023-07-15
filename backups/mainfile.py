from flask import Flask, render_template
app = Flask(__name__)

@app.route('/login')
def loginpage():
   return render_template('log.html')

@app.route('/signup')
def signup():
   return render_template('createnewaccount.html')

@app.route('/forgot')
def forgot():
   return render_template('forgot.html')

if __name__ == '__main__':
   app.run(debug = True)
