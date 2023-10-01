from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
import datetime
from flask_table import Table, Col, ButtonCol, DatetimeCol, DateCol
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

log_db = deta.Base("Log_DB")

now = datetime.datetime.now()

app = Flask(__name__)

chars = string.ascii_letters + string.digits+string.punctuation
key = ''.join(secrets.choice(chars) for _ in range(32))

app.secret_key = key

# app.config["SESSION_PERMANENT"] = True # so the session has a default time limit which expires
# app.config['PERMANENT_SESSION_LIFETIME'] = 3600 # 60 min


class Exe_log_table(Table):
    user_id = Col('user_id')
    date_worked = Col('date_worked')
    exercise_name = Col('exercise_name')
    equipment_used = Col('equipment_used')
    number_of_reps = Col('number_of_reps')
    number_of_cycles = Col('number_of_cycles')
    exercise_duration = Col('exercise_duration')
    feeling = Col('feeling')
    additional_info = Col('additional_info')

# def format_date(date, format_string):
#     if isinstance(date, str):
#         date = datetime.datetime.strptime(date, '%m/%d/%Y')
#     return date.strftime(format_string)

# app.jinja_env.filters['strftime'] = format_date


@app.route('/signup/')
def signup():
    """
    where user request to signup and his request will be sent to admin's 
    - if they approve it his data will be signed in the main db table
    - if not his data will be stored in separte db table
    """
    

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
        user_info_dict={}

        updateHeight = float(request.form['heightCM'])
        updateWeight = float(request.form['weightCM'])
        updateGoal = str(request.form['goal'])
        updateUserName = str(request.form['fullName'])

        user_info_dict["full_name"] = updateUserName
        user_info_dict["height"] = updateHeight
        user_info_dict["weight"] = updateWeight
        user_info_dict["main_goal"] = updateGoal

        user_info_dict["updated_at"] = datetime.date.today().strftime("%d/%m/%Y")

        gym_member_db.update(user_info_dict, user_id)

        return redirect(url_for('home'))
    else: 
        return redirect(url_for('login'))

@app.route("/add_exe_log", methods=['GET', 'POST'])
def add_log():
    """
    to add exercise log of user
    - if users telegram userid is registered
    """
    if 'loggedin' in session:
        msg = ''
        if request.method == 'POST':
            log_info_dict = {}

            log_info_dict["body_area"] = request.form['bodyOfArea']
            log_info_dict["exercise_name"] = request.form['exerciseName']
            log_info_dict["equipment_used"] = request.form['equipmentUsed']
            log_info_dict["number_of_reps"] = request.form['numberOfReps']
            log_info_dict["number_of_cycles"] = request.form['numberOfCycle']
            log_info_dict["exercise_duration"] = request.form['exerciseDuration']
            log_info_dict["feeling"] = request.form['feeling']
            log_info_dict["date_worked"] = request.form['dateWorked']
            log_info_dict["additional_info"] = request.form['addInfo']

            log_info_dict["user_id"] = session['user_id']
            msg = 'New exercise data saved'
            
            log_db.put(log_info_dict)
        return render_template("add_logg.html", msg=msg)
    else:
        return redirect(url_for('login'))

@app.route('/see_exe_log')
def see_log():
    """
    to see exercise log
    """
    if 'loggedin' in session:
        user_id = session["user_id"]
        user_exe_log = log_db.fetch({"user_id" : user_id}).items
        table_exe_log = Exe_log_table(user_exe_log)
        table_exe_log.border = True
        return render_template('see_logg.html', exe_table=table_exe_log)
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=7070)