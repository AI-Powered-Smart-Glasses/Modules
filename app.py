from flask import Flask, render_template, request,redirect,Markup
import numpy as np
import pandas as pd
import requests
import config
import pickle
import io
from PIL import Image
from flask_mail import Mail
import sys
sys.path.append('Module-4')
import mymain
# # ===============================================================================================

# # ------------------------------------ FLASK APP -------------------------------------------------

gmail_username="info.smartagrisolutions@gmail.com"
gmail_username2="kukreja.him@gmail.com"
gmail_password="woqhfnyooqamziey"

app = Flask(__name__)

app.secret_key = 'secret-key'
app.config.update(
  MAIL_SERVER = 'smtp.gmail.com',
  MAIL_PORT ='465',
  MAIL_USE_SSL = "True",
  MAIL_USERNAME=gmail_username,
  MAIL_PASSWORD=gmail_password
)

mail =Mail(app)

# render home page


@ app.route('/',methods= ['GET', 'POST'])
def home():
    heading='Smart AI Glasses for Blind'
    subheading='Improving Lifestyle for Blinf'
    title = 'Smart AI - Home'

    if request.method=="POST":
        name = request.form['name']
        email =request.form['email']
        phone =request.form['phone']
        message =request.form['message']
        # print("Message via post request: ",name,email)

        mail.send_message('New message from  ' + name + ' via  '+"SmartAgri Solutions", 
                          sender= email, 
                          recipients =[gmail_username,gmail_username2],
                          body = message + "\n" + "Contact No.: "+ phone 
                          )

        reply= "Thanks for reaching to us.\nYou will receive your reply shortly.\nTill then stay happy.\nThis is computer generated mail kindly don't reply back.\nFor more information contact the admin\nHimanshu Kukreja\nhkukreja_be19@thapar.edu\n9915579903"
        mail.send_message('Thanks for Contacting SmartAgri Solutions', 
                        sender=gmail_username, 
                        recipients =[email],
                        body = reply
                        )
        return render_template('index.html',title=title,heading=heading,subheading=subheading,home=True,message_sent=True)
      
    return render_template('index.html', title=title,heading=heading,subheading=subheading,home=True)


@ app.route('/reco', methods= ['GET', 'POST'])
def recognize():
    mymain.reco()
    heading='Smart AI Glasses for Blind'
    subheading='Improving Lifestyle for Blinf'
    title = 'Smart AI - Home'

    return render_template('index.html', title=title,heading=heading,subheading=subheading,home=True)

@ app.route('/caption', methods= ['GET', 'POST'])
def caption():
    mymain.caption()
    heading='Smart AI Glasses for Blind'
    subheading='Improving Lifestyle for Blinf'
    title = 'Smart AI - Home'

    return render_template('index.html', title=title,heading=heading,subheading=subheading,home=True)

@ app.route('/trafficLights', methods= ['GET', 'POST'])
def trafficLights():
    mymain.trafficLights()
    heading='Smart AI Glasses for Blind'
    subheading='Improving Lifestyle for Blinf'
    title = 'Smart AI - Home'

    return render_template('index.html', title=title,heading=heading,subheading=subheading,home=True)

@ app.route('/doclassify', methods= ['GET', 'POST'])
def doclassify():
    mymain.doclassify()
    heading='Smart AI Glasses for Blind'
    subheading='Improving Lifestyle for Blinf'
    title = 'Smart AI - Home'

    return render_template('index.html', title=title,heading=heading,subheading=subheading,home=True)


if __name__ == '__main__':
    app.run(debug=True)