# All the imports needed for this page
import os
from flask import Blueprint, render_template, send_from_directory, redirect, url_for, session, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo
from flask_session import Session
from datetime import date
from pymongo import MongoClient
# To authenticate the MognoClient, certifi is required
import certifi
# to get random winners for SOTM
import random
from random import randint
from flask import Blueprint, render_template, request, url_for, redirect, session
from pymongo import MongoClient
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo
from flask_session import Session
# In order to check the date for SOTM for when to refresh the SOTM random winners
from datetime import date
import certifi
from flask_wtf import Form
from wtforms import SubmitField
from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField
from wtforms.validators import InputRequired, Length
# For quarterly report to get the average points of the grade
from statistics import mean

# MongoDB Setup
ca = certifi.where()
client = MongoClient("mongodb+srv://mrmutturaja389:FBLA202223@fbla.mrh4gqm.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
auth = Blueprint('auth', __name__)
db = client.dpfbla
s = db.fbladata
c = db.clubs

# The setup of all the routes of our website
views = Blueprint('views', __name__)
# Setup of the Home pages
@views.route("/")
def beginning():
    return redirect(url_for('views.HomeNA'))

@views.route("/home")
def HomeNA():
    logout_user()
    return render_template("HomeNA.html")

@views.route("/home/Student")
@login_required
def HomeST():
    return render_template("HomeST.html", user=current_user)

@views.route("/home/Sponsor")
@login_required
def HomeSP():
    return render_template("HomeSP.html", user=current_user)

@views.route("/home/Admin", methods=['GET', 'POST'])
@login_required
def HomeAD():
    data = request.form
    # Making sure when refresh happens, no errors occur
    if data:
        if data.get('club') != "0" and data.get('point') != None and data.get('check') != None:
            session['points'] += int(data.get('point'))
            return redirect(url_for('views.HomeAD'))
    return render_template("HomeAD.html", user=current_user)

# Setup of the Prizes page
@views.route("/Prizes", methods=['GET','POST'])
def Prizes():
    data = request.form
    form = data.get('Purchase')
    k = 0
    # Purchases a prize only when a user clicks on it, not when they refresh the page
    if session.get('points') != None:
        k = session["points"]
    if data:
        if data.get('true') != None:
            if k < 100:
                flash("Insufficient Funds")
            else:
                session["points"] -= 100
                flash("Congrats on the purchase")
    return render_template("Prizes.html")
# Setup for Student of the Month
@views.route("/SOTM")
def SOTM():
    # Gets random winners and top student of the school
    if session.get('sotm9fn') == None or date.today().day == 1:
        high = 0
        listnine = []
        listten = []
        listeleven = []
        listtwelve = []
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
    return render_template("SOTM.html")
# Setup for Clubs
@views.route("/Clubs")
def Clubs():
    return render_template("clubs.html")
# Setup for Sports
@views.route("/Sports")
def Sports():
    return render_template("sports.html")
# Setup for Quarterlt Report
@views.route("/quarterly-report")
def QReport():
    # Gets new report of the average points of students for the quarter
    listnine = []
    listten = []
    listeleven = []
    listtwelve = []
    for document in s.find():
        if int(document['grade']) == 9:
            listnine.append(document['points'])
        elif int(document['grade']) == 10:
            listten.append(document['points'])
        elif int(document['grade']) == 11:
            listeleven.append(document['points'])
        else:
            listtwelve.append(document['points'])
    session["qr9"] = mean(listnine)
    session["qr10"] = mean(listten)
    session["qr11"] = mean(listeleven)
    session["qr12"] = mean(listtwelve)
    return render_template("QReport.html")
# Setup for the FAQ page
@views.route("/FAQ")
def FAQ():
    return render_template("FAQ.html")
# This checks wether form is filled out
class StatsForm(FlaskForm):
    user_stats = SubmitField()
    room_stats = SubmitField()