from flask import Flask, render_template, request
from dotenv import load_dotenv
import datetime
from deta import Deta
import os

load_dotenv()

DETA_KEY = os.getenv("DETA_KEY")
deta = Deta(DETA_KEY)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    to edit perosoanl data
    """
    if 'user_id' in request.form:
        user_id = request.form['user_id']
        msg ="user id is {}".format(user_id)
    msg = "did not get user_id"
    return render_template('home.html', msg=msg)

@app.route("/add_exe_log")
def add_log():
    """
    to add exercise log of user
    - if users telegram userid is registered
    """
    return render_template("add_logg.html")

@app.route('/see_exe_log')
def see_log():
    """
    to see exercise log
    """
    return render_template('see_logg.html')

if __name__ == "__main__":
    app.run(debug=True, port=7070)