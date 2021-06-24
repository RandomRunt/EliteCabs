import urllib.parse
import urllib.error
import urllib.request
from flask import Flask, render_template, redirect, url_for, request
from fareForm import fareCalculator
from flask_bootstrap import Bootstrap
import urllib.request, json

bingKey = "Ao3NIvhaVwN4XGUHxpNyou12XseihwwEZs6D6_hs0vxSHsOLix6UqgO6IAzH_O-y"

app = Flask(__name__)
app.secret_key = "super secret code"
bootstrap = Bootstrap(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'username' or request.form['password'] != 'password':
            error = 'The username or password is invalid.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/fare', methods=['GET', 'POST'])
def fare():
    ### Address Retrieval ###
    form = fareCalculator()
    if request.method == "POST":
        fare_info = request.form
        return result(fare_info)
    return render_template("fareEstimate.html", form=form)


@app.route('/fareEstimate')
def result(fare_info):
        ### API Retrieval ###
        origin = urllib.parse.quote(fare_info['tripOrigin'], safe='')
        dest = urllib.parse.quote(fare_info['tripDestination'], safe='')
        print(origin, dest)
        routeURL = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0="+origin+"&wp.1="+dest+"&key="+bingKey
        print(routeURL)
        farerequest = urllib.request.Request(routeURL)
        response = urllib.request.urlopen(farerequest)

        ### Distance and Time Collection ###
        fareresult = json.loads(response.read().decode(encoding="utf-8"))
        exactDist = fareresult["resourceSets"][0]["resources"][0]["travelDistance"]
        exactTime = fareresult["resourceSets"][0]["resources"][0]["travelDurationTraffic"]
        print(exactDist)
        print(exactTime)

        ### Cost Calculation ###
        cost = round(3.6 + (2.19 * exactDist), 2)
        roundedDist = round(exactDist, 2)
        roundedTime = (str(round((exactTime/3600), 2))).split('.')
        print(roundedTime)
        roundedTimeHour = str(roundedTime[0])
        roundedTimeMinute = (str(round(60 * float('0.'+roundedTime[1]), 0))).strip('.0')
        if roundedTimeMinute == '1':
            roundedTimeMinuteTrue = '1'
            minuteType = 'minute'
        elif roundedTimeMinute == '0':
            roundedTimeMinuteTrue = (str(roundedTimeMinute))[1]
            minuteType = 'minutes'
        else:
            roundedTimeMinuteTrue = roundedTimeMinute
            minuteType = 'minutes'

        if roundedTimeHour == '1':
            hourType = 'hour'
        else:
            hourType = 'hours'
        return render_template('fareResult.html', cost=round(cost, 2), dist=roundedDist, timeHour=roundedTimeHour, hourType=hourType, timeMinute=roundedTimeMinuteTrue, minuteType=minuteType)


@app.route('/contact', methods=['GET','POST'])
def contact():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        if name or email or subject or message != '':
            return redirect('/contactFeedback')
        else:
            return redirect(url_for('home'))
    return render_template("contact.html", error=error)

@app.route('/contactFeedback')
def feedback():
    return render_template("thanksFeedback.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run()
