from flask import Flask, render_template, request
from dotenv import load_dotenv
import datetime
from deta import Deta
import os

load_dotenv()

DETA_KEY = os.getenv("DETA_KEY")
deta = Deta(DETA_KEY)

gym_member_db = deta.Base("User_DB")

gym_members = gym_member_db.fetch().items
gym_member_ids = []
for gym_member in gym_members:
    gym_member_ids.append(gym_member["id"])

now = datetime.datetime.now()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    to edit perosoanl data
    """
    msg = "did not get user_id"
    if request.method == 'POST' and 'userId' in request.form and 'userName' in request.form:
        user_id = request.form['userId']
        user_name = request.form['userName']
        
        msg ="user id is {} and user name {}".format(user_id, user_name)

        if user_id not in gym_member_ids:
            msg = "did not registered"
            return render_template('home_1.html')
        # user_id = request.form.get("userId")
        # user_name = request.form.get("userName")

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