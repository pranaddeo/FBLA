# All of the imports needed for this page to opperate 
from flask import Flask, Blueprint, render_template, request, url_for, redirect, session
from pymongo import MongoClient
from website.views import views
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo
from website.models import User
from flask_session import Session
# In order to check the date for SOTM for when to refresh the SOTM random winners
from datetime import date
import time
# To authenticate the MognoClient, certifi is required
import certifi
# to get random winners for SOTM
import random
# Our database connection and how it is set up for the authentication later 
ca = certifi.where()
client = MongoClient("mongodb+srv://mrmutturaja389:FBLA202223@fbla.mrh4gqm.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.dpfbla
auth = Blueprint('auth', __name__)
s = db.fbladata
c = db.clubs
@auth.route("/SignIn", methods=['GET', 'POST'])
def signin():
    # Signs in user and saves all of their data to a flask session
    data = request.form
    email = data.get('email')
    password = data.get('password')
    if email != None and password != None:
        check = s.find_one({'username': email})
        if check != None:
            if check['password'] == password:
                login_user(User(check), remember=True)
                session["email"] = email
                session["password"] = password
                session["first_name"] = check['first_name']
                session["last_name"] = check['last_name']
                session["grade"] = check['grade']
                session["points"] = check['points']
                session["prizes"] = False
                session["clubs"] = check['clubs']
                session["type"] = check['type']
                session["events"] = None
                high = 0
                listnine = []
                listten = []
                listeleven = []
                listtwelve = []
                if session.get('highestfn') == None:
                    for document in s.find():
                        if document['points'] > high:
                            session["highestfn"] = document['first_name']
                            session["highestln"] = document['last_name']
                            session["highestg"] = document['grade']
                            session["highestp"] = document['points']
                            high = document['points']
                        if int(document['grade']) == 9:
                            listnine.append(document)
                        elif int(document['grade']) == 10:
                            listten.append(document)
                        elif int(document['grade']) == 11:
                            listeleven.append(document)
                        else:
                            listtwelve.append(document)
                    ninesotm = random.choice(listnine)
                    tensotm = random.choice(listten)
                    elevensotm = random.choice(listeleven)
                    twelvesotm = random.choice(listtwelve)
                    session["sotm9fn"] = ninesotm['first_name']
                    session["sotm9ln"] = ninesotm['last_name']
                    session["sotm9p"] = ninesotm['points']
                    session["sotm10fn"] = tensotm['first_name']
                    session["sotm10ln"] = tensotm['last_name']
                    session["sotm10p"] = tensotm['points']
                    session["sotm11fn"] = elevensotm['first_name']
                    session["sotm11ln"] = elevensotm['last_name']
                    session["sotm11p"] = elevensotm['points']
                    session["sotm12fn"] = twelvesotm['first_name']
                    session["sotm12ln"] = twelvesotm['last_name']
                    session["sotm12p"] = twelvesotm['points']
                for club in session["clubs"]:
                    session[club] = c.find_one({'clubname': club})['events']
                if check['type'] == "admin":
                    return redirect(url_for('views.HomeAD'))
                elif check['type'] == "sponsor":
                    return redirect(url_for('views.HomeSP'))
                else:
                    return redirect(url_for('views.HomeST'))
    return render_template("SignIn.html", user=current_user)

@auth.route("/SignUp", methods=['GET', 'POST'])
def signup():
    # Signs up user and redirects them to sign in
    email = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    points = 0
    
    # Insert new user document into the fbladata collection
    if email != None:
        grade = int(request.form.get('grade'))
        s.insert_one({'username': email, 'password': password, 'first_name': first_name, 'last_name': last_name, 'grade': grade, 'points': points, 'clubs':{}, 'type': "student"})
        check = s.find_one({'username': email})
        login_user(User(check), remember=True)
        return redirect(url_for('auth.signin'))
    # Redirect the user to the home page
    return render_template("SignUp.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    # Saves all parts of session that need to be saved and clears every other part of the session while updating the points to MongoDB
    a = session["highestfn"]
    b = session["highestln"]
    c = session["highestg"]
    d = session["highestp"]
    e = session["sotm9fn"]
    f = session["sotm9ln"]
    g = session["sotm9p"]
    h = session["sotm10fn"]
    i = session["sotm10ln"]
    j = session["sotm10p"]
    k = session["sotm11fn"]
    l = session["sotm11ln"]
    m = session["sotm11p"]
    n = session["sotm12fn"]
    o = session["sotm12ln"]
    p = session["sotm12p"]
    s.find_one_and_update({"first_name": session['first_name']}, {"$set": {"points": session['points']}})
    session.clear()
    logout_user()
    session["highestfn"] = a
    session["highestln"] = b
    session["highestg"] = c
    session["highestp"] = d
    session["sotm9fn"] = e
    session["sotm9ln"] = f
    session["sotm9p"] = g
    session["sotm10fn"] = h
    session["sotm10ln"] = i
    session["sotm10p"] = j
    session["sotm11fn"] = k
    session["sotm11ln"] = l
    session["sotm11p"] = m
    session["sotm12fn"] = n
    session["sotm12ln"] = o
    session["sotm12p"] = p
    return redirect(url_for('views.HomeNA'))



@views.route("/NewClub", methods=['GET', 'POST'])
def Club():
    # Adds club to club database
    clubname = request.form.get('clubname')
    sponsorname = request.form.get('sponsorname')
    sponsoremail = request.form.get('sponsoremail')
    roomnum = request.form.get('roomnum')
    
    if clubname != None:
        c.insert_one({'clubname': clubname, 'sponsorname': sponsorname, 'sponsoremail': sponsoremail, 'roomnum': int(roomnum)})
        return redirect(url_for('views.HomeAD'))
    return render_template("NewClub.html", user=current_user)