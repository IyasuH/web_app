from flask import Flask, render_template, request, session
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

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    to edit perosoanl data
    """
    msg = "did not get user_id"
    if request.method == 'POST' and 'userId' in request.form and 'userName' in request.form:
        msg = "user did not register"
        user_id = request.form['userId']

        if user_id in gym_member_ids:
            """
            this means user id is found in database
            """
            # let's update session here
            session['user'] = True
            session['user_id'] = user_id
            # user_name = request.form['userName']
        
            msg ="user registered"
            user = gym_member_db.get(user_id)
            return render_template('home.html', msg=msg, user=user)

    return render_template('home.html', msg=msg)

@app.route('/update_personal_data', methods=['POST'])
def update_personal_data():
    """
    when submitting the update to database
    """
    # if session['user'] == True:
    if 'user' in session:
        user_id = session['user_id']
        user = gym_member_db.get(user_id)
        user_info_dict=[]
        user_info_dict["height"] = request.form['height']
        user_info_dict["weight"] = request.form['weight']
        user_info_dict["specific_goal"] = request.form['goal']
        user_info_dict["updated_at"] = datetime.date.today().strftime("%d/%m/%Y")

        gym_member_db.update(user_info_dict, user_id)
        msg = "updated successfully"
        return render_template('home.html', msg=msg, user=user)
    else:
        return render_template('home.html', msg='unsuccessful update (session error)')

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