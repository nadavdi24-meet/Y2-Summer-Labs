import pyrebase
from flask import Flask , render_template , request , redirect , url_for
from flask import session as login_session
from requests.exceptions import HTTPError
import json


app = Flask(__name__ , template_folder = "templates")

app.config['SECRET_KEY'] = 'super-secret-key'

firebaseConfig = {
  "put in api"
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
@app.route("/" , methods = ["GET" , "POST"])
def signup():
  if request.method == "POST":
    email = request.form['email']
    password = request.form['password']
    full_name = request.form["full_name"]
    user_name = request.form["user_name"]
    try:
        login_session["quotes"] = []
        login_session["email"] = email
        login_session["password"] = password
        user = auth.create_user_with_email_and_password(email, password)
        login_session["user"] = user
        user_dict = {"full_name" : full_name , "email" : email , "user_name" : user_name , "uid" : login_session["user"]["localId"]}
        db.child("Users").set(user_dict)
        return redirect(url_for("home"))

    except HTTPError as e:
      error = True
      error_text = json.loads(e.args[1])["error"]["message"]
  else:
    error = False
    error_text = ""

  return render_template("signup.html" , error = error , error_text = error_text)

@app.route("/signin" , methods = ["GET" , "POST"])
def signin():
  return render_template("signin.html")

@app.route("/home" , methods = ["GET" , "POST"])
def home():
  if request.method == "POST":
    quote = {"text" : request.form["quote"] , "said_by" : request.form["said_by"] , "uid" : login_session["user"]["localId"]}
    db.child("Quotes").push(quote)

    return redirect(url_for("thanks"))
  return render_template("home.html")

@app.route("/signout" , methods = ["GET" , "POST"])
def signout():
  login_session['user'] = None
  auth.current_user = None
  return redirect(url_for("signin"))


@app.route("/thanks" , methods = ["GET" , "POST"])
def thanks():
  if request.method == "GET":
    return render_template("thanks.html")

@app.route("/display" , methods = ["GET" , "POST"])
def display():
  return render_template("display.html" , quotes = db.child("Quotes").get().val())

if __name__ == '__main__':
    app.run(debug=True)