import pyrebase
from flask import Flask , render_template , request , redirect , url_for
from flask import session as login_session


app = Flask(__name__ , template_folder = "templates")

app.config['SECRET_KEY'] = 'super-secret-key'


firebaseConfig = {
  "apiKey": "AIzaSyBN1GWq8ks55hEQ-c4-NPWcoBcw9HXIsCE",
  "authDomain": "auth-lab-f98c9.firebaseapp.com",
  "projectId": "auth-lab-9f8c9",
  "storageBucket": "auth-lab-f98c9.appspot.com",
  "messagingSenderId": "523981179319",
  "appId": "1:523981179319:web:6c8fdeb19935ba68378032",
  "measurementId": "G-43XMCRFBBW",
  "databaseURL":""
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@app.route("/" , methods = ["GET" , "POST"])
def signup():
  if request.method == "POST":
    email = request.form['email']
    password = request.form['password']
    login_session["user"] = auth.create_user_with_email_and_password(email , password)
    login_session["quotes"] = []
    login_session["email"] = email
    login_session["password"] = password
    return redirect(url_for("home"))
  return render_template("signup.html")

@app.route("/signin" , methods = ["GET" , "POST"])
def signin():
  if request.method == "GET":
    return render_template("signin.html")

@app.route("/home" , methods = ["GET" , "POST"])
def home():
  if request.method == "POST":
    login_session["quotes"].append(request.form["quote"])
    login_session.modified = True
    return redirect(url_for("thanks"))
  return render_template("home.html")

@app.route("/signout" , methods = ["GET" , "POST"])
def signout():
  login_session['user'] = None
  auth.current_user = None
  return render_template("signin.html")


@app.route("/thanks" , methods = ["GET" , "POST"])
def thanks():
  if request.method == "GET":
    return render_template("thanks.html")

@app.route("/display" , methods = ["GET" , "POST"])
def display():
  quotes = login_session["quotes"]
  return render_template("display.html" , quotes = quotes)

if __name__ == '__main__':
    app.run(debug=True)