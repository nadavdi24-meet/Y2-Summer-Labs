import pyrebase
from flask import Flask , render_template , request , redirect , url_for
from flask import session as login_session
from requests.exceptions import HTTPError
import json
import random

app = Flask(__name__ , template_folder = "templates")

app.config['SECRET_KEY'] = 'super-secret-key'

firebaseConfig = {
"your api key"
    "databaseURL" : "https://individual-project-ff8c8-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

@app.route("/" , methods = ["GET" , "POST"])
def signup():
  login_session["logged_in"] = False
  recommend_list = []
  i = 0
  while i < 4:
    recommended_album = db.child("Genres").get().val()
    recommended_album = random.choice(list(recommended_album.values()))
    recommended_album = random.choice(list(recommended_album.values()))
    if recommended_album in recommend_list:
      pass
    else:
      recommend_list.append(recommended_album)
      i += 1
  login_session["recommended_list"] = recommend_list
  if request.method == "POST":
    email = request.form['email']
    password = request.form['password']
    name = request.form["name"]
    try:
        login_session["email"] = email
        login_session["password"] = password
        user = auth.create_user_with_email_and_password(email, password)
        login_session["user"] = user
        user_dict = {"name" : name , "email" : email , "saved_albums" : []}
        db.child("Users").child(login_session["user"]["localId"]).set(user_dict)
        login_session["logged_in"] = True
        return redirect(url_for("home"))

    except HTTPError as e:
      error = True
      error_text = json.loads(e.args[1])["error"]["message"]
  else:
    error = False
    error_text = ""

  return render_template("signup.html" , error = error , error_text = error_text)

@app.route("/home" , methods = ["GET" , "POST"])
def home():
  if request.method == "POST":
    if login_session["logged_in"]:
      save_album = request.form["save_album"]
      if type(save_album) == str:
        save_album = eval(save_album)
      if db.child("Users").child(login_session["user"]["localId"]).child("saved_albums").get().val() == None:
        saved_albums = [save_album]
      else:
        saved_albums = db.child("Users").child(login_session["user"]["localId"]).child("saved_albums").get().val()
        print(saved_albums)
        if save_album in saved_albums:
          pass
        else:
          saved_albums.append(save_album)
      saved_albums_copy = []
      for i in saved_albums:
        if type(i) == str:
          saved_albums_copy.append(eval(i))
        else:
          saved_albums_copy.append(i)
      saved_albums = saved_albums_copy
      db.child("Users").child(login_session["user"]["localId"]).child("saved_albums").set(saved_albums)
      return render_template("home.html" , recommended_list = login_session["recommended_list"] , logged_in = login_session["logged_in"] , saved_albums = saved_albums)
    else:
      return render_template("home.html" , recommended_list = login_session["recommended_list"] , logged_in = login_session["logged_in"])
  else:
      return render_template("home.html" , recommended_list = login_session["recommended_list"] , logged_in = login_session["logged_in"] , saved_albums = db.child("Users").child(login_session["user"]["localId"]).child("saved_albums").get().val())

@app.route("/search" , methods = ["GET" , "POST"])
def search():
  if request.method == "POST":
    login_session["genre"] = request.form["genre"]
    login_session["mood"] = request.form["mood"]
    return redirect(url_for("album"))
  return render_template("search.html")


@app.route("/album" , methods = ["GET" , "POST"])
def album():
  if request.method == "POST":
    if "recommendations_chosen_album" in request.form:
      chosen_album = request.form["recommendations_chosen_album"]
    elif "saved_albums_form" in request.form:
      chosen_album = request.form["saved_albums_form"]
    else:
      chosen_album = request.form["saved_album_page"]
    print(chosen_album)
    if type(chosen_album) == str:
      chosen_album = eval(chosen_album)
  else:
    chosen_album = db.child("Genres").child(login_session["genre"]).child(login_session["mood"]).get().val()
  return render_template("album.html" , chosen_album = chosen_album , logged_in = login_session["logged_in"])



@app.route("/saved" , methods = ["GET" , "POST"])
def saved():
  return render_template("saved.html" , saved_albums = db.child("Users").child(login_session["user"]["localId"]).child("saved_albums").get().val())



if __name__ == '__main__':
  app.run(debug=True)