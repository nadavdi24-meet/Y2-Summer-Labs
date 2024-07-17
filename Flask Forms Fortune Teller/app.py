from flask import Flask , render_template , request , redirect , url_for
import random

app = Flask(__name__ , template_folder = "templates")

@app.route("/home" , methods = ["GET" , "POST"])
def home():
	if request.method == "GET":
		return render_template("home.html")
	else:
		birth_month = request.form["month"]
		return redirect(url_for("fortune" , birth_month = birth_month))

possible_fortunes = [
    "You will find something you didn’t know you were looking for—like your keys!",
    "In the near future, you will step on a LEGO brick. Stay vigilant.",
    "You will soon discover that you can snooze your alarm five more times.",
    "A surprise meeting will bring you unexpected snacks.",
    "Your lost sock will reappear, but it will no longer match any pair.",
    "You will have an epiphany while watching cat videos online.",
    "A thrilling adventure is in your future—called 'finding a parking spot.'",
    "You will make a decision that leads to an extra nap. Well done.",
    "Expect the unexpected: an email without typos is coming your way.",
    "A piece of cake is in your near future. Maybe it’s metaphorical, but fingers crossed!"
]

@app.route("/fortune /<birth_month>")
def fortune(birth_month):
	return render_template("fortune.html" , birth_month = birth_month , possible_fortunes = possible_fortunes)

@app.route("/indecisive")
def indecisive():
	indecisive_fortunes = []
	for i in range(3):
		random_fortune = random.choice(possible_fortunes)
		if random_fortune in indecisive_fortunes:
			i -= 1
		else:
			indecisive_fortunes.append(random_fortune)
	return render_template("indecisive.html" , indecisive_fortunes = indecisive_fortunes)




if __name__ == '__main__':
    app.run(debug=True)