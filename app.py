import numpy as np
import pickle
from flask import Flask, redirect, request, render_template, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


model = pickle.load(open('canp_model.pkl', 'rb')) 


app = Flask(__name__)

current_page = None



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index')
def index():
    return render_template('index.html',result="**Your risk will be shown here**")

@app.route('/predict', methods =['POST'])
def predict():
    features = [i for i in request.form.values()]
    name=features[0]
    phone=features[1]
    array_features = [np.array(features[2:])]
    prediction = model.predict(array_features)
    output = prediction
    if output == 3:
        output=0
        mes='high'
        send_email(name, phone, mes, to_email="rahulkumarjha.cs20@bitsathy.ac.in")
        return render_template('index.html', 
                               result = '''Your health is our top concern. 
                               Recent assessment indicate a HIGH significant risk of cancer. 
                               It's crucial to act swiftly. 
                               Please consult a doctor without delay to discuss this matter and plan the best course of action.''')
    
    elif output == 1:
        output=0
        return render_template('index.html', 
                               result = 'The patient is likely to have low risk!')
    elif output == 2:
         output=0
         mes='medium'
         send_email(name, phone, mes, to_email="rahuljha190802@gmail.com")
         return render_template('index.html', 
                               result = '''Your health is our top concern. 
                               Recent assessment indicate a MEDIUM significant risk of cancer. 
                               It's crucial to act swiftly. 
                               Please consult a doctor without delay to discuss this matter and plan the best course of action.''')
    return render_template('index.html',result="**Your risk will be shown here**")


def send_email(name, phone, message, to_email):
    from_email = 'doctorcancer000@gmail.com' 
    password = 'huwrfpyryparmskf'  

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Urgent: Risk of Cancer in Patient's Condition"

    html_message = f'''
<html>
  <body style="background-image: url('https://previews.123rf.com/images/ileezhun/ileezhun1508/ileezhun150800156/44189241-cancer-pink-ribbon-horizontal-background.jpg');  background-repeat: no-repeat; background-size: cover; background-attachment: fixed; margin: 0; padding: 0;">
    <div style="background-color: rgba(255, 255, 255, 0.7);  border-radius: 10px; padding: 20px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
    <p><b>Hello, Dr. Doctor</b></p>
    <p>We urgently need your expertise regarding a <b>{message}</b> risk of cancer for my patient, {name}. 
    The patient's contact number is +91{phone}, Your prompt attention to this matter is greatly appreciated.</p>
    <p>Regards,</p>
    <p>Cancer Guardian App</p>
    </div>
  </body>
</html>
'''
    # message=f'''Dear Dr. Doctor,\nWe urgently need your expertise regarding a {message} risk of cancer for my patient, {name}. 
    # The patient's contact number is +91{phone}, Your prompt attention to this matter is greatly appreciated.'''
    msg.attach(MIMEText(html_message, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print("SMTP connection failed:", e)


if __name__ == '__main__':
    app.run()
