from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
import datetime
from flask_table import Table, Col
from deta import Deta
import os
from bleach import clean
import string
import secrets
import logging
from flask_session import Session
# import redis

load_dotenv()

DETA_KEY = os.getenv("DETA_KEY")
# KV_REST_API_URL = os.getenv("KV_URL")
deta = Deta(DETA_KEY)

gym_member_db = deta.Base("User_DB")

change_log_db = deta.Base("Change_Log_DB")

def load_member_list():
    gym_members = gym_member_db.fetch().items
    gym_member_ids = [gym_member["user_id"] for gym_member in gym_members]
    return gym_member_ids

waiting_db = deta.Base("Waiting_DB")

def load_waiting_list():
    # to load waiting_member ids
    waiting_members = waiting_db.fetch().items
    waiting_member_ids = [waiting_member["user_id"] for waiting_member in waiting_members]
    return waiting_member_ids


log_db = deta.Base("Log_DB")

treadmill_db = deta.Base("Treadmill_DB")

now = datetime.datetime.now()

def gen_key():
    chars = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(chars) for _ in range(32))
    return key

app = Flask(__name__)

app.debug = True

app.secret_key = DETA_KEY
# app.config["SESSION_TYPE"] = "redis"
# app.config["SESSION_REDIS"] = redis.from_url(KV_REST_API_URL)
app.config["SESSION_PERMANENT"] = True # so the session has a default time limit which expires
app.config['PERMANENT_SESSION_LIFETIME'] = 1800 # 20 min

# Session(app)

app.logger.setLevel(logging.INFO)
# handler = logging.FileHandler('app.log')
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# app.logger.addHandler(handler)
 
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

@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Handles user login 
    """
    msg = ''
    if request.method == 'POST':
        user_id = request.form['request']
        first_name = request.form['first_name']
        hash = request.form['hash']
        print(f'id: {user_id}, first name: {first_name}, hash: {hash}')
    if 'userId' in request.form:
        user_id = clean(request.form['userId'])
        # to reload 
        gym_member_ids = load_member_list()
        waiting_member_ids = load_waiting_list()

        if user_id in gym_member_ids:
            session['loggedin'] = True
            session['user_id'] = user_id
            app.logger.info(f"{user_id} loggedin")
            return redirect(url_for('home'))
        
        elif user_id in waiting_member_ids:
            """
            user already in waiting list
            """
            user = waiting_db.get(user_id)
            msg = f"Hi {user['first_name']} 👋, approval is sent to admin please be patient 😊."
            app.logger.info(f"{user_id} already requested for approval")
            return render_template('waiting.html', msg=msg)
        
        else:
            """
            user does not request approval
            """
            # msg = 'User is not registered'
            app.logger.info("user neither does not request approval nor logged in")
            return render_template("signup.html")
    app.logger.warning("User not logged in or session expired")
    return render_template('login.html', msg=msg)

@app.route('/request_approval', methods=['GET', 'POST'])
def request_approval():
    """
    Handles user request for approval
    GET: Dispaly the form
    POST: process the form data and redirects to the login page
    """
    if request.method == 'POST':
        waiting_dict = {
            "first_name": clean(request.form['firstName']),
            "last_name": clean(request.form['lastName']),
            "user_name": clean(request.form['userName']),
            "user_id": clean(request.form['userId']),
            "is_bot": bool(request.form['isBot']),
            "allows_write": bool(request.form['allowWrite']),
            "requested_at": datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),
            "approved": False,
            "key": clean(request.form['userId']),
        }
        waiting_db.put(waiting_dict)
        # here let's reload waiting_id list and return to login
        app.logger.info(f"Approval submitted for {request.form['userId']}")
        load_waiting_list()
        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Handles main page
    GET: Dispaly form
    POST: Process the form
    """
    if 'loggedin' in session:
        user = gym_member_db.get(session['user_id'])
        return render_template('home.html', user=user)
    app.logger.warning("User not logged in or session expired")
    return redirect(url_for('login'))
    

@app.route('/update_personal_data', methods=['POST'])
def update_personal_data():
    """
    when submitting the update to database
    POST: process the form and update data and returns to home page
    """
    if 'loggedin' in session:
        user_id = session['user_id']
        # user = gym_member_db.get(user_id)
        user_info_dict={}
        change_log_dict = {}

        user_info_dict["full_name"] = clean(str(request.form['fullName']))
        user_info_dict["height"] = change_log_dict["height"] = float(request.form['heightCM'])
        user_info_dict["weight"] = change_log_dict["weight"] = float(request.form['weightCM'])
        user_info_dict["main_goal"] = clean(str(request.form['goal']))

        user_info_dict["fat_percent"] = change_log_dict["fat_percent"] = float(request.form["fatPercent"])
        user_info_dict["waist_circumference"] = change_log_dict["waist_circum"] = float(request.form["waistCircum"])
        user_info_dict["hip_circumference"] = change_log_dict["hip_circum"] = float(request.form["hipCircum"])
        user_info_dict["calf_circumference"] = change_log_dict["calf_circum"] = float(request.form["calfCircum"])
        user_info_dict["chest_width"] = change_log_dict["chest_width"] = float(request.form["chestWidth"])
        user_info_dict["shoulder_width"] = change_log_dict["shoulder_width"] = float(request.form["shoulderWidth"])
        user_info_dict["bicep_circumference"] = change_log_dict["bicep_circum"] = float(request.form["bicepCircum"])

        change_log_dict["user_id"] = user_id

        user_info_dict["updated_at"] = change_log_dict["date_recorded"] = datetime.date.today().strftime("%d/%m/%Y")

        change_log_db.put(change_log_dict)

        gym_member_db.update(user_info_dict, user_id)
        app.logger.info(f"Perosnla data for {user_id} is updated successfully")
        return redirect(url_for('home'))
    else: 
        app.logger.warning("User not logged in or session expired")
        return redirect(url_for('login'))

@app.route('/add_treadmill_log', methods=['GET', 'POST'])
def treadmill():
    """
    to enter treadmill log
    GET: display the form
    POST: process the form and eneter the data to db
    """
    if 'loggedin' in session:
        msg = ''
        if request.method == 'POST':
            tread_mill_dict = {
                'steps': request.form["steps"],
                'distance': clean(str(request.form["distance"])),
                'minute': request.form["minutes"],
                'calories': clean(str(request.form["calories"])),
                'max_speed': clean(str(request.form["max_speed"])),
                'max_incline': clean(str(request.form["max_incline"])),
                'feeling': clean(request.form["feeling"]),
                'date': clean(request.form["work_date"]),
                'user_id': session['user_id'],
                'notes': clean(request.form["notes"])
            }
            treadmill_db.put(tread_mill_dict)
            app.logger.info(f"New Traedmill exercise is recorded for user {session['user_id']}")
        return render_template("treadmill_log.html", msg=msg)
    else:
        app.logger.warning("User not logged in or session expired")
        return redirect(url_for('login'))

@app.route("/add_exe_log", methods=['GET', 'POST'])
def add_log():
    """
    to add exercise log of user
    - if users telegram userid is registered
    GET: dispaly the form to add exercise log
    POST: process the form and add the data to db
    """
    if 'loggedin' in session:
        msg = ''
        if request.method == 'POST':
            log_info_dict = {
                'body_area': clean(request.form['bodyOfArea']),
                'exercise_name': clean(request.form['exerciseName']),
                'equipment_used': clean(request.form['equipmentUsed']),
                'number_of_reps': request.form['numberOfReps'],
                'number_of_cycles': request.form['numberOfCycle'],
                'exercise_duration': clean(request.form['exerciseDuration']),
                'feeling': clean(request.form['feeling']),
                'date_worked': clean(request.form['dateWorked']),
                'additional_info': clean(request.form['addInfo']),
                'user_id':session["user_id"],
            }
            msg = 'New exercise data saved'
            
            log_db.put(log_info_dict)
            app.logger.info(f"new exercise is log is recorded for user {session['user_id']}")
        return render_template("add_logg.html", msg=msg)
    else:
        app.logger.warning("User not logged in or session expired")
        return redirect(url_for('login'))

@app.route('/see_exe_log')
def see_log():
    """
    to see exercise log
    GET: dispplays the exercise table  - if user is logged in
    """
    if 'loggedin' in session:
        user_id = session["user_id"]
        user_exe_log = log_db.fetch({"user_id" : user_id}).items
        table_exe_log = Exe_log_table(user_exe_log)
        table_exe_log.border = True
        return render_template('see_logg.html', exe_table=table_exe_log)
    else:
        app.logger.warning("User not logged in or session expired")
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=7070)
