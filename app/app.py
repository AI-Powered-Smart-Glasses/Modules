from flask import Flask, render_template, request,redirect,Markup
import numpy as np
import pandas as pd
from utils.disease import disease_dic
from utils.fertilizer import fertilizer_dic
import requests
import config
import pickle
import io
import torch
from torchvision import transforms
from PIL import Image
from utils.model import ResNet9
from utils.disease_classes import disease_classes
from flask_mail import Mail

# -------------------------LOADING THE TRAINED MODELS -----------------------------------------------

# Loading plant disease classification model

disease_model_path = 'models/plant_disease_model.pth'
disease_model = ResNet9(3, len(disease_classes))
disease_model.load_state_dict(torch.load(
disease_model_path, map_location=torch.device('cpu')))
disease_model.eval()


# Loading crop recommendation model

crop_recommendation_model_path = 'models/RandomForest.pkl'
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))


# =========================================================================================

# Custom functions for calculations


def weather_fetch(city_name):

    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    api_key = config.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None


def predict_image(img, model=disease_model):
    """
    Transforms image to tensor and predicts disease label
    :params: image
    :return: prediction (string)
    """
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(img))
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t, 0)

    # Get predictions from model
    yb = model(img_u)
    # Pick index with highest probability
    _, preds = torch.max(yb, dim=1)
    prediction = disease_classes[preds[0].item()]
    # Retrieve the class label
    return prediction

# ===============================================================================================
# ------------------------------------ FLASK APP -------------------------------------------------

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

# render crop recommendation form page


@ app.route('/crop', methods= ['GET', 'POST'])
def crop_recommend():
    heading='Smart AI Glasses for Blind'
    subheading='Improving Lifestyle for Blinf'
    title = 'Smart AI - Home'

    if request.method=='POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        # state = request.form.get("stt")
        city = request.form.get("city")

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]
            print(final_prediction)
            params={"N":N,"P":P,K:"K","ph":ph,"rainfall":rainfall,"city": city,"temp":temperature,"hum":humidity}
            return render_template('crop.html', title=title,heading=heading,subheading=subheading,prediction=final_prediction,params=params,done="True")
        else:
            return render_template('crop.html', title=title,heading=heading,subheading=subheading,city=city,done="Error")
        
    return render_template('crop.html', title=title,heading=heading,subheading=subheading,done=False)

# # render fertilizer recommendation form page


@ app.route('/fertilizer', methods=['GET','POST'])
def fertilizer_recommendation():
    
    heading='Smart AI Glasses for Blind'
    subheading='Improving Lifestyle for Blinf'
    title = 'Smart AI - Home'

    if request.method == 'POST':
        crop_name = str(request.form['cropname'])
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        # ph = float(request.form['ph'])

        df = pd.read_csv('../processed_data/fertilizer.csv')

        nr = df[df['Crop'] == crop_name]['N'].iloc[0]
        pr = df[df['Crop'] == crop_name]['P'].iloc[0]
        kr = df[df['Crop'] == crop_name]['K'].iloc[0]

        n = nr - N
        p = pr - P
        k = kr - K
        temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
        max_value = temp[max(temp.keys())]
        if max_value == "N":
            if n < 0:
                key = 'NHigh'
            else:
                key = "Nlow"
        elif max_value == "P":
            if p < 0:
                key = 'PHigh'
            else:
                key = "Plow"
        else:
            if k < 0:
                key = 'KHigh'
            else:
                key = "Klow"
        response = Markup(str(fertilizer_dic[key]))
        return render_template('fertilizer.html', recommendation=response, title=title,heading=heading,subheading=subheading,check="True")

    return render_template('fertilizer.html', title=title,heading=heading,subheading=subheading)




@app.route('/disease', methods=['GET', 'POST'])
def disease_prediction():
    heading='Smart AI Glasses for Blind'
    subheading='Improving Lifestyle for Blinf'
    title = 'Smart AI - Home'

    if request.method == 'POST':
        if 'file' not in request.files:
            # print("file not in request")
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            # print("file not present")
            return render_template('disease.html', title=title,ok="False")
        try:
            img = file.read()
            # print("predicting........")
            try:
                prediction = predict_image(img)
            except:
                render_template('disease.html', title=title,heading=heading,subheading=subheading)

            prediction = Markup(str(disease_dic[prediction]))
            # print(prediction)
            return render_template('disease.html', title=title,heading=heading,
                                subheading=subheading, ok="True",
                                prediction=prediction)
        except:
            print("Error")
            pass
    return render_template('disease.html', title=title,heading=heading,subheading=subheading)



if __name__ == '__main__':
    app.run(debug=True)