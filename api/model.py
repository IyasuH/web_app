from dotenv import load_dotenv
from deta import Deta
import datetime
import os

load_dotenv()

DETA_KEY = os.getenv("DETA_KEY")
MY_ID = os.getenv("MY_ID")
deta = Deta(DETA_KEY)


def personal_info():
    """
    this table is to store all personal information about the user where primary key is user telegram id
    """
    
# ----------------personal info db-----------------
    user_db = deta.Base("User_DB")

    full_name = "Eyasu Hailegebriel" #string type
    dob = datetime.date(2001, 5, 5).strftime("%d/%m/%Y") #datetime type
    gender = "M" #string (but make these to be choosen)
    height = 169.0 #floating point number in cm
    weight = 62.5 #floating point number in kg
    main_goal = "To be active and to increase strength"#string type
    entry_date = datetime.date.today().strftime("%d/%m/%Y") #datetime type the date gym started
    created_at = datetime.date.today().strftime("%d/%m/%Y") # data created date datetime
    updated_at = created_at #data updated date initially equals to created_at

# and data from telegram
    first_name = "Iyasu"#string type default value empty string
    last_name = "H"#string type default value empty string
    user_name = "IyasuHa"#string type default value empty string
    user_id = MY_ID#string, which is telegram user id

# and Additional info about user body 

    fat_percent = "" # in %
    waist_circumference = "" # in cm
    hip_circumference = "" # in cm
    calf_circumference = "" # in cm
    chest_width = "" # in cm
    shoulder_width = "" # in cm
    bicep_circumference = "" # in cm


    user_info_dict = {}

    user_info_dict["full_name"] = full_name
    user_info_dict["dob"] =dob
    user_info_dict["gender"]=gender
    user_info_dict["height"]=height
    user_info_dict["weight"]=weight
    user_info_dict["main_goal"]=main_goal
    user_info_dict["entry_date"]=entry_date
    user_info_dict["created_at"]=created_at
    user_info_dict["updated_at"]=updated_at
    user_info_dict["first_name"]=first_name
    user_info_dict["last_name"]=last_name
    user_info_dict["user_name"]=user_name
    user_info_dict["key"] =user_id
    user_info_dict["user_id"]=user_id

    user_info_dict["fat_percent"] = fat_percent
    user_info_dict["waist_circumference"] = waist_circumference
    user_info_dict["hip_circumference"] = hip_circumference
    user_info_dict["calf_circumference"] = calf_circumference
    user_info_dict["chest_width"] = chest_width
    user_info_dict["shoulder_width"] = shoulder_width
    user_info_dict["bicep_circumference"] = bicep_circumference

    user_db.put(user_info_dict)

# personal_info()



def exercise_log():
    """
    this table is to store the exercise log - where id(primary key) for each log (row) will be automatically generated
    """
    
#---------------exercise log------------
    log_db = deta.Base("Log_DB")

    body_area = "Biceps" # make users to be specific about the body of area
    exercise_name = "Normal push ups" # here also be specifc about the exercise
    equipment_used = "none" # be specifc like 8kg dumbbells
    number_of_reps = 10 # number of reps in single round
    number_of_cycles = 3 # or number of rounds
    exercise_duration = "12" # this to measure for how much period of time(in minute) the exercise is performed (can be critical for some activities like planks)
    feeling = "just right" # this will be how the user feels after each exercise and it will be ENUM type where users choose between ("too easy", "a little easy", "just right", "a little hard", "too hard")
    date_worked = datetime.date.today().strftime("%d/%m/%Y") #make the default date to be today asuming users most of the time enter todays exercise after it
    additional_info = "especially the last round was challenging" # any additional info user wants to add 
    user_id = MY_ID # this is telegram id 
# key automatically assigned

    log_info_dict = {}

    log_info_dict["body_area"] = body_area
    log_info_dict["exercise_name"] = exercise_name
    log_info_dict["equipment_used"] = equipment_used
    log_info_dict["number_of_reps"] = number_of_reps
    log_info_dict["number_of_cycles"] = number_of_cycles
    log_info_dict["exercise_duration"] = exercise_duration
    log_info_dict["feeling"] = feeling
    log_info_dict["date_worked"] = date_worked
    log_info_dict["additional_info"] = additional_info
    log_info_dict["user_id"] = user_id

    log_db.put(log_info_dict)

# exercise_log()

def treadmill_log():
    """
    this table is to enter treadmill log - where key(primary key) for each log (row) will be automatically generated
    """
    treadmill_db = deta.Base("Treadmill_DB")
    # steps
    # distance - mile/kilometer
    # minutes
    # burned calories - kilo joules
    # max_speed(to be maximum speed user have to run on that speed atleast for 20sec) - unit
    # max_inclination(to be maximum inclination user have to run on that inclination at least for 20 sec) - unit
    # feeling
    # additional_note

    tm_log_dict = {}

    tm_log_dict["steps"] = 1000
    tm_log_dict["distance"] = "3.4" # I don't know the exact unit of the machine output(for now asuming km)
    tm_log_dict["minute"] = 15 # 
    tm_log_dict["calories"] = "110" # also here I don't know the unit(for now asuming in kj)
    tm_log_dict["max_speed"] = "13.5" # no idea for its unit
    tm_log_dict["max_incline"] = "12" # no idea for its unit
    tm_log_dict["feeling"] = "A Little Hard"
    tm_log_dict["date"] = datetime.date.today().strftime("%d/%m/%Y")
    tm_log_dict["user_id"] = MY_ID
    tm_log_dict["notes"] = "I synced with the music"

    treadmill_db.put(tm_log_dict)
    
treadmill_log()

def change_log():
    """
    this table is to record changes in user physical
    """
    
#---------------change log db--------------
    change_log_db = deta.Base("Change_Log_DB")
# this database table is intended to record the body measurments changes
# so finally users can see the changes
# and get motiovated and also can be portifolio for trainer 

    weigth = "62.5" # in kg
    height = "169.0" # in cm

    fat_percent = "30" # in %
    waist_circumference = "32" # in cm
    hip_circumference = "15" # in cm
    calf_circumference = "8" # in cm
    chest_width = "30" # in cm
    shoulder_width = "28" # in cm
    bicep_circumference = "9" # in cm

    date_recorded = datetime.date.today().strftime("%d/%m/%Y")
    user_id = MY_ID

    change_log_dict = {}
    change_log_dict["weight"] = weigth
    change_log_dict["height"] = height
    change_log_dict["fat_percent"] = fat_percent
    change_log_dict["waist_circum"] = waist_circumference
    change_log_dict["hip_circum"] = hip_circumference
    change_log_dict["calf_circum"] = calf_circumference
    change_log_dict["chest_width"] = chest_width
    change_log_dict["shoulder_width"] = shoulder_width
    change_log_dict["bicep_circum"] = bicep_circumference
    change_log_dict["date_recorded"] = date_recorded
    change_log_dict["user_id"] = user_id

    change_log_db.put(change_log_dict)
    # key automatically assigned
# change_log()

def goal_setting():
    """
    this table is to record users SMART goal
    """
    
# ----------------goal setting db----------------------

    smart_goal_db = deta.Base("SMART_goal_DB")
    # SMART goal(specific, measurable, achivable, reliable, time bounded)
    # to record individuals SMART goal 
    # which can create sense of accomplishment

    goal_statment = "" # here is where the goal specific statment will be put
    setup_at = datetime.date.today().strftime("%d/%m/%Y") # specifc date the goal setupped
    tobe_achived_at = datetime.date(2023, 11, 23).strftime("%d/%m/%Y") # when to be achived
    goal_progress = "" # goal progress in %
    updated_at = setup_at # date value when the goal elements are changed inital value is equal to set_up_date
    goal_state = False # whether the goal is achieved or not bool value 

# goal_setting()


def create_waiting_db():
    """
    this is created when new user requests admin permission to be memeber 
    """
    
#-----------------------waiting db------------------------------
    waiting_db = deta.Base("Waiting_DB")
    # this lists are list of users who requested admin's to approve them as gym_user

    # this data is directly recived from telegram 
    first_name = "Iyasu" # Optional 
    last_name = "H" # Optional
    user_name = "IyasuHa" # Optional 
    user_id = MY_ID # please delete this
    is_bot = False # optional if users is a bot
    allows_write_to_pm = True # if the user allowed the bot to message them
    approved = False

    requested_at = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

    # and the other data will be entered from by user
    # okay let make the other data to be submitted by user after their account is created
    # when the user authenticate User_DB will be created 

    waiting_info_dict = {}

    waiting_info_dict["first_name"] = first_name
    waiting_info_dict["last_name"] = last_name
    waiting_info_dict["user_name"] = user_name
    waiting_info_dict["user_id"] = user_id
    waiting_info_dict["is_bot"] = is_bot
    waiting_info_dict["allows_write"] = allows_write_to_pm
    waiting_info_dict["requested_at"] = requested_at
    waiting_info_dict["approved"] = approved
    waiting_info_dict["key"] = user_id

    waiting_db.put(waiting_info_dict)

# create_waiting_db()