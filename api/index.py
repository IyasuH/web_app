from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
import datetime
from deta import Deta
import os

import string
import secrets

load_dotenv()

DETA_KEY = os.getenv("DETA_KEY")
deta = Deta(DETA_KEY)

gym_member_db = deta.Base("User_DB")

gym_members = gym_member_db.fetch().items
gym_member_ids = []
for gym_member in gym_members:
    gym_member_ids.append(gym_member["user_id"])

now = datetime.datetime.now()

app = Flask(__name__)

chars = string.ascii_letters + string.digits+string.punctuation
key = ''.join(secrets.choice(chars) for _ in range(32))

app.secret_key = key


@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'userId' in request.form:
        user_id = request.form['userId']
        if user_id in gym_member_ids:
            session['loggedin'] = True
            session['user_id'] = user_id
            return redirect(url_for('home'))
        else:
            msg = 'User is not registered'
    return render_template('login.html', msg=msg)

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    to see and edit perosoanl data
    """
    if 'loggedin' in session:
        user = gym_member_db.get(session['user_id'])
        print(user)
        print(type(user))
        # print(user[0])
        return render_template('home.html', user=user)
    return redirect(url_for('login'))

@app.route('/update_personal_data', methods=['POST'])
def update_personal_data():
    """
    when submitting the update to database
    """
    if 'loggedin' in session:
        user_id = session['user_id']
        # user = gym_member_db.get(user_id)
        user_info_dict=[]

        updateHeight = float(request.form['heightCM'])
        updateWeight = float(request.form['weightCM'])
        updateGoal = string(request.form['goal'])

        print(updateHeight)
        print(type(updateHeight))
        print(type(updateGoal))

        user_info_dict["height"] = updateHeight
        user_info_dict["weight"] = updateWeight
        user_info_dict["specific_goal"] = updateGoal

        user_info_dict["updated_at"] = datetime.date.today().strftime("%d/%m/%Y")

        gym_member_db.update(user_info_dict, user_id)

        return redirect(url_for('home'))
    else: 
        return redirect(url_for('login'))

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