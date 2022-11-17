import numpy as np
import os
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import load_img,img_to_array
from flask import Flask,render_template,request
from twilio.rest import Client

app=Flask(__name__)

model = load_model('/home/veeraraghavan/Desktop/Flask_web_app/Forestfire.h5')
def send_message():
  account_sid = 'AC4c6802dceef3f53e86d8f323381b6e9f' 
  auth_token = '00de958a0cd6b0507e9d48189f4fe5a0' 
  client = Client(account_sid, auth_token) 
 
  message = client.messages.create(  
                              messaging_service_sid='MG39f0273fc2caf682130af0fe591f15ca', 
                              body='forest_fire',      
                              to='+918925643320' 
                          ) 
 
  print(message.sid)
   
  print("Fire Detected")
  print("SMS Sent") 
@app.route('/')
def index():
    return render_template("index.html")
text=''
@app.route('/predict',methods=['GET','POST'])
def upload():
    msg_sent=False
    text=""
    if request.method=='POST':
        f=request.files['image']
        basepath=os.path.dirname(__file__)
        filepath=os.path.join(basepath,'uploads',f.filename)
        f.save(filepath)
        v = 0
        vid= cv2.VideoCapture(filepath)
        if vid.isOpened():
          while True:
            success,frame = vid.read()
            if success:
                 
                 cv2.imwrite('output.jpg',frame)
                 s='/home/veeraraghavan/Desktop/Flask_web_app/output.jpg'
                 img = image.load_img(s,target_size=(150,150))
                 x = image.img_to_array(img)
                 x = np.expand_dims(x,axis=0)
                 predict = model.predict(x)
                 y = int(predict[0][0])
            
                 if y==0:
                      if not msg_sent:
                           print("fire")
                           text="Fire detected"
                           send_message()
                           msg_sent=True
                 else:
                    print("No Forest Fire Detected")
                    text="no fire"
   
            else:
               break
            cv2.imshow('frame',frame)
            print("frame")
            print(v)
            v+=1
         
            
               
        vid.release()
    cv2.destroyAllWindows()
    return text 
if __name__=='__main__':
    app.run(debug=False)
